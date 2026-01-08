import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Users, Bot, Swords, ArrowRight, Sparkles } from 'lucide-react'

type GameMode = 'human' | 'ai' | null
type Difficulty = 'easy' | 'medium' | 'hard'
type Color = 'white' | 'black' | 'random'

export function PlayPage() {
  const navigate = useNavigate()
  const [selectedMode, setSelectedMode] = useState<GameMode>(null)
  const [difficulty, setDifficulty] = useState<Difficulty>('medium')
  const [playerColor, setPlayerColor] = useState<Color>('white')
  const [isCreating, setIsCreating] = useState(false)

  const handleCreateGame = async () => {
    setIsCreating(true)

    try {
      const response = await fetch('/api/games', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          player_name: 'Player',
          game_type: selectedMode === 'ai' ? 'ai' : 'multiplayer',
          ai_difficulty: difficulty,
          player_color: playerColor === 'random'
            ? (Math.random() < 0.5 ? 'white' : 'black')
            : playerColor
        })
      })

      const data = await response.json()

      if (data.success) {
        // Store player info in session storage
        sessionStorage.setItem('playerId', data.player_id)
        sessionStorage.setItem('playerColor', data.player_color || data.color)

        if (selectedMode === 'human') {
          // Go to lobby to share game link
          navigate(`/play/lobby?gameId=${data.game_id}`)
        } else {
          // Start AI game immediately
          navigate(`/play/game/${data.game_id}`)
        }
      }
    } catch (error) {
      console.error('Failed to create game:', error)
    } finally {
      setIsCreating(false)
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
              Play Quantum Chess
            </span>
          </h1>
          <p className="text-slate-400 text-lg">
            Choose your game mode and start playing
          </p>
        </motion.div>

        {/* Game Mode Selection */}
        {!selectedMode ? (
          <div className="grid md:grid-cols-2 gap-6">
            {/* Play vs Human */}
            <motion.button
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              onClick={() => setSelectedMode('human')}
              className="card p-8 text-left hover:border-quantum-primary/50 transition-all group cursor-pointer"
            >
              <div className="w-16 h-16 rounded-xl bg-quantum-primary/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Users className="w-8 h-8 text-quantum-primary" />
              </div>
              <h2 className="text-2xl font-bold mb-2">Play vs Human</h2>
              <p className="text-slate-400 mb-4">
                Challenge a friend or play against other players online.
                Share a game link to invite your opponent.
              </p>
              <div className="flex items-center text-quantum-primary font-medium">
                Start Game <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </motion.button>

            {/* Play vs AI */}
            <motion.button
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              onClick={() => setSelectedMode('ai')}
              className="card p-8 text-left hover:border-quantum-secondary/50 transition-all group cursor-pointer"
            >
              <div className="w-16 h-16 rounded-xl bg-quantum-secondary/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Bot className="w-8 h-8 text-quantum-secondary" />
              </div>
              <h2 className="text-2xl font-bold mb-2">Play vs Gemini AI</h2>
              <p className="text-slate-400 mb-4">
                Test your skills against Google's Gemini AI.
                Choose your difficulty level and color.
              </p>
              <div className="flex items-center text-quantum-secondary font-medium">
                Start Game <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </motion.button>
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card p-8"
          >
            {/* Back button */}
            <button
              onClick={() => setSelectedMode(null)}
              className="text-slate-400 hover:text-white transition-colors mb-6 flex items-center gap-2"
            >
              <ArrowRight className="w-4 h-4 rotate-180" />
              Back to mode selection
            </button>

            {/* Game Setup */}
            <div className="flex items-center gap-4 mb-8">
              {selectedMode === 'human' ? (
                <Users className="w-10 h-10 text-quantum-primary" />
              ) : (
                <Bot className="w-10 h-10 text-quantum-secondary" />
              )}
              <div>
                <h2 className="text-2xl font-bold">
                  {selectedMode === 'human' ? 'Play vs Human' : 'Play vs Gemini AI'}
                </h2>
                <p className="text-slate-400">Configure your game settings</p>
              </div>
            </div>

            {/* Settings */}
            <div className="space-y-6">
              {/* AI Difficulty (only for AI mode) */}
              {selectedMode === 'ai' && (
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-3">
                    AI Difficulty
                  </label>
                  <div className="grid grid-cols-3 gap-3">
                    {(['easy', 'medium', 'hard'] as Difficulty[]).map((level) => (
                      <button
                        key={level}
                        onClick={() => setDifficulty(level)}
                        className={`
                          py-3 px-4 rounded-lg border-2 transition-all capitalize font-medium
                          ${difficulty === level
                            ? 'border-quantum-secondary bg-quantum-secondary/20 text-white'
                            : 'border-slate-700 text-slate-400 hover:border-slate-600'}
                        `}
                      >
                        {level}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Color Selection */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-3">
                  Play As
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { value: 'white', label: 'White', emoji: '♔' },
                    { value: 'black', label: 'Black', emoji: '♚' },
                    { value: 'random', label: 'Random', emoji: '🎲' },
                  ].map((option) => (
                    <button
                      key={option.value}
                      onClick={() => setPlayerColor(option.value as Color)}
                      className={`
                        py-3 px-4 rounded-lg border-2 transition-all font-medium flex items-center justify-center gap-2
                        ${playerColor === option.value
                          ? 'border-quantum-primary bg-quantum-primary/20 text-white'
                          : 'border-slate-700 text-slate-400 hover:border-slate-600'}
                      `}
                    >
                      <span className="text-xl">{option.emoji}</span>
                      {option.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Start Game Button */}
              <button
                onClick={handleCreateGame}
                disabled={isCreating}
                className="w-full btn-quantum flex items-center justify-center gap-2 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCreating ? (
                  <>
                    <Sparkles className="w-5 h-5 animate-spin" />
                    Creating Game...
                  </>
                ) : (
                  <>
                    <Swords className="w-5 h-5" />
                    Start Game
                  </>
                )}
              </button>
            </div>
          </motion.div>
        )}

        {/* Quick Play Options */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mt-12 text-center"
        >
          <p className="text-slate-500 mb-4">Or join an existing game:</p>
          <Link
            to="/play/lobby"
            className="text-quantum-accent hover:text-quantum-primary transition-colors"
          >
            Browse Open Games →
          </Link>
        </motion.div>
      </div>
    </div>
  )
}
