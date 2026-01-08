"""
Quantum Chess Backend API

FastAPI server with WebSocket support for real-time multiplayer quantum chess.
"""

import os
import uuid
import json
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .quantum_engine import (
    QuantumChessEngine, QuantumChessGame, QuantumMove,
    MoveType, MoveVariant, Color
)
from .gemini_ai import QuantumChessAIGame, GeminiChessAI


# Game storage (in production, use Redis or database)
games: Dict[str, QuantumChessGame] = {}
ai_games: Dict[str, QuantumChessAIGame] = {}
websocket_connections: Dict[str, Dict[str, WebSocket]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    print("🎮 Quantum Chess Server starting...")
    yield
    print("🎮 Quantum Chess Server shutting down...")


app = FastAPI(
    title="Quantum Chess API",
    description="A quantum computing-powered chess game using Cirq",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class CreateGameRequest(BaseModel):
    player_name: str
    game_type: str = "multiplayer"  # multiplayer or ai
    ai_difficulty: str = "medium"  # easy, medium, hard
    player_color: str = "white"  # For AI games


class JoinGameRequest(BaseModel):
    player_name: str


class MoveRequest(BaseModel):
    source: str
    target1: str
    target2: Optional[str] = None
    move_type: str = "standard"


class GameResponse(BaseModel):
    game_id: str
    success: bool
    message: str = ""


# REST API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Quantum Chess API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "games": "/api/games",
            "create_game": "POST /api/games",
            "join_game": "POST /api/games/{game_id}/join",
            "websocket": "/ws/{game_id}/{player_id}"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_games": len(games) + len(ai_games)
    }


@app.post("/api/games")
async def create_game(request: CreateGameRequest):
    """Create a new game"""
    game_id = str(uuid.uuid4())[:8]
    player_id = str(uuid.uuid4())[:8]

    if request.game_type == "ai":
        # Create AI game
        player_color = Color.WHITE if request.player_color == "white" else Color.BLACK
        api_key = os.getenv("GEMINI_API_KEY")

        ai_game = QuantumChessAIGame(
            game_id=game_id,
            player_color=player_color,
            api_key=api_key,
            difficulty=request.ai_difficulty
        )
        ai_games[game_id] = ai_game

        return {
            "success": True,
            "game_id": game_id,
            "player_id": player_id,
            "game_type": "ai",
            "player_color": request.player_color,
            "ai_difficulty": request.ai_difficulty,
            "message": "AI game created. Start when ready."
        }
    else:
        # Create multiplayer game
        game = QuantumChessGame(game_id=game_id)
        result = game.add_player(player_id)

        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])

        games[game_id] = game

        return {
            "success": True,
            "game_id": game_id,
            "player_id": player_id,
            "color": result['color'],
            "game_type": "multiplayer",
            "message": "Game created. Share the game ID with your opponent."
        }


@app.get("/api/games")
async def list_games():
    """List all active games"""
    game_list = []

    for game_id, game in games.items():
        game_list.append({
            "game_id": game_id,
            "type": "multiplayer",
            "players": {
                "white": game.players[Color.WHITE] is not None,
                "black": game.players[Color.BLACK] is not None
            },
            "started": game.started,
            "ended": game.ended
        })

    for game_id, game in ai_games.items():
        game_list.append({
            "game_id": game_id,
            "type": "ai",
            "started": game.started,
            "ended": game.ended
        })

    return {"games": game_list}


@app.get("/api/games/{game_id}")
async def get_game(game_id: str):
    """Get game state"""
    if game_id in games:
        return games[game_id].get_state()
    elif game_id in ai_games:
        return ai_games[game_id].get_state()
    else:
        raise HTTPException(status_code=404, detail="Game not found")


@app.post("/api/games/{game_id}/join")
async def join_game(game_id: str, request: JoinGameRequest):
    """Join an existing game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    player_id = str(uuid.uuid4())[:8]

    result = game.add_player(player_id)

    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])

    return {
        "success": True,
        "game_id": game_id,
        "player_id": player_id,
        "color": result['color'],
        "message": "Joined game successfully"
    }


@app.post("/api/games/{game_id}/start")
async def start_game(game_id: str):
    """Start a game"""
    if game_id in games:
        game = games[game_id]
        result = game.start_game()
    elif game_id in ai_games:
        game = ai_games[game_id]
        result = game.start_game()
    else:
        raise HTTPException(status_code=404, detail="Game not found")

    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])

    # Notify via WebSocket
    await broadcast_to_game(game_id, {
        "type": "game_started",
        "board_state": result['board_state']
    })

    return result


@app.post("/api/games/{game_id}/move")
async def make_move(game_id: str, request: MoveRequest, player_id: str = Query(...)):
    """Make a move via REST API"""

    move = QuantumMove(
        source=request.source,
        target1=request.target1,
        target2=request.target2,
        move_type=MoveType(request.move_type)
    )

    if game_id in games:
        game = games[game_id]
        result = game.make_move(player_id, move)
    elif game_id in ai_games:
        game = ai_games[game_id]
        result = await game.player_move(move)
    else:
        raise HTTPException(status_code=404, detail="Game not found")

    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result.get('error', 'Move failed'))

    # Broadcast to other players
    await broadcast_to_game(game_id, {
        "type": "move_made",
        "move": {
            "source": request.source,
            "target1": request.target1,
            "target2": request.target2,
            "move_type": request.move_type
        },
        "result": result
    })

    return result


@app.get("/api/games/{game_id}/legal-moves/{square}")
async def get_legal_moves(game_id: str, square: str):
    """Get legal moves for a piece"""
    if game_id in games:
        engine = games[game_id].engine
    elif game_id in ai_games:
        engine = ai_games[game_id].engine
    else:
        raise HTTPException(status_code=404, detail="Game not found")

    moves = engine.get_legal_moves(square)
    return {"square": square, "moves": moves}


@app.post("/api/games/{game_id}/undo")
async def undo_move(game_id: str, player_id: str = Query(...)):
    """Undo the last move"""
    if game_id in games:
        engine = games[game_id].engine
    elif game_id in ai_games:
        engine = ai_games[game_id].engine
    else:
        raise HTTPException(status_code=404, detail="Game not found")

    result = engine.undo_last_move()

    if result['success']:
        await broadcast_to_game(game_id, {
            "type": "move_undone",
            "result": result
        })

    return result


# WebSocket endpoints

async def broadcast_to_game(game_id: str, message: dict):
    """Broadcast a message to all players in a game"""
    if game_id in websocket_connections:
        for player_id, websocket in websocket_connections[game_id].items():
            try:
                await websocket.send_json(message)
            except Exception:
                pass


@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    """WebSocket endpoint for real-time game updates"""
    await websocket.accept()

    # Register connection
    if game_id not in websocket_connections:
        websocket_connections[game_id] = {}
    websocket_connections[game_id][player_id] = websocket

    try:
        # Send current game state
        if game_id in games:
            state = games[game_id].get_state()
        elif game_id in ai_games:
            state = ai_games[game_id].get_state()
        else:
            await websocket.send_json({"error": "Game not found"})
            return

        await websocket.send_json({
            "type": "connected",
            "player_id": player_id,
            "game_state": state
        })

        # Notify other players
        await broadcast_to_game(game_id, {
            "type": "player_joined",
            "player_id": player_id
        })

        # Listen for messages
        while True:
            data = await websocket.receive_json()
            await handle_websocket_message(game_id, player_id, data, websocket)

    except WebSocketDisconnect:
        # Remove connection
        if game_id in websocket_connections:
            websocket_connections[game_id].pop(player_id, None)
            if not websocket_connections[game_id]:
                del websocket_connections[game_id]

        # Notify other players
        await broadcast_to_game(game_id, {
            "type": "player_left",
            "player_id": player_id
        })


async def handle_websocket_message(game_id: str, player_id: str, data: dict, websocket: WebSocket):
    """Handle incoming WebSocket messages"""
    message_type = data.get("type")

    if message_type == "move":
        # Handle move
        move = QuantumMove(
            source=data.get("source"),
            target1=data.get("target1"),
            target2=data.get("target2"),
            move_type=MoveType(data.get("move_type", "standard"))
        )

        if game_id in games:
            result = games[game_id].make_move(player_id, move)
        elif game_id in ai_games:
            result = await ai_games[game_id].player_move(move)
        else:
            await websocket.send_json({"error": "Game not found"})
            return

        # Send result to player
        await websocket.send_json({
            "type": "move_result",
            "result": result
        })

        if result.get('success'):
            # Broadcast to other players
            await broadcast_to_game(game_id, {
                "type": "move_made",
                "player_id": player_id,
                "move": {
                    "source": data.get("source"),
                    "target1": data.get("target1"),
                    "target2": data.get("target2"),
                    "move_type": data.get("move_type", "standard")
                },
                "result": result
            })

    elif message_type == "get_legal_moves":
        square = data.get("square")

        if game_id in games:
            engine = games[game_id].engine
        elif game_id in ai_games:
            engine = ai_games[game_id].engine
        else:
            await websocket.send_json({"error": "Game not found"})
            return

        moves = engine.get_legal_moves(square)
        await websocket.send_json({
            "type": "legal_moves",
            "square": square,
            "moves": moves
        })

    elif message_type == "chat":
        # Broadcast chat message
        await broadcast_to_game(game_id, {
            "type": "chat",
            "player_id": player_id,
            "message": data.get("message", "")
        })

    elif message_type == "offer_draw":
        await broadcast_to_game(game_id, {
            "type": "draw_offered",
            "player_id": player_id
        })

    elif message_type == "resign":
        if game_id in games:
            games[game_id].ended = True
        elif game_id in ai_games:
            ai_games[game_id].ended = True

        await broadcast_to_game(game_id, {
            "type": "game_ended",
            "reason": "resignation",
            "resigned_player": player_id
        })


# Learning Path API

@app.get("/api/learning/modules")
async def get_learning_modules():
    """Get all learning modules"""
    from .learning_content import LEARNING_MODULES
    return {"modules": LEARNING_MODULES}


@app.get("/api/learning/modules/{module_id}")
async def get_learning_module(module_id: str):
    """Get a specific learning module"""
    from .learning_content import get_module_by_id
    module = get_module_by_id(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@app.get("/api/learning/modules/{module_id}/lessons/{lesson_id}")
async def get_lesson(module_id: str, lesson_id: str):
    """Get a specific lesson"""
    from .learning_content import get_lesson
    lesson = get_lesson(module_id, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


# Quantum simulation endpoint for learning

@app.post("/api/quantum/simulate")
async def simulate_quantum_circuit(circuit_data: dict):
    """Simulate a simple quantum circuit for learning purposes"""
    import cirq
    import numpy as np

    try:
        gates = circuit_data.get("gates", [])
        num_qubits = circuit_data.get("num_qubits", 2)

        qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
        circuit = cirq.Circuit()

        for gate in gates:
            gate_type = gate.get("type")
            targets = gate.get("targets", [0])

            if gate_type == "H":
                circuit.append(cirq.H(qubits[targets[0]]))
            elif gate_type == "X":
                circuit.append(cirq.X(qubits[targets[0]]))
            elif gate_type == "CNOT" and len(targets) >= 2:
                circuit.append(cirq.CNOT(qubits[targets[0]], qubits[targets[1]]))
            elif gate_type == "ISWAP" and len(targets) >= 2:
                circuit.append(cirq.ISWAP(qubits[targets[0]], qubits[targets[1]]))

        simulator = cirq.Simulator()
        result = simulator.simulate(circuit)

        # Get state vector amplitudes
        state_vector = result.final_state_vector
        probabilities = np.abs(state_vector) ** 2

        return {
            "circuit": str(circuit),
            "probabilities": probabilities.tolist(),
            "state_labels": [format(i, f'0{num_qubits}b') for i in range(len(probabilities))]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
