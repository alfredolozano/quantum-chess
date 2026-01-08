import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { BookOpen, Clock, ChevronRight, Atom, Cpu, Crown, Brain, Code } from 'lucide-react'

interface Lesson {
  id: string
  title: string
  duration: string
}

interface Module {
  id: string
  title: string
  description: string
  icon: string
  difficulty: string
  estimated_time: string
  lessons: Lesson[]
}

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  'atom': Atom,
  'circuit': Cpu,
  'chess': Crown,
  'brain': Brain,
  'code': Code,
}

const difficultyColors: Record<string, string> = {
  'beginner': 'text-emerald-400 bg-emerald-400/10',
  'intermediate': 'text-amber-400 bg-amber-400/10',
  'advanced': 'text-rose-400 bg-rose-400/10',
}

export function LearnPage() {
  const [modules, setModules] = useState<Module[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedModule, setExpandedModule] = useState<string | null>(null)

  useEffect(() => {
    fetchModules()
  }, [])

  const fetchModules = async () => {
    try {
      const response = await fetch('/api/learning/modules')
      const data = await response.json()
      setModules(data.modules)
    } catch (error) {
      console.error('Failed to fetch modules:', error)
      // Use fallback data for demo
      setModules([
        {
          id: 'quantum-basics',
          title: 'Quantum Computing Fundamentals',
          description: 'Learn the core concepts of quantum computing that power Quantum Chess',
          icon: 'atom',
          difficulty: 'beginner',
          estimated_time: '45 min',
          lessons: [
            { id: 'what-is-quantum', title: 'What is Quantum Computing?', duration: '10 min' },
            { id: 'qubits', title: 'Qubits: The Quantum Bit', duration: '10 min' },
            { id: 'superposition', title: 'Superposition: Being in Two States', duration: '10 min' },
            { id: 'measurement', title: 'Measurement and Collapse', duration: '8 min' },
            { id: 'entanglement', title: 'Entanglement: Spooky Action', duration: '7 min' },
          ]
        },
        {
          id: 'quantum-gates',
          title: 'Quantum Gates',
          description: 'Understand the quantum gates used in Quantum Chess',
          icon: 'circuit',
          difficulty: 'intermediate',
          estimated_time: '40 min',
          lessons: [
            { id: 'gate-basics', title: 'What are Quantum Gates?', duration: '8 min' },
            { id: 'single-qubit-gates', title: 'Single-Qubit Gates (X, H, Z)', duration: '10 min' },
            { id: 'iswap-gate', title: 'The iSWAP Gate', duration: '12 min' },
            { id: 'controlled-gates', title: 'Controlled Gates', duration: '10 min' },
          ]
        },
        {
          id: 'quantum-chess-rules',
          title: 'Quantum Chess Rules',
          description: 'Master the rules of Quantum Chess',
          icon: 'chess',
          difficulty: 'beginner',
          estimated_time: '35 min',
          lessons: [
            { id: 'overview', title: 'Quantum Chess Overview', duration: '8 min' },
            { id: 'standard-moves', title: 'Standard Quantum Moves', duration: '8 min' },
            { id: 'split-moves', title: 'Split Moves: Creating Superposition', duration: '10 min' },
            { id: 'merge-moves', title: 'Merge Moves: Collapsing Superposition', duration: '9 min' },
          ]
        },
        {
          id: 'quantum-strategy',
          title: 'Quantum Chess Strategy',
          description: 'Advanced strategies for Quantum Chess',
          icon: 'brain',
          difficulty: 'advanced',
          estimated_time: '50 min',
          lessons: [
            { id: 'quantum-threats', title: 'Creating Quantum Threats', duration: '12 min' },
            { id: 'probability-thinking', title: 'Thinking in Probabilities', duration: '12 min' },
            { id: 'entanglement-tactics', title: 'Entanglement Tactics', duration: '13 min' },
            { id: 'measurement-timing', title: 'When to Measure', duration: '13 min' },
          ]
        },
        {
          id: 'cirq-introduction',
          title: 'Introduction to Cirq',
          description: "Learn Google's quantum computing framework",
          icon: 'code',
          difficulty: 'intermediate',
          estimated_time: '60 min',
          lessons: [
            { id: 'cirq-setup', title: 'Setting Up Cirq', duration: '10 min' },
            { id: 'creating-circuits', title: 'Creating Quantum Circuits', duration: '15 min' },
            { id: 'simulation', title: 'Simulating Circuits', duration: '15 min' },
            { id: 'chess-application', title: 'Cirq in Quantum Chess', duration: '20 min' },
          ]
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin">
          <Atom className="w-12 h-12 text-quantum-primary" />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold mb-4">
            <span className="bg-quantum-gradient bg-clip-text text-transparent">
              Learning Path
            </span>
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Master quantum computing concepts and become a Quantum Chess expert
            through our interactive lessons.
          </p>
        </motion.div>

        {/* Progress Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card p-6 mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold mb-1">Your Progress</h3>
              <p className="text-slate-400 text-sm">
                {modules.length} modules • {modules.reduce((acc, m) => acc + m.lessons.length, 0)} lessons
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-quantum-primary">0%</div>
              <p className="text-slate-400 text-sm">Complete</p>
            </div>
          </div>
          <div className="mt-4 h-2 bg-slate-700 rounded-full overflow-hidden">
            <div className="h-full w-0 bg-quantum-gradient rounded-full transition-all duration-500" />
          </div>
        </motion.div>

        {/* Modules */}
        <div className="space-y-4">
          {modules.map((module, index) => {
            const Icon = iconMap[module.icon] || BookOpen
            const isExpanded = expandedModule === module.id

            return (
              <motion.div
                key={module.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="card overflow-hidden"
              >
                {/* Module Header */}
                <button
                  onClick={() => setExpandedModule(isExpanded ? null : module.id)}
                  className="w-full p-6 flex items-center gap-4 hover:bg-slate-800/50 transition-colors text-left"
                >
                  <div className={`w-14 h-14 rounded-xl ${difficultyColors[module.difficulty].split(' ')[1]} flex items-center justify-center flex-shrink-0`}>
                    <Icon className={`w-7 h-7 ${difficultyColors[module.difficulty].split(' ')[0]}`} />
                  </div>
                  <div className="flex-grow min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="text-lg font-semibold truncate">{module.title}</h3>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium capitalize ${difficultyColors[module.difficulty]}`}>
                        {module.difficulty}
                      </span>
                    </div>
                    <p className="text-slate-400 text-sm line-clamp-1">{module.description}</p>
                  </div>
                  <div className="flex items-center gap-4 flex-shrink-0">
                    <div className="text-right hidden sm:block">
                      <div className="flex items-center gap-1 text-slate-400 text-sm">
                        <Clock className="w-4 h-4" />
                        {module.estimated_time}
                      </div>
                      <div className="text-slate-500 text-xs">
                        {module.lessons.length} lessons
                      </div>
                    </div>
                    <ChevronRight
                      className={`w-5 h-5 text-slate-400 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                    />
                  </div>
                </button>

                {/* Lessons */}
                {isExpanded && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="border-t border-slate-700"
                  >
                    <div className="p-4 space-y-2">
                      {module.lessons.map((lesson, lessonIndex) => (
                        <Link
                          key={lesson.id}
                          to={`/learn/${module.id}/${lesson.id}`}
                          className="flex items-center gap-4 p-4 rounded-lg hover:bg-slate-800/50 transition-colors group"
                        >
                          <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-sm font-medium text-slate-400 group-hover:bg-quantum-primary/20 group-hover:text-quantum-primary transition-colors">
                            {lessonIndex + 1}
                          </div>
                          <div className="flex-grow">
                            <h4 className="font-medium group-hover:text-quantum-primary transition-colors">
                              {lesson.title}
                            </h4>
                          </div>
                          <div className="flex items-center gap-2 text-slate-500 text-sm">
                            <Clock className="w-4 h-4" />
                            {lesson.duration}
                          </div>
                          <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-quantum-primary group-hover:translate-x-1 transition-all" />
                        </Link>
                      ))}
                    </div>
                  </motion.div>
                )}
              </motion.div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
