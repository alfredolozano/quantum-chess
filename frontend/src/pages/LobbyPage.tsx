import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Copy, Check, Users, RefreshCw, Play, Clock, ArrowRight } from 'lucide-react'

interface Game {
  game_id: string
  type: string
  players: {
    white: boolean
    black: boolean
  }
  started: boolean
  ended: boolean
}

export function LobbyPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const gameIdFromUrl = searchParams.get('gameId')

  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [copied, setCopied] = useState(false)
  const [joinCode, setJoinCode] = useState('')

  useEffect(() => {
    fetchGames()

    // Refresh games list every 5 seconds
    const interval = setInterval(fetchGames, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchGames = async () => {
    try {
      const response = await fetch('/api/games')
      const data = await response.json()
      setGames(data.games.filter((g: Game) => g.type === 'multiplayer' && !g.ended))
    } catch (error) {
      console.error('Failed to fetch games:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCopyLink = () => {
    if (gameIdFromUrl) {
      const link = `${window.location.origin}/play/lobby?gameId=${gameIdFromUrl}`
      navigator.clipboard.writeText(link)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleJoinGame = async (gameId: string) => {
    try {
      const response = await fetch(`/api/games/${gameId}/join`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_name: 'Player' })
      })

      const data = await response.json()

      if (data.success) {
        sessionStorage.setItem('playerId', data.player_id)
        sessionStorage.setItem('playerColor', data.color)
        navigate(`/play/game/${gameId}`)
      }
    } catch (error) {
      console.error('Failed to join game:', error)
    }
  }

  const handleJoinByCode = async () => {
    if (joinCode.trim()) {
      await handleJoinGame(joinCode.trim())
    }
  }

  const handleStartMyGame = () => {
    if (gameIdFromUrl) {
      navigate(`/play/game/${gameIdFromUrl}`)
    }
  }

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold mb-4">
            <span className="bg-quantum-gradient bg-clip-text text-transparent">
              Game Lobby
            </span>
          </h1>
          <p className="text-slate-400 text-lg">
            Join an existing game or share your game link
          </p>
        </motion.div>

        {/* Your Game (if created) */}
        {gameIdFromUrl && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card p-6 mb-8 border-quantum-primary/30 bg-quantum-primary/5"
          >
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Play className="w-5 h-5 text-quantum-primary" />
              Your Game is Ready
            </h2>

            <p className="text-slate-300 mb-4">
              Share this link with your opponent to start playing:
            </p>

            <div className="flex gap-2 mb-6">
              <input
                type="text"
                readOnly
                value={`${window.location.origin}/play/lobby?gameId=${gameIdFromUrl}`}
                className="flex-grow px-4 py-3 bg-slate-800 rounded-lg text-sm font-mono text-slate-300"
              />
              <button
                onClick={handleCopyLink}
                className="px-4 py-3 bg-slate-700 rounded-lg hover:bg-slate-600 transition-colors flex items-center gap-2"
              >
                {copied ? (
                  <>
                    <Check className="w-4 h-4 text-emerald-400" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4" />
                    Copy
                  </>
                )}
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-slate-400">
                <Clock className="w-4 h-4" />
                <span>Waiting for opponent...</span>
              </div>
              <button onClick={handleStartMyGame} className="btn-quantum flex items-center gap-2">
                Go to Game
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        )}

        {/* Join by Code */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card p-6 mb-8"
        >
          <h2 className="text-xl font-semibold mb-4">Join by Game Code</h2>

          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Enter game code..."
              value={joinCode}
              onChange={(e) => setJoinCode(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleJoinByCode()}
              className="flex-grow px-4 py-3 bg-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-quantum-primary"
            />
            <button
              onClick={handleJoinByCode}
              disabled={!joinCode.trim()}
              className="btn-quantum disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Join Game
            </button>
          </div>
        </motion.div>

        {/* Available Games */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Users className="w-5 h-5 text-quantum-accent" />
              Open Games
            </h2>
            <button
              onClick={fetchGames}
              className="p-2 text-slate-400 hover:text-white transition-colors"
            >
              <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>

          {loading ? (
            <div className="text-center py-8">
              <RefreshCw className="w-8 h-8 text-quantum-primary animate-spin mx-auto" />
            </div>
          ) : games.length > 0 ? (
            <div className="space-y-3">
              {games.map(game => (
                <div
                  key={game.game_id}
                  className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg hover:bg-slate-800 transition-colors"
                >
                  <div>
                    <div className="font-mono text-sm text-quantum-accent">
                      {game.game_id}
                    </div>
                    <div className="text-sm text-slate-400">
                      {game.players.white && game.players.black
                        ? 'Full'
                        : game.players.white
                          ? 'Needs Black player'
                          : 'Needs White player'}
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="flex gap-1">
                      <span className={`w-3 h-3 rounded-full ${game.players.white ? 'bg-white' : 'bg-slate-600'}`} />
                      <span className={`w-3 h-3 rounded-full ${game.players.black ? 'bg-slate-800 border border-slate-500' : 'bg-slate-600'}`} />
                    </div>

                    {(!game.players.white || !game.players.black) && (
                      <button
                        onClick={() => handleJoinGame(game.game_id)}
                        className="px-4 py-2 bg-quantum-primary rounded-lg hover:bg-quantum-primary/80 transition-colors text-sm font-medium"
                      >
                        Join
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-slate-400">
              <Users className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p>No open games available</p>
              <Link to="/play" className="text-quantum-accent hover:text-quantum-primary transition-colors mt-2 inline-block">
                Create a new game →
              </Link>
            </div>
          )}
        </motion.div>

        {/* Create New Game */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-center mt-8"
        >
          <Link
            to="/play"
            className="text-quantum-accent hover:text-quantum-primary transition-colors"
          >
            ← Back to Game Setup
          </Link>
        </motion.div>
      </div>
    </div>
  )
}
