# Quantum Chess

A beautiful online quantum chess game that brings quantum mechanics to the classic game of chess. Experience superposition, entanglement, and measurement in this revolutionary chess variant.

![Quantum Chess](frontend/public/quantum-chess.svg)

## Features

### Game Modes
- **Play vs Human**: Challenge friends or other players online with real-time multiplayer
- **Play vs Gemini AI**: Test your skills against Google's Gemini 2.0 Flash AI with adjustable difficulty

### Quantum Mechanics
- **Superposition**: Split your pieces to exist in two places at once using √iSWAP gates
- **Entanglement**: Pieces become mysteriously connected through quantum operations
- **Measurement**: Captures trigger measurement, collapsing superposition probabilistically

### Learning Path
- Comprehensive interactive tutorials on quantum computing fundamentals
- Learn about qubits, superposition, entanglement, and measurement
- Understand quantum gates (H, X, Z, iSWAP)
- Master quantum chess rules and advanced strategies
- Introduction to Google's Cirq framework

## Technology Stack

### Backend
- **Python 3.11+**
- **FastAPI**: Modern async web framework
- **Cirq**: Google's quantum computing framework for quantum simulation
- **WebSockets**: Real-time game communication
- **Google Generative AI**: Gemini 2.0 Flash for AI opponent

### Frontend
- **React 18** with TypeScript
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **React Router**: Client-side routing

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional for AI)
export GEMINI_API_KEY=your_api_key_here

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The application will be available at `http://localhost:3000`

## Quantum Chess Rules

### Standard Moves
Pieces move according to normal chess rules, but the underlying quantum state uses iSWAP gates for movement.

### Split Moves
Knights, Bishops, Rooks, and Queens can split into superposition:
1. Select your piece
2. Right-click to enter split mode
3. Choose two valid destination squares
4. The piece exists at both locations with 50% probability each

### Capture & Measurement
When you attempt to capture a piece in superposition:
- Measurement occurs based on probability
- If the piece is there: Capture succeeds
- If the piece isn't there: The capture "misses"

### Entanglement
Split pieces become entangled. Measuring one position affects all entangled positions, potentially cascading across the board.

## API Endpoints

### REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/games` | GET | List active games |
| `/api/games` | POST | Create a new game |
| `/api/games/{id}` | GET | Get game state |
| `/api/games/{id}/join` | POST | Join a game |
| `/api/games/{id}/start` | POST | Start a game |
| `/api/games/{id}/move` | POST | Make a move |
| `/api/games/{id}/legal-moves/{square}` | GET | Get legal moves |
| `/api/learning/modules` | GET | Get learning modules |
| `/api/quantum/simulate` | POST | Simulate quantum circuit |

### WebSocket

Connect to `/ws/{game_id}/{player_id}` for real-time game updates.

Message types:
- `move`: Make a move
- `get_legal_moves`: Request legal moves
- `chat`: Send chat message
- `resign`: Resign the game

## Project Structure

```
quantum-chess/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── quantum_engine.py    # Quantum chess engine (Cirq)
│   │   ├── gemini_ai.py         # Gemini AI integration
│   │   └── learning_content.py  # Learning path content
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── quantum-chess.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   └── QuantumChessBoard.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── PlayPage.tsx
│   │   │   ├── GamePage.tsx
│   │   │   ├── LobbyPage.tsx
│   │   │   ├── LearnPage.tsx
│   │   │   └── LessonPage.tsx
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
└── README.md
```

## Quantum Computing Concepts

### Qubits
Each chess square is represented by a qubit:
- |0⟩ = Empty square
- |1⟩ = Occupied square
- Superposition allows both states simultaneously

### Gates Used
- **iSWAP**: Standard piece movement
- **√iSWAP**: Creates superposition (split moves)
- **Controlled-iSWAP**: Slide moves through potential blockers

### Measurement
Probabilities are calculated from quantum amplitudes. Measurement collapses the superposition to a definite state.

## Contributing

We welcome contributions! Please feel free to submit pull requests.

## Resources

- [Cirq Documentation](https://quantumai.google/cirq)
- [Unitary Library](https://github.com/quantumlib/unitary)
- [Quantum Chess Concepts](https://github.com/quantumlib/unitary/tree/main/docs/quantum_chess)

## License

MIT License - see LICENSE file for details.

---

Built with Cirq and Google AI
