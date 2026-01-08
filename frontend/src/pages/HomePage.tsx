import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Play, BookOpen, Users, Bot, Sparkles, Atom, Zap, GitBranch } from 'lucide-react'

export function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-32">
        {/* Background Effects */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-quantum-primary/20 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-quantum-secondary/20 rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-quantum-accent/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            {/* Animated Logo */}
            <motion.div
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="flex justify-center mb-8"
            >
              <div className="relative">
                <Atom className="w-24 h-24 text-quantum-primary animate-pulse-slow" />
                <div className="absolute inset-0 blur-xl bg-quantum-primary/30 animate-quantum-glow" />
              </div>
            </motion.div>

            {/* Title */}
            <motion.h1
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="text-5xl md:text-7xl font-bold mb-6"
            >
              <span className="bg-quantum-gradient bg-clip-text text-transparent">
                Quantum Chess
              </span>
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3, duration: 0.5 }}
              className="text-xl md:text-2xl text-slate-300 mb-8 max-w-3xl mx-auto"
            >
              Experience chess like never before. Pieces exist in{' '}
              <span className="text-quantum-accent font-semibold">superposition</span>,{' '}
              moves create <span className="text-quantum-secondary font-semibold">entanglement</span>,{' '}
              and captures trigger <span className="text-quantum-primary font-semibold">measurement</span>.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.5 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <Link to="/play" className="btn-quantum flex items-center gap-2 text-lg">
                <Play className="w-5 h-5" />
                Play Now
              </Link>
              <Link to="/learn" className="btn-outline flex items-center gap-2 text-lg">
                <BookOpen className="w-5 h-5" />
                Learn Quantum Chess
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              The Future of Chess
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              Powered by Google's Cirq quantum computing framework and Gemini AI
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature Cards */}
            {[
              {
                icon: Sparkles,
                title: 'Superposition Moves',
                description: 'Split your pieces to exist in two places at once. Create quantum threats that force impossible choices.',
                color: 'text-quantum-primary',
                bgColor: 'bg-quantum-primary/10',
              },
              {
                icon: GitBranch,
                title: 'Entanglement Tactics',
                description: 'Pieces become mysteriously connected. Measuring one affects the other, creating cascading effects.',
                color: 'text-quantum-secondary',
                bgColor: 'bg-quantum-secondary/10',
              },
              {
                icon: Zap,
                title: 'Quantum Measurement',
                description: 'Captures trigger measurement, collapsing superposition. Strategy meets probability.',
                color: 'text-quantum-accent',
                bgColor: 'bg-quantum-accent/10',
              },
              {
                icon: Users,
                title: 'Play Online',
                description: 'Challenge friends or players worldwide in real-time quantum chess battles.',
                color: 'text-emerald-400',
                bgColor: 'bg-emerald-400/10',
              },
              {
                icon: Bot,
                title: 'AI Opponent',
                description: 'Test your skills against Gemini AI, trained to understand quantum chess strategy.',
                color: 'text-amber-400',
                bgColor: 'bg-amber-400/10',
              },
              {
                icon: BookOpen,
                title: 'Learning Path',
                description: 'Master quantum computing concepts through interactive lessons and puzzles.',
                color: 'text-rose-400',
                bgColor: 'bg-rose-400/10',
              },
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ y: 20, opacity: 0 }}
                whileInView={{ y: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card p-6 hover:border-slate-600/50 transition-colors group"
              >
                <div className={`w-12 h-12 rounded-lg ${feature.bgColor} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <feature.icon className={`w-6 h-6 ${feature.color}`} />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-slate-800/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              How Quantum Chess Works
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              The game uses real quantum computing principles
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <motion.div
              initial={{ x: -20, opacity: 0 }}
              whileInView={{ x: 0, opacity: 1 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 rounded-full bg-quantum-primary/20 border-2 border-quantum-primary flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-quantum-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Split Move</h3>
              <p className="text-slate-400">
                Move your Knight to two squares at once using √iSWAP gate.
                It now exists with 50% probability in each location.
              </p>
              <div className="mt-4 font-mono text-sm text-quantum-accent bg-slate-800 rounded-lg p-3">
                ♞ e4 → f6(50%) + d6(50%)
              </div>
            </motion.div>

            {/* Step 2 */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              whileInView={{ y: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-center"
            >
              <div className="w-16 h-16 rounded-full bg-quantum-secondary/20 border-2 border-quantum-secondary flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-quantum-secondary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Create Threats</h3>
              <p className="text-slate-400">
                Your superposed piece threatens all squares from both positions.
                Opponent must defend against both possibilities.
              </p>
              <div className="mt-4 font-mono text-sm text-quantum-secondary bg-slate-800 rounded-lg p-3">
                ♞~(f6) threatens ♛(g8)<br/>
                ♞~(d6) threatens ♜(b7)
              </div>
            </motion.div>

            {/* Step 3 */}
            <motion.div
              initial={{ x: 20, opacity: 0 }}
              whileInView={{ x: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="text-center"
            >
              <div className="w-16 h-16 rounded-full bg-quantum-accent/20 border-2 border-quantum-accent flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-quantum-accent">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Measurement</h3>
              <p className="text-slate-400">
                When you capture, measurement occurs. The quantum state collapses
                to a definite outcome based on probability.
              </p>
              <div className="mt-4 font-mono text-sm text-quantum-accent bg-slate-800 rounded-lg p-3">
                Capture ♛(g8)? → 50% success!<br/>
                Measurement: ♞ found on f6 ✓
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            className="card p-12 bg-gradient-to-br from-quantum-primary/20 to-quantum-secondary/20 border-quantum-primary/30"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Enter the Quantum Realm?
            </h2>
            <p className="text-slate-300 text-lg mb-8 max-w-2xl mx-auto">
              Start with our interactive learning path or jump straight into a game.
              No quantum physics PhD required!
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link to="/play" className="btn-quantum flex items-center gap-2 text-lg">
                <Play className="w-5 h-5" />
                Start Playing
              </Link>
              <Link to="/learn" className="btn-outline flex items-center gap-2 text-lg">
                <BookOpen className="w-5 h-5" />
                Take the Tutorial
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
