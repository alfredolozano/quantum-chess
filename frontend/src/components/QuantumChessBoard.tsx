import { useState, useCallback, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import clsx from 'clsx'

interface Piece {
  piece_type: string
  color: 'white' | 'black'
  probability: number
  is_superposed: boolean
}

interface BoardState {
  pieces: Record<string, Piece>
  probabilities: Record<string, number>
  turn: 'white' | 'black'
  entangled_groups: string[][]
  superposed_pieces: Record<string, string[]>
}

interface Move {
  target: string
  move_type: string
  target2?: string
  can_capture?: boolean
}

interface QuantumChessBoardProps {
  boardState: BoardState | null
  playerColor: 'white' | 'black'
  onMove: (move: {
    source: string
    target1: string
    target2?: string
    move_type: string
  }) => void
  isMyTurn: boolean
  legalMoves: Move[]
  onRequestLegalMoves: (square: string) => void
}

// Chess piece Unicode symbols
const pieceSymbols: Record<string, Record<string, string>> = {
  white: {
    king: '♔',
    queen: '♕',
    rook: '♖',
    bishop: '♗',
    knight: '♘',
    pawn: '♙',
  },
  black: {
    king: '♚',
    queen: '♛',
    rook: '♜',
    bishop: '♝',
    knight: '♞',
    pawn: '♟',
  },
}

// Convert algebraic notation to board position
const squareToPosition = (square: string): { row: number; col: number } => {
  const col = square.charCodeAt(0) - 'a'.charCodeAt(0)
  const row = parseInt(square[1]) - 1
  return { row, col }
}

// Convert position to algebraic notation
const positionToSquare = (row: number, col: number): string => {
  return String.fromCharCode('a'.charCodeAt(0) + col) + (row + 1)
}

export function QuantumChessBoard({
  boardState,
  playerColor,
  onMove,
  isMyTurn,
  legalMoves,
  onRequestLegalMoves,
}: QuantumChessBoardProps) {
  const [selectedSquare, setSelectedSquare] = useState<string | null>(null)
  const [splitTargets, setSplitTargets] = useState<string[]>([])
  const [isSplitMode, setIsSplitMode] = useState(false)
  const [hoveredSquare, setHoveredSquare] = useState<string | null>(null)

  // Generate board squares
  const squares = useMemo(() => {
    const result = []
    // Reverse row order if playing as black
    const rows = playerColor === 'white'
      ? [7, 6, 5, 4, 3, 2, 1, 0]
      : [0, 1, 2, 3, 4, 5, 6, 7]
    const cols = playerColor === 'white'
      ? [0, 1, 2, 3, 4, 5, 6, 7]
      : [7, 6, 5, 4, 3, 2, 1, 0]

    for (const row of rows) {
      for (const col of cols) {
        result.push({ row, col, square: positionToSquare(row, col) })
      }
    }
    return result
  }, [playerColor])

  // Get legal move targets for highlighting
  const legalMoveTargets = useMemo(() => {
    return new Set(legalMoves.map(m => m.target))
  }, [legalMoves])

  // Get split move targets
  const splitMoveTargets = useMemo(() => {
    return legalMoves
      .filter(m => m.move_type === 'split')
      .map(m => ({ target: m.target, target2: m.target2 }))
  }, [legalMoves])

  // Handle square click
  const handleSquareClick = useCallback((square: string) => {
    if (!isMyTurn) return

    const piece = boardState?.pieces[square]

    // If in split mode, collect targets
    if (isSplitMode && selectedSquare) {
      if (legalMoveTargets.has(square)) {
        const newTargets = [...splitTargets, square]

        if (newTargets.length === 2) {
          // Execute split move
          onMove({
            source: selectedSquare,
            target1: newTargets[0],
            target2: newTargets[1],
            move_type: 'split',
          })
          setSelectedSquare(null)
          setSplitTargets([])
          setIsSplitMode(false)
        } else {
          setSplitTargets(newTargets)
        }
      } else {
        // Cancel split mode
        setIsSplitMode(false)
        setSplitTargets([])
        setSelectedSquare(null)
      }
      return
    }

    // If a piece is already selected
    if (selectedSquare) {
      if (square === selectedSquare) {
        // Deselect
        setSelectedSquare(null)
        return
      }

      if (legalMoveTargets.has(square)) {
        // Make move
        onMove({
          source: selectedSquare,
          target1: square,
          move_type: piece ? 'capture' : 'standard',
        })
        setSelectedSquare(null)
      } else {
        // Select new piece if it's ours
        if (piece && piece.color === playerColor) {
          setSelectedSquare(square)
          onRequestLegalMoves(square)
        } else {
          setSelectedSquare(null)
        }
      }
    } else {
      // Select a piece
      if (piece && piece.color === playerColor) {
        setSelectedSquare(square)
        onRequestLegalMoves(square)
      }
    }
  }, [isMyTurn, selectedSquare, splitTargets, isSplitMode, boardState, playerColor, legalMoveTargets, onMove, onRequestLegalMoves])

  // Handle right-click for split mode
  const handleRightClick = useCallback((e: React.MouseEvent, square: string) => {
    e.preventDefault()

    if (!isMyTurn || !selectedSquare) return

    const piece = boardState?.pieces[selectedSquare]
    if (!piece) return

    // Check if piece can split (not pawn or king)
    if (['pawn', 'king'].includes(piece.piece_type)) return

    // Enter split mode
    setIsSplitMode(true)
    setSplitTargets([])
  }, [isMyTurn, selectedSquare, boardState])

  // Check if square is in an entangled group
  const getEntanglementGroup = useCallback((square: string): string[] | null => {
    if (!boardState?.entangled_groups) return null

    for (const group of boardState.entangled_groups) {
      if (group.includes(square)) {
        return group
      }
    }
    return null
  }, [boardState])

  return (
    <div className="relative">
      {/* Board Container */}
      <div className="relative bg-slate-800 p-4 rounded-xl shadow-2xl">
        {/* Coordinate labels */}
        <div className="absolute -left-6 top-4 bottom-4 flex flex-col justify-around text-slate-500 text-sm">
          {(playerColor === 'white' ? [8, 7, 6, 5, 4, 3, 2, 1] : [1, 2, 3, 4, 5, 6, 7, 8]).map(n => (
            <span key={n}>{n}</span>
          ))}
        </div>
        <div className="absolute -bottom-6 left-4 right-4 flex justify-around text-slate-500 text-sm">
          {(playerColor === 'white' ? ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] : ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']).map(l => (
            <span key={l}>{l}</span>
          ))}
        </div>

        {/* Chess Board */}
        <div
          className="grid grid-cols-8 gap-0 rounded-lg overflow-hidden"
          style={{ width: '480px', height: '480px' }}
        >
          {squares.map(({ row, col, square }) => {
            const isLight = (row + col) % 2 === 1
            const piece = boardState?.pieces[square]
            const probability = boardState?.probabilities[square] || 0
            const isSelected = selectedSquare === square
            const isLegalMove = legalMoveTargets.has(square)
            const isSplitTarget = splitTargets.includes(square)
            const entanglementGroup = getEntanglementGroup(square)
            const isHovered = hoveredSquare === square

            return (
              <div
                key={square}
                onClick={() => handleSquareClick(square)}
                onContextMenu={(e) => handleRightClick(e, square)}
                onMouseEnter={() => setHoveredSquare(square)}
                onMouseLeave={() => setHoveredSquare(null)}
                className={clsx(
                  'relative w-[60px] h-[60px] flex items-center justify-center cursor-pointer transition-colors',
                  isLight ? 'bg-board-light' : 'bg-board-dark',
                  isSelected && 'ring-4 ring-inset ring-quantum-primary',
                  isSplitTarget && 'ring-4 ring-inset ring-quantum-secondary',
                )}
              >
                {/* Legal move indicator */}
                {isLegalMove && !piece && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute w-4 h-4 rounded-full bg-quantum-primary/50"
                  />
                )}

                {/* Capture indicator */}
                {isLegalMove && piece && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute inset-1 rounded-full border-4 border-quantum-primary/50"
                  />
                )}

                {/* Entanglement indicator */}
                {entanglementGroup && piece?.is_superposed && (
                  <div className="absolute inset-0 border-2 border-quantum-secondary animate-pulse" />
                )}

                {/* Piece */}
                <AnimatePresence mode="wait">
                  {piece && (
                    <motion.div
                      key={`${square}-${piece.piece_type}-${piece.color}`}
                      initial={{ scale: 0.5, opacity: 0 }}
                      animate={{
                        scale: 1,
                        opacity: piece.probability,
                      }}
                      exit={{ scale: 0.5, opacity: 0 }}
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                      className={clsx(
                        'chess-piece text-5xl select-none relative',
                        piece.is_superposed && 'animate-superposition',
                        isHovered && 'transform scale-110',
                      )}
                      style={{
                        textShadow: piece.color === 'white'
                          ? '0 2px 4px rgba(0,0,0,0.5)'
                          : '0 2px 4px rgba(0,0,0,0.8)',
                        filter: piece.is_superposed
                          ? 'drop-shadow(0 0 8px rgba(139, 92, 246, 0.6))'
                          : undefined,
                      }}
                    >
                      {pieceSymbols[piece.color][piece.piece_type]}

                      {/* Probability indicator */}
                      {piece.probability < 1 && (
                        <span className="probability-overlay">
                          {Math.round(piece.probability * 100)}%
                        </span>
                      )}

                      {/* Superposition glow */}
                      {piece.is_superposed && (
                        <div className="absolute inset-0 rounded-full bg-quantum-secondary/20 animate-quantum-glow blur-md" />
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )
          })}
        </div>

        {/* Split mode indicator */}
        {isSplitMode && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="absolute -bottom-16 left-0 right-0 text-center"
          >
            <span className="bg-quantum-secondary/20 text-quantum-secondary px-4 py-2 rounded-lg text-sm">
              Split Mode: Select two target squares ({splitTargets.length}/2)
            </span>
          </motion.div>
        )}
      </div>

      {/* Turn Indicator */}
      <div className="mt-6 text-center">
        <span className={clsx(
          'px-4 py-2 rounded-lg font-medium',
          boardState?.turn === playerColor
            ? 'bg-quantum-primary/20 text-quantum-primary'
            : 'bg-slate-700 text-slate-400'
        )}>
          {boardState?.turn === playerColor ? 'Your Turn' : "Opponent's Turn"}
        </span>
      </div>

      {/* Controls */}
      <div className="mt-4 flex justify-center gap-4 text-sm text-slate-400">
        <span>Click to move</span>
        <span>•</span>
        <span>Right-click for split move</span>
      </div>
    </div>
  )
}
