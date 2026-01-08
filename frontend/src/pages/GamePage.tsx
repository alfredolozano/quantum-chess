import { useState, useEffect, useRef, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { QuantumChessBoard } from '../components/QuantumChessBoard'
import { MessageSquare, Send, Flag, RotateCcw, Copy, Check, Bot, User, Sparkles } from 'lucide-react'

interface GameState {
  game_id: string
  started: boolean
  ended: boolean
  board_state: {
    pieces: Record<string, {
      piece_type: string
      color: 'white' | 'black'
      probability: number
      is_superposed: boolean
    }>
    probabilities: Record<string, number>
    turn: 'white' | 'black'
    entangled_groups: string[][]
    superposed_pieces: Record<string, string[]>
  } | null
  players?: {
    white: string | null
    black: string | null
  }
  player_color?: string
  ai_color?: string
  move_history?: Array<{
    source: string
    target1: string
    target2?: string
    move_type: string
    player: string
    reasoning?: string
  }>
}

interface ChatMessage {
  id: string
  player_id: string
  message: string
  timestamp: Date
}

interface LegalMove {
  target: string
  move_type: string
  target2?: string
  can_capture?: boolean
}

export function GamePage() {
  const { gameId } = useParams()
  const navigate = useNavigate()

  const [gameState, setGameState] = useState<GameState | null>(null)
  const [playerColor, setPlayerColor] = useState<'white' | 'black'>('white')
  const [playerId, setPlayerId] = useState<string>('')
  const [legalMoves, setLegalMoves] = useState<LegalMove[]>([])
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([])
  const [chatInput, setChatInput] = useState('')
  const [isConnected, setIsConnected] = useState(false)
  const [copied, setCopied] = useState(false)
  const [aiThinking, setAiThinking] = useState(false)
  const [aiReasoning, setAiReasoning] = useState<string>('')

  const wsRef = useRef<WebSocket | null>(null)
  const chatEndRef = useRef<HTMLDivElement>(null)

  // Initialize game
  useEffect(() => {
    const storedPlayerId = sessionStorage.getItem('playerId') || ''
    const storedColor = sessionStorage.getItem('playerColor')

    setPlayerId(storedPlayerId)

    // Initialize game
    initializeGame(storedPlayerId, storedColor)

    return () => {
      wsRef.current?.close()
    }
  }, [gameId])

  // Scroll chat to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  const initializeGame = async (pid: string, storedColor: string | null) => {
    try {
      // Fetch game state first
      const response = await fetch(`/api/games/${gameId}`)
      const data = await response.json()

      // Set player color - API response takes precedence
      const color = data.player_color || storedColor || 'white'
      setPlayerColor(color as 'white' | 'black')

      // For AI games, auto-start if not started
      if (data.ai_color && !data.started) {
        const startResponse = await fetch(`/api/games/${gameId}/start`, { method: 'POST' })
        const startData = await startResponse.json()

        if (startData.success) {
          setGameState({
            ...data,
            started: true,
            board_state: startData.board_state,
            player_color: startData.player_color || data.player_color
          })

          if (startData.player_color) {
            setPlayerColor(startData.player_color as 'white' | 'black')
          }
        } else {
          setGameState(data)
        }
      } else {
        setGameState(data)
      }

      // Connect WebSocket after state is set
      connectWebSocket(pid)
    } catch (error) {
      console.error('Failed to initialize game:', error)
    }
  }

  const fetchGameState = async () => {
    try {
      const response = await fetch(`/api/games/${gameId}`)
      const data = await response.json()
      setGameState(data)

      if (data.player_color) {
        setPlayerColor(data.player_color as 'white' | 'black')
      }
    } catch (error) {
      console.error('Failed to fetch game state:', error)
    }
  }

  const connectWebSocket = (pid: string) => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/ws/${gameId}/${pid}`

    const ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      setIsConnected(true)
      console.log('WebSocket connected')
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handleWebSocketMessage(data)
    }

    ws.onclose = () => {
      setIsConnected(false)
      console.log('WebSocket disconnected')

      // Attempt to reconnect after 3 seconds
      setTimeout(() => connectWebSocket(pid), 3000)
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    wsRef.current = ws
  }

  const handleWebSocketMessage = (data: Record<string, unknown>) => {
    switch (data.type) {
      case 'connected':
        if (data.game_state) {
          setGameState(data.game_state as GameState)
        }
        break

      case 'game_started':
        setGameState(prev => prev ? { ...prev, started: true, board_state: data.board_state as GameState['board_state'] } : null)
        break

      case 'move_result':
      case 'move_made':
        if ((data.result as { board_state?: GameState['board_state'] })?.board_state) {
          setGameState(prev => prev ? { ...prev, board_state: (data.result as { board_state: GameState['board_state'] }).board_state } : null)
        }
        // Show AI reasoning if available
        if ((data as { ai_move?: { reasoning?: string } }).ai_move?.reasoning) {
          setAiReasoning((data as { ai_move: { reasoning: string } }).ai_move.reasoning)
          setAiThinking(false)
        }
        if ((data.result as { game_over?: { winner: string } })?.game_over) {
          handleGameOver((data.result as { game_over: { winner: string } }).game_over)
        }
        break

      case 'legal_moves':
        setLegalMoves(data.moves as LegalMove[])
        break

      case 'chat':
        setChatMessages(prev => [...prev, {
          id: Date.now().toString(),
          player_id: data.player_id as string,
          message: data.message as string,
          timestamp: new Date()
        }])
        break

      case 'player_joined':
        fetchGameState()
        break

      case 'game_ended':
        handleGameOver(data as { winner?: string; reason?: string })
        break
    }
  }

  const handleGameOver = (gameOver: { winner?: string; reason?: string }) => {
    // Show game over notification
    setGameState(prev => prev ? { ...prev, ended: true } : null)
  }

  const handleMove = useCallback(async (move: {
    source: string
    target1: string
    target2?: string
    move_type: string
  }) => {
    // Set AI thinking for AI games
    if (gameState?.ai_color) {
      setAiThinking(true)
      setAiReasoning('')
    }

    // Send move via WebSocket
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'move',
        ...move
      }))
    } else {
      // Fallback to REST API
      try {
        const response = await fetch(`/api/games/${gameId}/move?player_id=${playerId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(move)
        })
        const data = await response.json()

        if (data.board_state) {
          setGameState(prev => prev ? { ...prev, board_state: data.board_state } : null)
        }
        if (data.ai_move?.reasoning) {
          setAiReasoning(data.ai_move.reasoning)
          setAiThinking(false)
        }
      } catch (error) {
        console.error('Failed to make move:', error)
        setAiThinking(false)
      }
    }

    // Clear legal moves after moving
    setLegalMoves([])
  }, [gameId, playerId, gameState])

  const handleRequestLegalMoves = useCallback(async (square: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'get_legal_moves',
        square
      }))
    } else {
      try {
        const response = await fetch(`/api/games/${gameId}/legal-moves/${square}`)
        const data = await response.json()
        setLegalMoves(data.moves || [])
      } catch (error) {
        console.error('Failed to get legal moves:', error)
      }
    }
  }, [gameId])

  const handleStartGame = async () => {
    try {
      await fetch(`/api/games/${gameId}/start`, { method: 'POST' })
    } catch (error) {
      console.error('Failed to start game:', error)
    }
  }

  const handleSendChat = () => {
    if (!chatInput.trim()) return

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'chat',
        message: chatInput
      }))
    }

    setChatInput('')
  }

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleResign = () => {
    if (confirm('Are you sure you want to resign?')) {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ type: 'resign' }))
      }
    }
  }

  const isMyTurn = gameState?.board_state?.turn === playerColor
  const isAIGame = !!gameState?.ai_color

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-[1fr,380px] gap-8">
          {/* Main Game Area */}
          <div>
            {/* Game Header */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center justify-between mb-6"
            >
              <div>
                <h1 className="text-2xl font-bold">
                  {isAIGame ? 'Playing vs Gemini AI' : 'Quantum Chess Match'}
                </h1>
                <p className="text-slate-400">
                  Game ID: {gameId}
                  <button
                    onClick={handleCopyLink}
                    className="ml-2 text-quantum-accent hover:text-quantum-primary transition-colors"
                  >
                    {copied ? <Check className="w-4 h-4 inline" /> : <Copy className="w-4 h-4 inline" />}
                  </button>
                </p>
              </div>

              <div className="flex items-center gap-2">
                {/* Connection status */}
                <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-500' : 'bg-red-500'}`} />
                <span className="text-sm text-slate-400">
                  {isConnected ? 'Connected' : 'Connecting...'}
                </span>
              </div>
            </motion.div>

            {/* Chess Board */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex justify-center"
            >
              {gameState?.board_state ? (
                <QuantumChessBoard
                  boardState={gameState.board_state}
                  playerColor={playerColor}
                  onMove={handleMove}
                  isMyTurn={isMyTurn && !aiThinking}
                  legalMoves={legalMoves}
                  onRequestLegalMoves={handleRequestLegalMoves}
                />
              ) : (
                <div className="w-[480px] h-[480px] bg-slate-800 rounded-xl flex items-center justify-center">
                  {!gameState?.started ? (
                    <div className="text-center">
                      <p className="text-slate-400 mb-4">Waiting for game to start...</p>
                      <button onClick={handleStartGame} className="btn-quantum">
                        Start Game
                      </button>
                    </div>
                  ) : (
                    <div className="animate-pulse">
                      <Sparkles className="w-12 h-12 text-quantum-primary" />
                    </div>
                  )}
                </div>
              )}
            </motion.div>

            {/* Game Controls */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex justify-center gap-4 mt-8"
            >
              <button
                onClick={handleResign}
                className="px-4 py-2 rounded-lg bg-slate-700 text-slate-300 hover:bg-slate-600 transition-colors flex items-center gap-2"
              >
                <Flag className="w-4 h-4" />
                Resign
              </button>
              <button
                className="px-4 py-2 rounded-lg bg-slate-700 text-slate-300 hover:bg-slate-600 transition-colors flex items-center gap-2"
              >
                <RotateCcw className="w-4 h-4" />
                Offer Draw
              </button>
            </motion.div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Players Panel */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="card p-4"
            >
              <h3 className="font-semibold mb-4">Players</h3>

              {/* White Player */}
              <div className={`flex items-center gap-3 p-3 rounded-lg ${gameState?.board_state?.turn === 'white' ? 'bg-quantum-primary/10 border border-quantum-primary/30' : ''}`}>
                <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-2xl">
                  ♔
                </div>
                <div className="flex-grow">
                  <div className="font-medium flex items-center gap-2">
                    {isAIGame && playerColor !== 'white' ? (
                      <>
                        <Bot className="w-4 h-4 text-quantum-secondary" />
                        Gemini AI
                      </>
                    ) : (
                      <>
                        <User className="w-4 h-4" />
                        {playerColor === 'white' ? 'You' : 'Opponent'}
                      </>
                    )}
                  </div>
                  <div className="text-sm text-slate-400">White</div>
                </div>
                {gameState?.board_state?.turn === 'white' && (
                  <span className="text-xs text-quantum-primary animate-pulse">●</span>
                )}
              </div>

              {/* Black Player */}
              <div className={`flex items-center gap-3 p-3 rounded-lg mt-2 ${gameState?.board_state?.turn === 'black' ? 'bg-quantum-primary/10 border border-quantum-primary/30' : ''}`}>
                <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-600 flex items-center justify-center text-2xl">
                  ♚
                </div>
                <div className="flex-grow">
                  <div className="font-medium flex items-center gap-2">
                    {isAIGame && playerColor !== 'black' ? (
                      <>
                        <Bot className="w-4 h-4 text-quantum-secondary" />
                        Gemini AI
                      </>
                    ) : (
                      <>
                        <User className="w-4 h-4" />
                        {playerColor === 'black' ? 'You' : 'Opponent'}
                      </>
                    )}
                  </div>
                  <div className="text-sm text-slate-400">Black</div>
                </div>
                {gameState?.board_state?.turn === 'black' && (
                  <span className="text-xs text-quantum-primary animate-pulse">●</span>
                )}
              </div>
            </motion.div>

            {/* AI Thinking Panel */}
            {isAIGame && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 }}
                className="card p-4"
              >
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <Bot className="w-4 h-4 text-quantum-secondary" />
                  AI Analysis
                </h3>

                {aiThinking ? (
                  <div className="flex items-center gap-3 text-slate-400">
                    <Sparkles className="w-5 h-5 animate-spin text-quantum-secondary" />
                    Gemini is thinking...
                  </div>
                ) : aiReasoning ? (
                  <p className="text-sm text-slate-300">{aiReasoning}</p>
                ) : (
                  <p className="text-sm text-slate-500">Make a move to see AI analysis</p>
                )}
              </motion.div>
            )}

            {/* Move History */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.15 }}
              className="card p-4"
            >
              <h3 className="font-semibold mb-3">Move History</h3>
              <div className="max-h-48 overflow-y-auto space-y-1 text-sm font-mono">
                {gameState?.move_history && gameState.move_history.length > 0 ? (
                  gameState.move_history.map((move, index) => (
                    <div key={index} className="flex items-center gap-2 text-slate-400">
                      <span className="text-slate-500">{Math.floor(index / 2) + 1}.</span>
                      <span>{move.source} → {move.target1}</span>
                      {move.target2 && <span className="text-quantum-secondary">(split: {move.target2})</span>}
                    </div>
                  ))
                ) : (
                  <p className="text-slate-500">No moves yet</p>
                )}
              </div>
            </motion.div>

            {/* Chat (for multiplayer) */}
            {!isAIGame && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="card p-4"
              >
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  Chat
                </h3>

                {/* Messages */}
                <div className="h-48 overflow-y-auto space-y-2 mb-3">
                  {chatMessages.map(msg => (
                    <div
                      key={msg.id}
                      className={`text-sm p-2 rounded-lg ${msg.player_id === playerId
                        ? 'bg-quantum-primary/20 ml-4'
                        : 'bg-slate-700/50 mr-4'
                        }`}
                    >
                      <p>{msg.message}</p>
                    </div>
                  ))}
                  <div ref={chatEndRef} />
                </div>

                {/* Input */}
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendChat()}
                    placeholder="Type a message..."
                    className="flex-grow px-3 py-2 bg-slate-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-quantum-primary"
                  />
                  <button
                    onClick={handleSendChat}
                    className="p-2 bg-quantum-primary rounded-lg hover:bg-quantum-primary/80 transition-colors"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
