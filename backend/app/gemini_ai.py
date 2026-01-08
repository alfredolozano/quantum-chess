"""
Gemini AI Integration for Quantum Chess

Uses Google's Gemini 2.0 Flash model to play quantum chess.
"""

import json
import random
from typing import Dict, List, Optional
import httpx
import os

from .quantum_engine import (
    QuantumChessEngine, QuantumMove, MoveType,
    Color, PieceType, square_to_index, index_to_square
)


GEMINI_SYSTEM_PROMPT = """You are an expert Quantum Chess player. Quantum Chess is a variant of chess that incorporates quantum mechanics concepts:

## Quantum Chess Rules:

1. **Standard Moves**: Work like regular chess but use iSWAP gates internally.

2. **Split Moves**: A piece can split into a superposition across two squares. Both locations have 50% probability. Only Knights, Bishops, Rooks, and Queens can split.

3. **Merge Moves**: A piece in superposition can attempt to merge back to a single location through measurement.

4. **Capture Moves**: When capturing a piece in superposition, measurement occurs:
   - If the target piece is there (based on probability), it's captured
   - If not, the capture may fail

5. **Entanglement**: Split pieces become entangled. Measuring one affects the other.

## Strategy Tips:
- Use splits to create uncertainty and control multiple areas
- Be careful with splits near the king - measurement can be unpredictable
- Use superposition to threaten multiple pieces simultaneously
- Remember pieces in superposition have reduced "presence" (50% each location)

## Your Task:
Analyze the board state and suggest the best move. Consider:
- Material advantage
- King safety
- Piece activity
- Quantum tactical opportunities

Respond with a JSON object containing:
{
    "reasoning": "Your analysis of the position",
    "move": {
        "source": "e2",
        "target1": "e4",
        "target2": null,  // Only for split moves
        "move_type": "standard"  // standard, split, merge, or capture
    },
    "confidence": 0.8  // Your confidence in this move (0-1)
}
"""


class GeminiChessAI:
    """
    AI opponent using Gemini 2.0 Flash
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = "gemini-2.0-flash-exp"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.difficulty = "medium"  # easy, medium, hard

    async def get_move(self, engine: QuantumChessEngine, game_history: List[Dict] = None) -> Dict:
        """Get the AI's move for the current position"""

        if not self.api_key:
            # Fallback to random valid move if no API key
            return self._get_random_move(engine)

        board_state = engine.get_board_state()
        prompt = self._create_prompt(board_state, game_history)

        try:
            response = await self._call_gemini(prompt)
            move_data = self._parse_response(response)

            if move_data and self._validate_ai_move(engine, move_data):
                return move_data
            else:
                # Fallback to random move if AI response is invalid
                return self._get_random_move(engine)

        except Exception as e:
            print(f"Gemini AI error: {e}")
            return self._get_random_move(engine)

    def _create_prompt(self, board_state: Dict, game_history: List[Dict] = None) -> str:
        """Create the prompt for Gemini"""

        # Format board as text
        board_text = self._format_board_text(board_state)

        history_text = ""
        if game_history:
            history_text = "\n\nRecent moves:\n"
            for move in game_history[-10:]:  # Last 10 moves
                history_text += f"- {move.get('source')} -> {move.get('target1')}"
                if move.get('target2'):
                    history_text += f" / {move.get('target2')} (split)"
                history_text += "\n"

        superposition_text = ""
        if board_state.get('superposed_pieces'):
            superposition_text = "\n\nPieces in superposition:\n"
            for piece_id, squares in board_state['superposed_pieces'].items():
                superposition_text += f"- {piece_id}: {', '.join(squares)}\n"

        prompt = f"""Current position:
{board_text}

Turn: {board_state['turn'].upper()}
{history_text}
{superposition_text}

What is the best move? Analyze the position and provide your move in JSON format."""

        return prompt

    def _format_board_text(self, board_state: Dict) -> str:
        """Format the board as ASCII text"""
        pieces = board_state.get('pieces', {})
        probabilities = board_state.get('probabilities', {})

        piece_symbols = {
            ('pawn', 'white'): '♙', ('pawn', 'black'): '♟',
            ('rook', 'white'): '♖', ('rook', 'black'): '♜',
            ('knight', 'white'): '♘', ('knight', 'black'): '♞',
            ('bishop', 'white'): '♗', ('bishop', 'black'): '♝',
            ('queen', 'white'): '♕', ('queen', 'black'): '♛',
            ('king', 'white'): '♔', ('king', 'black'): '♚',
        }

        board_lines = []
        board_lines.append("  a b c d e f g h")
        board_lines.append("  ----------------")

        for row in range(7, -1, -1):
            line = f"{row + 1}|"
            for col in range(8):
                square = chr(ord('a') + col) + str(row + 1)
                if square in pieces:
                    piece = pieces[square]
                    symbol = piece_symbols.get(
                        (piece['piece_type'], piece['color']), '?'
                    )
                    prob = piece.get('probability', 1.0)
                    if prob < 1.0:
                        symbol = f"{symbol}~"  # Indicate superposition
                    else:
                        symbol = f"{symbol} "
                else:
                    symbol = ". "
                line += symbol
            line += f"|{row + 1}"
            board_lines.append(line)

        board_lines.append("  ----------------")
        board_lines.append("  a b c d e f g h")

        return "\n".join(board_lines)

    async def _call_gemini(self, prompt: str) -> str:
        """Call the Gemini API"""

        url = f"{self.base_url}/models/{self.model}:generateContent"

        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": GEMINI_SYSTEM_PROMPT + "\n\n" + prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7 if self.difficulty == "medium" else (0.3 if self.difficulty == "hard" else 0.9),
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 1024,
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()

            # Extract text from response
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    return candidate['content']['parts'][0].get('text', '')

            return ""

    def _parse_response(self, response: str) -> Optional[Dict]:
        """Parse Gemini's response to extract the move"""
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1

            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)

                move_data = data.get('move', {})

                return {
                    'source': move_data.get('source'),
                    'target1': move_data.get('target1'),
                    'target2': move_data.get('target2'),
                    'move_type': move_data.get('move_type', 'standard'),
                    'reasoning': data.get('reasoning', ''),
                    'confidence': data.get('confidence', 0.5)
                }
        except json.JSONDecodeError:
            pass

        return None

    def _validate_ai_move(self, engine: QuantumChessEngine, move_data: Dict) -> bool:
        """Validate that the AI's move is legal"""
        if not move_data.get('source') or not move_data.get('target1'):
            return False

        source = move_data['source']
        target = move_data['target1']

        # Check source has a piece of the correct color
        piece_id = engine.square_to_piece.get(source)
        if not piece_id:
            return False

        piece = engine.pieces.get(piece_id)
        if not piece or piece.color != engine.turn:
            return False

        # Get legal moves and check if this move is among them
        legal_moves = engine.get_legal_moves(source)

        for move in legal_moves:
            if move['target'] == target:
                if move_data.get('move_type') == 'split':
                    if move.get('target2') == move_data.get('target2'):
                        return True
                else:
                    return True

        return False

    def _get_random_move(self, engine: QuantumChessEngine) -> Dict:
        """Get a random legal move (fallback)"""
        all_moves = []

        # Find all pieces of the current turn
        for square, piece_id in engine.square_to_piece.items():
            if not piece_id:
                continue

            piece = engine.pieces.get(piece_id)
            if not piece or piece.color != engine.turn:
                continue

            moves = engine.get_legal_moves(square)
            for move in moves:
                move['source'] = square
                all_moves.append(move)

        if not all_moves:
            return None

        # Weight moves based on difficulty
        if self.difficulty == "hard":
            # Prefer captures and splits
            weighted_moves = []
            for move in all_moves:
                weight = 1
                if move.get('can_capture'):
                    weight = 5
                if move.get('move_type') == 'split':
                    weight = 3
                weighted_moves.extend([move] * weight)
            chosen_move = random.choice(weighted_moves)
        else:
            chosen_move = random.choice(all_moves)

        return {
            'source': chosen_move['source'],
            'target1': chosen_move['target'],
            'target2': chosen_move.get('target2'),
            'move_type': chosen_move.get('move_type', 'standard'),
            'reasoning': 'Random move (AI fallback)',
            'confidence': 0.5
        }

    def set_difficulty(self, difficulty: str):
        """Set AI difficulty level"""
        if difficulty in ['easy', 'medium', 'hard']:
            self.difficulty = difficulty


class QuantumChessAIGame:
    """
    Manages a game against the AI
    """

    def __init__(self, game_id: str, player_color: Color = Color.WHITE,
                 api_key: Optional[str] = None, difficulty: str = "medium"):
        self.game_id = game_id
        self.engine = QuantumChessEngine()
        self.ai = GeminiChessAI(api_key)
        self.ai.set_difficulty(difficulty)
        self.player_color = player_color
        self.ai_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
        self.move_history: List[Dict] = []
        self.started = False
        self.ended = False

    def start_game(self) -> Dict:
        """Start the game"""
        self.started = True
        self.engine.reset_board()

        result = {
            'success': True,
            'board_state': self.engine.get_board_state(),
            'player_color': self.player_color.value,
            'ai_color': self.ai_color.value
        }

        # If AI plays white, make first move
        if self.ai_color == Color.WHITE:
            result['ai_thinking'] = True

        return result

    async def player_move(self, move: QuantumMove) -> Dict:
        """Process player's move and get AI response"""
        if not self.started:
            return {'success': False, 'error': 'Game not started'}

        if self.ended:
            return {'success': False, 'error': 'Game already ended'}

        if self.engine.turn != self.player_color:
            return {'success': False, 'error': 'Not your turn'}

        # Execute player's move
        result = self.engine.execute_move(move)

        if not result.get('success'):
            return result

        self.move_history.append({
            'source': move.source,
            'target1': move.target1,
            'target2': move.target2,
            'move_type': move.move_type.value,
            'player': 'human'
        })

        # Check for game over
        game_over = self.engine.is_game_over()
        if game_over:
            self.ended = True
            result['game_over'] = game_over
            return result

        # Get AI's move
        ai_move_data = await self.ai.get_move(self.engine, self.move_history)

        if ai_move_data:
            ai_move = QuantumMove(
                source=ai_move_data['source'],
                target1=ai_move_data['target1'],
                target2=ai_move_data.get('target2'),
                move_type=MoveType(ai_move_data.get('move_type', 'standard'))
            )

            ai_result = self.engine.execute_move(ai_move)

            if ai_result.get('success'):
                self.move_history.append({
                    'source': ai_move.source,
                    'target1': ai_move.target1,
                    'target2': ai_move.target2,
                    'move_type': ai_move.move_type.value,
                    'player': 'ai',
                    'reasoning': ai_move_data.get('reasoning', '')
                })

                result['ai_move'] = ai_move_data
                result['board_state'] = self.engine.get_board_state()

                # Check for game over after AI move
                game_over = self.engine.is_game_over()
                if game_over:
                    self.ended = True
                    result['game_over'] = game_over

        return result

    async def get_ai_first_move(self) -> Dict:
        """Get AI's first move if it plays white"""
        if self.ai_color != Color.WHITE:
            return {'success': False, 'error': 'AI does not play first'}

        ai_move_data = await self.ai.get_move(self.engine, self.move_history)

        if ai_move_data:
            ai_move = QuantumMove(
                source=ai_move_data['source'],
                target1=ai_move_data['target1'],
                target2=ai_move_data.get('target2'),
                move_type=MoveType(ai_move_data.get('move_type', 'standard'))
            )

            result = self.engine.execute_move(ai_move)

            if result.get('success'):
                self.move_history.append({
                    'source': ai_move.source,
                    'target1': ai_move.target1,
                    'target2': ai_move.target2,
                    'move_type': ai_move.move_type.value,
                    'player': 'ai',
                    'reasoning': ai_move_data.get('reasoning', '')
                })

                return {
                    'success': True,
                    'ai_move': ai_move_data,
                    'board_state': self.engine.get_board_state()
                }

        return {'success': False, 'error': 'AI could not generate move'}

    def get_state(self) -> Dict:
        """Get current game state"""
        return {
            'game_id': self.game_id,
            'player_color': self.player_color.value,
            'ai_color': self.ai_color.value,
            'started': self.started,
            'ended': self.ended,
            'board_state': self.engine.get_board_state() if self.started else None,
            'move_history': self.move_history,
            'current_turn': self.engine.turn.value
        }
