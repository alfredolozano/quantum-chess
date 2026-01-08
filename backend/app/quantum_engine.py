"""
Quantum Chess Engine using Cirq

This module implements the quantum mechanics of quantum chess,
including superposition, entanglement, and measurement of chess pieces.
"""

import cirq
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
from dataclasses import dataclass, field
import random


class MoveType(str, Enum):
    """Types of quantum chess moves"""
    STANDARD = "standard"       # Normal classical move
    SPLIT = "split"             # Split piece into superposition
    MERGE = "merge"             # Merge superposed pieces
    CAPTURE = "capture"         # Capture with measurement
    QUANTUM_CAPTURE = "quantum_capture"  # Capture in superposition


class MoveVariant(str, Enum):
    """Variants of moves"""
    BASIC = "basic"
    EXCLUDED = "excluded"       # Move blocked by potential piece
    CAPTURE = "capture"


class PieceType(str, Enum):
    """Chess piece types"""
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


class Color(str, Enum):
    """Player colors"""
    WHITE = "white"
    BLACK = "black"


@dataclass
class ChessPiece:
    """Represents a chess piece"""
    piece_type: PieceType
    color: Color
    id: str  # Unique identifier for tracking


@dataclass
class QuantumMove:
    """Represents a quantum chess move"""
    source: str  # e.g., "e2"
    target1: str  # Primary target
    target2: Optional[str] = None  # Secondary target for split moves
    move_type: MoveType = MoveType.STANDARD
    variant: MoveVariant = MoveVariant.BASIC


@dataclass
class GameState:
    """Complete game state"""
    board: Dict[str, Optional[ChessPiece]]
    probabilities: Dict[str, float]
    turn: Color
    move_history: List[QuantumMove]
    entangled_squares: List[Set[str]]
    superposed_pieces: Dict[str, List[str]]  # piece_id -> list of squares


def square_to_index(square: str) -> int:
    """Convert algebraic notation to index (0-63)"""
    col = ord(square[0].lower()) - ord('a')
    row = int(square[1]) - 1
    return row * 8 + col


def index_to_square(index: int) -> str:
    """Convert index (0-63) to algebraic notation"""
    col = chr(ord('a') + (index % 8))
    row = str((index // 8) + 1)
    return col + row


class QuantumChessEngine:
    """
    Quantum Chess Engine using Cirq

    Implements quantum mechanics for chess including:
    - Superposition of pieces
    - Entanglement between squares
    - Measurement and collapse
    """

    def __init__(self):
        self.qubits = [cirq.LineQubit(i) for i in range(64)]
        self.circuit = cirq.Circuit()
        self.simulator = cirq.Simulator()

        # Classical piece tracking
        self.pieces: Dict[str, ChessPiece] = {}
        self.square_to_piece: Dict[str, Optional[str]] = {}

        # Quantum state tracking
        self.probabilities = np.zeros(64)
        self.superposed_pieces: Dict[str, List[str]] = {}
        self.entangled_groups: List[Set[int]] = []

        # Game state
        self.turn = Color.WHITE
        self.move_history: List[Tuple[QuantumMove, cirq.Circuit]] = []

        self._initialize_board()

    def _initialize_board(self):
        """Initialize the chess board to starting position"""
        self.circuit = cirq.Circuit()

        # Setup initial pieces
        piece_setup = {
            # White pieces
            'a1': ('R', Color.WHITE), 'b1': ('N', Color.WHITE), 'c1': ('B', Color.WHITE),
            'd1': ('Q', Color.WHITE), 'e1': ('K', Color.WHITE), 'f1': ('B', Color.WHITE),
            'g1': ('N', Color.WHITE), 'h1': ('R', Color.WHITE),
            'a2': ('P', Color.WHITE), 'b2': ('P', Color.WHITE), 'c2': ('P', Color.WHITE),
            'd2': ('P', Color.WHITE), 'e2': ('P', Color.WHITE), 'f2': ('P', Color.WHITE),
            'g2': ('P', Color.WHITE), 'h2': ('P', Color.WHITE),
            # Black pieces
            'a8': ('R', Color.BLACK), 'b8': ('N', Color.BLACK), 'c8': ('B', Color.BLACK),
            'd8': ('Q', Color.BLACK), 'e8': ('K', Color.BLACK), 'f8': ('B', Color.BLACK),
            'g8': ('N', Color.BLACK), 'h8': ('R', Color.BLACK),
            'a7': ('P', Color.BLACK), 'b7': ('P', Color.BLACK), 'c7': ('P', Color.BLACK),
            'd7': ('P', Color.BLACK), 'e7': ('P', Color.BLACK), 'f7': ('P', Color.BLACK),
            'g7': ('P', Color.BLACK), 'h7': ('P', Color.BLACK),
        }

        piece_type_map = {
            'P': PieceType.PAWN, 'R': PieceType.ROOK, 'N': PieceType.KNIGHT,
            'B': PieceType.BISHOP, 'Q': PieceType.QUEEN, 'K': PieceType.KING
        }

        # Initialize all squares
        for i in range(64):
            self.square_to_piece[index_to_square(i)] = None
            self.probabilities[i] = 0.0

        # Place pieces
        piece_counter = 0
        for square, (symbol, color) in piece_setup.items():
            piece_id = f"{color.value}_{symbol}_{piece_counter}"
            piece = ChessPiece(
                piece_type=piece_type_map[symbol],
                color=color,
                id=piece_id
            )
            self.pieces[piece_id] = piece
            self.square_to_piece[square] = piece_id
            self.superposed_pieces[piece_id] = [square]

            # Set qubit to |1⟩ for occupied squares
            idx = square_to_index(square)
            self.circuit.append(cirq.X(self.qubits[idx]))
            self.probabilities[idx] = 1.0

            piece_counter += 1

    def reset_board(self):
        """Reset the board to initial state"""
        self.pieces.clear()
        self.square_to_piece.clear()
        self.superposed_pieces.clear()
        self.entangled_groups.clear()
        self.move_history.clear()
        self.turn = Color.WHITE
        self._initialize_board()

    def get_probabilities(self) -> Dict[str, float]:
        """Get occupation probabilities for all squares"""
        return {index_to_square(i): float(self.probabilities[i]) for i in range(64)}

    def get_board_state(self) -> Dict:
        """Get the complete board state for frontend"""
        pieces_on_board = {}
        for square, piece_id in self.square_to_piece.items():
            if piece_id:
                piece = self.pieces[piece_id]
                prob = self.probabilities[square_to_index(square)]
                pieces_on_board[square] = {
                    'piece_type': piece.piece_type.value,
                    'color': piece.color.value,
                    'probability': prob,
                    'is_superposed': len(self.superposed_pieces.get(piece_id, [])) > 1
                }

        return {
            'pieces': pieces_on_board,
            'probabilities': self.get_probabilities(),
            'turn': self.turn.value,
            'entangled_groups': [[index_to_square(i) for i in group] for group in self.entangled_groups],
            'superposed_pieces': {
                pid: squares for pid, squares in self.superposed_pieces.items()
                if len(squares) > 1
            }
        }

    def _apply_iswap(self, q1: int, q2: int):
        """Apply iSWAP gate between two qubits"""
        self.circuit.append(cirq.ISWAP(self.qubits[q1], self.qubits[q2]))

    def _apply_sqrt_iswap(self, q1: int, q2: int):
        """Apply √iSWAP gate for split moves"""
        self.circuit.append(cirq.ISWAP(self.qubits[q1], self.qubits[q2]) ** 0.5)

    def _apply_controlled_iswap(self, control: int, q1: int, q2: int):
        """Apply controlled iSWAP for slide moves"""
        # Controlled iSWAP implementation
        self.circuit.append(
            cirq.ControlledGate(cirq.ISWAP).on(
                self.qubits[control], self.qubits[q1], self.qubits[q2]
            )
        )

    def execute_move(self, move: QuantumMove) -> Dict:
        """Execute a quantum chess move"""
        source_idx = square_to_index(move.source)
        target1_idx = square_to_index(move.target1)
        target2_idx = square_to_index(move.target2) if move.target2 else None

        # Store current circuit for undo
        circuit_before = self.circuit.copy()

        piece_id = self.square_to_piece.get(move.source)
        if not piece_id:
            return {'success': False, 'error': 'No piece at source square'}

        piece = self.pieces[piece_id]
        if piece.color != self.turn:
            return {'success': False, 'error': 'Not your turn'}

        # Validate move based on piece type
        if not self._validate_move(move, piece):
            return {'success': False, 'error': 'Invalid move for this piece'}

        result = {'success': True}

        if move.move_type == MoveType.STANDARD:
            result = self._execute_standard_move(move, piece_id, source_idx, target1_idx)

        elif move.move_type == MoveType.SPLIT:
            if target2_idx is None:
                return {'success': False, 'error': 'Split move requires two targets'}
            result = self._execute_split_move(move, piece_id, source_idx, target1_idx, target2_idx)

        elif move.move_type == MoveType.MERGE:
            result = self._execute_merge_move(move, piece_id, source_idx, target1_idx)

        elif move.move_type == MoveType.CAPTURE:
            result = self._execute_capture_move(move, piece_id, source_idx, target1_idx)

        if result.get('success'):
            self.move_history.append((move, circuit_before))
            self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
            result['board_state'] = self.get_board_state()

        return result

    def _validate_move(self, move: QuantumMove, piece: ChessPiece) -> bool:
        """Validate if a move is legal for the piece type"""
        source_idx = square_to_index(move.source)
        target_idx = square_to_index(move.target1)

        source_col, source_row = source_idx % 8, source_idx // 8
        target_col, target_row = target_idx % 8, target_idx // 8

        dx = abs(target_col - source_col)
        dy = abs(target_row - source_row)

        if piece.piece_type == PieceType.KNIGHT:
            # Knight moves in L-shape
            return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

        elif piece.piece_type == PieceType.ROOK:
            # Rook moves in straight lines
            return dx == 0 or dy == 0

        elif piece.piece_type == PieceType.BISHOP:
            # Bishop moves diagonally
            return dx == dy

        elif piece.piece_type == PieceType.QUEEN:
            # Queen moves like rook or bishop
            return dx == 0 or dy == 0 or dx == dy

        elif piece.piece_type == PieceType.KING:
            # King moves one square any direction
            return dx <= 1 and dy <= 1

        elif piece.piece_type == PieceType.PAWN:
            direction = 1 if piece.color == Color.WHITE else -1
            # Pawn move forward
            if dx == 0:
                if target_row - source_row == direction:
                    return True
                # First move can be two squares
                if (source_row == 1 and piece.color == Color.WHITE) or \
                   (source_row == 6 and piece.color == Color.BLACK):
                    if target_row - source_row == 2 * direction:
                        return True
            # Pawn capture diagonally
            elif dx == 1 and target_row - source_row == direction:
                return True
            return False

        return True

    def _execute_standard_move(self, move: QuantumMove, piece_id: str,
                               source_idx: int, target_idx: int) -> Dict:
        """Execute a standard quantum move using iSWAP"""
        target_square = move.target1
        source_square = move.source

        # Check if target is occupied
        target_piece_id = self.square_to_piece.get(target_square)

        if target_piece_id:
            # Target occupied - this becomes a capture
            return self._execute_capture_move(move, piece_id, source_idx, target_idx)

        # Apply iSWAP gate
        self._apply_iswap(source_idx, target_idx)

        # Update classical tracking
        self.square_to_piece[source_square] = None
        self.square_to_piece[target_square] = piece_id

        # Update superposition tracking
        if piece_id in self.superposed_pieces:
            squares = self.superposed_pieces[piece_id]
            if source_square in squares:
                squares.remove(source_square)
            squares.append(target_square)

        # Update probabilities
        self.probabilities[target_idx] = self.probabilities[source_idx]
        self.probabilities[source_idx] = 0.0

        return {'success': True, 'move_type': 'standard'}

    def _execute_split_move(self, move: QuantumMove, piece_id: str,
                           source_idx: int, target1_idx: int, target2_idx: int) -> Dict:
        """Execute a split move creating superposition"""
        source_square = move.source
        target1_square = move.target1
        target2_square = move.target2

        # Check targets are unoccupied
        for target in [target1_square, target2_square]:
            if self.square_to_piece.get(target):
                return {'success': False, 'error': f'Target square {target} is occupied'}

        # Apply √iSWAP to create superposition with first target
        self._apply_sqrt_iswap(source_idx, target1_idx)

        # Apply iSWAP between source and second target
        self._apply_iswap(source_idx, target2_idx)

        # Update classical tracking - piece now exists in superposition
        self.square_to_piece[source_square] = None
        self.square_to_piece[target1_square] = piece_id
        self.square_to_piece[target2_square] = piece_id

        # Update superposition tracking
        self.superposed_pieces[piece_id] = [target1_square, target2_square]

        # Update probabilities - equal superposition
        original_prob = self.probabilities[source_idx]
        self.probabilities[source_idx] = 0.0
        self.probabilities[target1_idx] = original_prob * 0.5
        self.probabilities[target2_idx] = original_prob * 0.5

        # Add entanglement group
        self.entangled_groups.append({target1_idx, target2_idx})

        return {
            'success': True,
            'move_type': 'split',
            'superposition': [target1_square, target2_square],
            'probabilities': {
                target1_square: self.probabilities[target1_idx],
                target2_square: self.probabilities[target2_idx]
            }
        }

    def _execute_merge_move(self, move: QuantumMove, piece_id: str,
                           source_idx: int, target_idx: int) -> Dict:
        """Execute a merge move collapsing superposition"""
        source_square = move.source
        target_square = move.target1

        # Check if piece is in superposition
        if piece_id not in self.superposed_pieces or \
           len(self.superposed_pieces[piece_id]) < 2:
            return {'success': False, 'error': 'Piece is not in superposition'}

        superposed_squares = self.superposed_pieces[piece_id]

        if source_square not in superposed_squares:
            return {'success': False, 'error': 'Source not in superposition'}

        # Measure to collapse superposition
        result = self._perform_measurement([source_idx])

        if result[source_idx]:
            # Piece was at source, move to target
            self._apply_iswap(source_idx, target_idx)

            # Collapse all other superposition locations
            for sq in superposed_squares:
                if sq != source_square:
                    sq_idx = square_to_index(sq)
                    self.probabilities[sq_idx] = 0.0
                    self.square_to_piece[sq] = None

            self.square_to_piece[source_square] = None
            self.square_to_piece[target_square] = piece_id
            self.superposed_pieces[piece_id] = [target_square]

            self.probabilities[target_idx] = 1.0
            self.probabilities[source_idx] = 0.0

            return {'success': True, 'move_type': 'merge', 'collapsed_to': target_square}
        else:
            # Piece was not at source - find where it collapsed to
            for sq in superposed_squares:
                if sq != source_square:
                    collapsed_square = sq
                    self.superposed_pieces[piece_id] = [sq]
                    self.probabilities[square_to_index(sq)] = 1.0
                    break

            self.square_to_piece[source_square] = None
            self.probabilities[source_idx] = 0.0

            return {
                'success': True,
                'move_type': 'merge_collapsed',
                'collapsed_to': collapsed_square,
                'move_cancelled': True
            }

    def _execute_capture_move(self, move: QuantumMove, piece_id: str,
                             source_idx: int, target_idx: int) -> Dict:
        """Execute a capture move with measurement"""
        target_square = move.target1
        source_square = move.source
        target_piece_id = self.square_to_piece.get(target_square)

        if not target_piece_id:
            # No piece to capture, treat as standard move
            return self._execute_standard_move(move, piece_id, source_idx, target_idx)

        target_piece = self.pieces[target_piece_id]

        # If target is in superposition, measure it
        target_prob = self.probabilities[target_idx]

        if target_prob < 1.0 and target_prob > 0.0:
            # Target in superposition - perform measurement
            measurement_result = random.random() < target_prob

            if measurement_result:
                # Target piece was there - capture it
                self._capture_piece(target_piece_id, target_square)

                # Move our piece
                self._apply_iswap(source_idx, target_idx)
                self.square_to_piece[source_square] = None
                self.square_to_piece[target_square] = piece_id

                self.probabilities[target_idx] = self.probabilities[source_idx]
                self.probabilities[source_idx] = 0.0

                # Update superposition
                if piece_id in self.superposed_pieces:
                    self.superposed_pieces[piece_id] = [target_square]

                return {
                    'success': True,
                    'move_type': 'capture',
                    'captured': target_piece.piece_type.value,
                    'measurement_result': 'captured'
                }
            else:
                # Target piece wasn't there - move without capture
                # But our move might fail if blocked
                return {
                    'success': True,
                    'move_type': 'capture_miss',
                    'measurement_result': 'miss',
                    'message': 'Target was not at the expected position'
                }
        else:
            # Target definitely there - classical capture
            self._capture_piece(target_piece_id, target_square)

            self._apply_iswap(source_idx, target_idx)
            self.square_to_piece[source_square] = None
            self.square_to_piece[target_square] = piece_id

            self.probabilities[target_idx] = self.probabilities[source_idx]
            self.probabilities[source_idx] = 0.0

            if piece_id in self.superposed_pieces:
                self.superposed_pieces[piece_id] = [target_square]

            return {
                'success': True,
                'move_type': 'capture',
                'captured': target_piece.piece_type.value
            }

    def _capture_piece(self, piece_id: str, square: str):
        """Remove a captured piece from the game"""
        piece = self.pieces.get(piece_id)

        # Remove from all superposition locations
        if piece_id in self.superposed_pieces:
            for sq in self.superposed_pieces[piece_id]:
                if self.square_to_piece.get(sq) == piece_id:
                    self.square_to_piece[sq] = None
                self.probabilities[square_to_index(sq)] = 0.0
            del self.superposed_pieces[piece_id]
        else:
            self.square_to_piece[square] = None
            self.probabilities[square_to_index(square)] = 0.0

        # Don't delete the piece from self.pieces - keep for history

    def _perform_measurement(self, qubit_indices: List[int]) -> Dict[int, bool]:
        """Perform measurement on specified qubits"""
        results = {}
        for idx in qubit_indices:
            prob = self.probabilities[idx]
            results[idx] = random.random() < prob
        return results

    def undo_last_move(self) -> Dict:
        """Undo the last move"""
        if not self.move_history:
            return {'success': False, 'error': 'No moves to undo'}

        move, circuit_before = self.move_history.pop()
        self.circuit = circuit_before

        # Recalculate board state
        # This is a simplified undo - full implementation would restore complete state
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK

        return {
            'success': True,
            'undone_move': {
                'source': move.source,
                'target1': move.target1,
                'target2': move.target2,
                'move_type': move.move_type.value
            }
        }

    def get_legal_moves(self, square: str) -> List[Dict]:
        """Get all legal moves for a piece at a given square"""
        piece_id = self.square_to_piece.get(square)
        if not piece_id:
            return []

        piece = self.pieces[piece_id]
        moves = []

        source_idx = square_to_index(square)

        for target_idx in range(64):
            target_square = index_to_square(target_idx)
            if target_square == square:
                continue

            test_move = QuantumMove(
                source=square,
                target1=target_square,
                move_type=MoveType.STANDARD
            )

            if self._validate_move(test_move, piece):
                target_piece_id = self.square_to_piece.get(target_square)
                move_info = {
                    'target': target_square,
                    'move_type': 'standard'
                }

                if target_piece_id:
                    target_piece = self.pieces[target_piece_id]
                    if target_piece.color != piece.color:
                        move_info['move_type'] = 'capture'
                        move_info['can_capture'] = True
                    else:
                        continue  # Can't capture own piece

                moves.append(move_info)

        # Add split move possibilities for knights, bishops, rooks, queens
        if piece.piece_type in [PieceType.KNIGHT, PieceType.BISHOP,
                                 PieceType.ROOK, PieceType.QUEEN]:
            standard_targets = [m['target'] for m in moves if m['move_type'] == 'standard']
            for i, t1 in enumerate(standard_targets):
                for t2 in standard_targets[i+1:]:
                    moves.append({
                        'target': t1,
                        'target2': t2,
                        'move_type': 'split'
                    })

        return moves

    def is_game_over(self) -> Optional[Dict]:
        """Check if the game is over (king captured)"""
        white_king_exists = False
        black_king_exists = False

        for piece_id, squares in self.superposed_pieces.items():
            piece = self.pieces.get(piece_id)
            if piece and piece.piece_type == PieceType.KING:
                # Check if king has non-zero probability
                for sq in squares:
                    if self.probabilities[square_to_index(sq)] > 0:
                        if piece.color == Color.WHITE:
                            white_king_exists = True
                        else:
                            black_king_exists = True

        if not white_king_exists:
            return {'game_over': True, 'winner': 'black', 'reason': 'White king captured'}
        if not black_king_exists:
            return {'game_over': True, 'winner': 'white', 'reason': 'Black king captured'}

        return None


class QuantumChessGame:
    """
    High-level game manager for quantum chess
    """

    def __init__(self, game_id: str):
        self.game_id = game_id
        self.engine = QuantumChessEngine()
        self.players: Dict[Color, Optional[str]] = {
            Color.WHITE: None,
            Color.BLACK: None
        }
        self.spectators: List[str] = []
        self.created_at = None
        self.started = False
        self.ended = False

    def add_player(self, player_id: str, color: Optional[Color] = None) -> Dict:
        """Add a player to the game"""
        if color:
            if self.players[color]:
                return {'success': False, 'error': f'{color.value} already taken'}
            self.players[color] = player_id
        else:
            # Auto-assign color
            if not self.players[Color.WHITE]:
                self.players[Color.WHITE] = player_id
                color = Color.WHITE
            elif not self.players[Color.BLACK]:
                self.players[Color.BLACK] = player_id
                color = Color.BLACK
            else:
                return {'success': False, 'error': 'Game is full'}

        return {'success': True, 'color': color.value}

    def start_game(self) -> Dict:
        """Start the game"""
        if not self.players[Color.WHITE] or not self.players[Color.BLACK]:
            return {'success': False, 'error': 'Need two players to start'}

        self.started = True
        self.engine.reset_board()

        return {
            'success': True,
            'board_state': self.engine.get_board_state()
        }

    def make_move(self, player_id: str, move: QuantumMove) -> Dict:
        """Make a move for a player"""
        if not self.started:
            return {'success': False, 'error': 'Game not started'}

        if self.ended:
            return {'success': False, 'error': 'Game already ended'}

        current_color = self.engine.turn
        if self.players[current_color] != player_id:
            return {'success': False, 'error': 'Not your turn'}

        result = self.engine.execute_move(move)

        if result.get('success'):
            game_over = self.engine.is_game_over()
            if game_over:
                self.ended = True
                result['game_over'] = game_over

        return result

    def get_state(self) -> Dict:
        """Get the current game state"""
        return {
            'game_id': self.game_id,
            'players': {
                'white': self.players[Color.WHITE],
                'black': self.players[Color.BLACK]
            },
            'started': self.started,
            'ended': self.ended,
            'board_state': self.engine.get_board_state() if self.started else None
        }
