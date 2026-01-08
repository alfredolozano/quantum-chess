import { Outlet, Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Atom, Play, BookOpen, Github } from 'lucide-react'

export function Layout() {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Home', icon: Atom },
    { path: '/play', label: 'Play', icon: Play },
    { path: '/learn', label: 'Learn', icon: BookOpen },
  ]

  return (
    <div className="min-h-screen bg-dark-gradient">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-3 group">
              <div className="relative">
                <Atom className="w-8 h-8 text-quantum-primary group-hover:text-quantum-accent transition-colors" />
                <div className="absolute inset-0 blur-md bg-quantum-primary/30 group-hover:bg-quantum-accent/30 transition-colors" />
              </div>
              <span className="text-xl font-bold bg-quantum-gradient bg-clip-text text-transparent">
                Quantum Chess
              </span>
            </Link>

            {/* Nav Links */}
            <div className="flex items-center gap-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path ||
                  (item.path !== '/' && location.pathname.startsWith(item.path))

                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`
                      relative px-4 py-2 rounded-lg flex items-center gap-2 transition-all
                      ${isActive
                        ? 'text-white'
                        : 'text-slate-400 hover:text-white hover:bg-slate-800/50'}
                    `}
                  >
                    {isActive && (
                      <motion.div
                        layoutId="activeNav"
                        className="absolute inset-0 bg-quantum-primary/20 rounded-lg border border-quantum-primary/30"
                        transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                    <Icon className="w-4 h-4 relative z-10" />
                    <span className="relative z-10 font-medium">{item.label}</span>
                  </Link>
                )
              })}
            </div>

            {/* GitHub Link */}
            <a
              href="https://github.com/quantumlib/unitary"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-slate-400 hover:text-white transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-16">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-8 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-slate-400">
              <Atom className="w-5 h-5" />
              <span>Quantum Chess - Powered by Cirq & Google AI</span>
            </div>
            <div className="flex items-center gap-6 text-sm text-slate-500">
              <a href="https://quantumai.google/cirq" target="_blank" rel="noopener noreferrer" className="hover:text-quantum-accent transition-colors">
                Cirq Documentation
              </a>
              <a href="https://github.com/quantumlib/unitary" target="_blank" rel="noopener noreferrer" className="hover:text-quantum-accent transition-colors">
                Unitary Library
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
