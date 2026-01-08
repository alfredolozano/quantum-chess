import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { ChevronLeft, ChevronRight, BookOpen, CheckCircle, Play } from 'lucide-react'

interface LessonContent {
  id: string
  title: string
  content: string
  interactive?: {
    type: string
    config?: Record<string, unknown>
    questions?: Array<{
      question: string
      options: string[]
      correct: number
      explanation: string
    }>
  }
}

export function LessonPage() {
  const { moduleId, lessonId } = useParams()
  const navigate = useNavigate()
  const [lesson, setLesson] = useState<LessonContent | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showExplanation, setShowExplanation] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState(0)

  useEffect(() => {
    fetchLesson()
  }, [moduleId, lessonId])

  const fetchLesson = async () => {
    try {
      const response = await fetch(`/api/learning/modules/${moduleId}/lessons/${lessonId}`)
      const data = await response.json()
      setLesson(data)
    } catch (error) {
      console.error('Failed to fetch lesson:', error)
      // Fallback demo content
      setLesson({
        id: lessonId || 'demo',
        title: 'Quantum Computing Basics',
        content: `
# What is Quantum Computing?

Quantum computing is a revolutionary approach to computation that harnesses the strange and powerful properties of quantum mechanics.

## Classical vs Quantum

**Classical computers** use bits that are either 0 or 1. Every operation, every calculation, every piece of data is ultimately represented as a sequence of these binary digits.

**Quantum computers** use **qubits** (quantum bits) that can exist in a **superposition** of both 0 and 1 simultaneously.

## The Power of Quantum

| Classical | Quantum |
|-----------|---------|
| Bit: 0 OR 1 | Qubit: 0 AND 1 (until measured) |
| Definite state | Probabilistic state |
| Independent bits | Entangled qubits |

## Code Example

\`\`\`python
import cirq

# Create a qubit
q = cirq.LineQubit(0)

# Create a circuit with Hadamard gate
circuit = cirq.Circuit(cirq.H(q))

print(circuit)
\`\`\`

## Key Takeaways

1. Quantum computers exploit quantum mechanical phenomena
2. Qubits can be in superposition (multiple states at once)
3. Measurement collapses the quantum state to a definite value
`,
        interactive: {
          type: 'quiz',
          questions: [
            {
              question: 'What is the main difference between a bit and a qubit?',
              options: [
                'Qubits are faster',
                'Qubits can be in superposition',
                'Bits are more accurate',
                'There is no difference'
              ],
              correct: 1,
              explanation: 'Unlike classical bits which are either 0 or 1, qubits can exist in a superposition of both states simultaneously.'
            }
          ]
        }
      })
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSelect = (index: number) => {
    setSelectedAnswer(index)
    setShowExplanation(true)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse">
          <BookOpen className="w-12 h-12 text-quantum-primary" />
        </div>
      </div>
    )
  }

  if (!lesson) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Lesson not found</h2>
          <Link to="/learn" className="text-quantum-primary hover:underline">
            Return to Learning Path
          </Link>
        </div>
      </div>
    )
  }

  const currentQuiz = lesson.interactive?.questions?.[currentQuestion]

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Navigation */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-2 text-slate-400 mb-8"
        >
          <Link to="/learn" className="hover:text-white transition-colors">
            Learning Path
          </Link>
          <ChevronRight className="w-4 h-4" />
          <span className="capitalize">{moduleId?.replace('-', ' ')}</span>
          <ChevronRight className="w-4 h-4" />
          <span className="text-white">{lesson.title}</span>
        </motion.div>

        {/* Lesson Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-8 md:p-12"
        >
          <div className="markdown-content prose prose-invert max-w-none">
            <ReactMarkdown
              components={{
                code({ className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '')
                  const isInline = !match

                  return isInline ? (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  ) : (
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  )
                }
              }}
            >
              {lesson.content}
            </ReactMarkdown>
          </div>

          {/* Interactive Quiz */}
          {lesson.interactive?.type === 'quiz' && currentQuiz && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-12 pt-8 border-t border-slate-700"
            >
              <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <Play className="w-5 h-5 text-quantum-primary" />
                Test Your Knowledge
              </h3>

              <div className="bg-slate-800/50 rounded-xl p-6">
                <p className="text-lg mb-6">{currentQuiz.question}</p>

                <div className="space-y-3">
                  {currentQuiz.options.map((option, index) => {
                    const isSelected = selectedAnswer === index
                    const isCorrect = index === currentQuiz.correct
                    const showResult = showExplanation

                    return (
                      <button
                        key={index}
                        onClick={() => handleAnswerSelect(index)}
                        disabled={showExplanation}
                        className={`
                          w-full p-4 rounded-lg text-left transition-all flex items-center gap-3
                          ${showResult
                            ? isCorrect
                              ? 'bg-emerald-500/20 border-2 border-emerald-500'
                              : isSelected
                                ? 'bg-rose-500/20 border-2 border-rose-500'
                                : 'bg-slate-700/50 border-2 border-transparent'
                            : isSelected
                              ? 'bg-quantum-primary/20 border-2 border-quantum-primary'
                              : 'bg-slate-700/50 border-2 border-transparent hover:border-slate-600'
                          }
                          ${showExplanation ? 'cursor-default' : 'cursor-pointer'}
                        `}
                      >
                        <span className={`
                          w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium
                          ${showResult
                            ? isCorrect
                              ? 'bg-emerald-500 text-white'
                              : isSelected
                                ? 'bg-rose-500 text-white'
                                : 'bg-slate-600 text-slate-300'
                            : isSelected
                              ? 'bg-quantum-primary text-white'
                              : 'bg-slate-600 text-slate-300'
                          }
                        `}>
                          {String.fromCharCode(65 + index)}
                        </span>
                        <span className="flex-grow">{option}</span>
                        {showResult && isCorrect && (
                          <CheckCircle className="w-5 h-5 text-emerald-500" />
                        )}
                      </button>
                    )
                  })}
                </div>

                {/* Explanation */}
                {showExplanation && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-6 p-4 bg-slate-700/50 rounded-lg"
                  >
                    <p className="text-slate-300">
                      <span className="font-semibold text-quantum-accent">Explanation: </span>
                      {currentQuiz.explanation}
                    </p>
                  </motion.div>
                )}
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* Navigation Buttons */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="flex items-center justify-between mt-8"
        >
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
            Previous Lesson
          </button>

          <button
            className="btn-quantum flex items-center gap-2"
          >
            Next Lesson
            <ChevronRight className="w-5 h-5" />
          </button>
        </motion.div>
      </div>
    </div>
  )
}
