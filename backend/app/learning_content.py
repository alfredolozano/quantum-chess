"""
Quantum Chess Learning Path Content

Comprehensive learning modules for quantum computing and quantum chess.
"""

from typing import Dict, List, Optional


LEARNING_MODULES = [
    {
        "id": "quantum-basics",
        "title": "Quantum Computing Fundamentals",
        "description": "Learn the core concepts of quantum computing that power Quantum Chess",
        "icon": "atom",
        "difficulty": "beginner",
        "estimated_time": "45 min",
        "lessons": [
            {
                "id": "what-is-quantum",
                "title": "What is Quantum Computing?",
                "duration": "10 min"
            },
            {
                "id": "qubits",
                "title": "Qubits: The Quantum Bit",
                "duration": "10 min"
            },
            {
                "id": "superposition",
                "title": "Superposition: Being in Two States",
                "duration": "10 min"
            },
            {
                "id": "measurement",
                "title": "Measurement and Collapse",
                "duration": "8 min"
            },
            {
                "id": "entanglement",
                "title": "Entanglement: Spooky Action",
                "duration": "7 min"
            }
        ]
    },
    {
        "id": "quantum-gates",
        "title": "Quantum Gates",
        "description": "Understand the quantum gates used in Quantum Chess",
        "icon": "circuit",
        "difficulty": "intermediate",
        "estimated_time": "40 min",
        "lessons": [
            {
                "id": "gate-basics",
                "title": "What are Quantum Gates?",
                "duration": "8 min"
            },
            {
                "id": "single-qubit-gates",
                "title": "Single-Qubit Gates (X, H, Z)",
                "duration": "10 min"
            },
            {
                "id": "iswap-gate",
                "title": "The iSWAP Gate",
                "duration": "12 min"
            },
            {
                "id": "controlled-gates",
                "title": "Controlled Gates",
                "duration": "10 min"
            }
        ]
    },
    {
        "id": "quantum-chess-rules",
        "title": "Quantum Chess Rules",
        "description": "Master the rules of Quantum Chess",
        "icon": "chess",
        "difficulty": "beginner",
        "estimated_time": "35 min",
        "lessons": [
            {
                "id": "overview",
                "title": "Quantum Chess Overview",
                "duration": "8 min"
            },
            {
                "id": "standard-moves",
                "title": "Standard Quantum Moves",
                "duration": "8 min"
            },
            {
                "id": "split-moves",
                "title": "Split Moves: Creating Superposition",
                "duration": "10 min"
            },
            {
                "id": "merge-moves",
                "title": "Merge Moves: Collapsing Superposition",
                "duration": "9 min"
            }
        ]
    },
    {
        "id": "quantum-strategy",
        "title": "Quantum Chess Strategy",
        "description": "Advanced strategies for Quantum Chess",
        "icon": "brain",
        "difficulty": "advanced",
        "estimated_time": "50 min",
        "lessons": [
            {
                "id": "quantum-threats",
                "title": "Creating Quantum Threats",
                "duration": "12 min"
            },
            {
                "id": "probability-thinking",
                "title": "Thinking in Probabilities",
                "duration": "12 min"
            },
            {
                "id": "entanglement-tactics",
                "title": "Entanglement Tactics",
                "duration": "13 min"
            },
            {
                "id": "measurement-timing",
                "title": "When to Measure",
                "duration": "13 min"
            }
        ]
    },
    {
        "id": "cirq-introduction",
        "title": "Introduction to Cirq",
        "description": "Learn Google's quantum computing framework",
        "icon": "code",
        "difficulty": "intermediate",
        "estimated_time": "60 min",
        "lessons": [
            {
                "id": "cirq-setup",
                "title": "Setting Up Cirq",
                "duration": "10 min"
            },
            {
                "id": "creating-circuits",
                "title": "Creating Quantum Circuits",
                "duration": "15 min"
            },
            {
                "id": "simulation",
                "title": "Simulating Circuits",
                "duration": "15 min"
            },
            {
                "id": "chess-application",
                "title": "Cirq in Quantum Chess",
                "duration": "20 min"
            }
        ]
    }
]


LESSON_CONTENT = {
    "quantum-basics": {
        "what-is-quantum": {
            "id": "what-is-quantum",
            "title": "What is Quantum Computing?",
            "content": """
# What is Quantum Computing?

Quantum computing is a revolutionary approach to computation that harnesses the strange and powerful properties of quantum mechanics.

## Classical vs Quantum

**Classical computers** use bits that are either 0 or 1. Every operation, every calculation, every piece of data is ultimately represented as a sequence of these binary digits.

**Quantum computers** use **qubits** (quantum bits) that can exist in a **superposition** of both 0 and 1 simultaneously. This allows quantum computers to process vast amounts of information in parallel.

## Why Does This Matter for Chess?

In Quantum Chess, we use these quantum properties to create a new kind of game:

- **Pieces can exist in multiple positions at once** (superposition)
- **Pieces can be mysteriously connected** (entanglement)
- **The game only becomes definite when you look** (measurement)

## The Power of Quantum

| Classical | Quantum |
|-----------|---------|
| Bit: 0 OR 1 | Qubit: 0 AND 1 (until measured) |
| Definite state | Probabilistic state |
| Independent bits | Entangled qubits |
| Read anytime | Measurement changes state |

## Key Takeaways

1. Quantum computers exploit quantum mechanical phenomena
2. Qubits can be in superposition (multiple states at once)
3. Measurement collapses the quantum state to a definite value
4. These properties create new strategic possibilities in Quantum Chess
""",
            "interactive": {
                "type": "quiz",
                "questions": [
                    {
                        "question": "What is the main difference between a bit and a qubit?",
                        "options": [
                            "Qubits are faster",
                            "Qubits can be in superposition",
                            "Bits are more accurate",
                            "There is no difference"
                        ],
                        "correct": 1,
                        "explanation": "Unlike classical bits which are either 0 or 1, qubits can exist in a superposition of both states simultaneously."
                    },
                    {
                        "question": "In Quantum Chess, what happens to a piece in superposition?",
                        "options": [
                            "It moves twice as fast",
                            "It exists in multiple positions at once",
                            "It becomes invisible",
                            "It captures two pieces"
                        ],
                        "correct": 1,
                        "explanation": "A piece in superposition exists in multiple positions simultaneously, each with a certain probability."
                    }
                ]
            }
        },
        "qubits": {
            "id": "qubits",
            "title": "Qubits: The Quantum Bit",
            "content": """
# Qubits: The Quantum Bit

A **qubit** (quantum bit) is the fundamental unit of quantum information.

## The Bloch Sphere

A qubit's state can be visualized as a point on the **Bloch sphere**:

```
         |0⟩
          ↑
          |
    ←-----+-----→
          |
          ↓
         |1⟩
```

- The north pole represents |0⟩
- The south pole represents |1⟩
- Points in between represent superpositions

## Mathematical Representation

A qubit state is written as:

**|ψ⟩ = α|0⟩ + β|1⟩**

Where:
- α and β are complex numbers called **amplitudes**
- |α|² is the probability of measuring 0
- |β|² is the probability of measuring 1
- |α|² + |β|² = 1 (probabilities must sum to 1)

## Example States

| State | α | β | P(0) | P(1) |
|-------|---|---|------|------|
| |0⟩ | 1 | 0 | 100% | 0% |
| |1⟩ | 0 | 1 | 0% | 100% |
| |+⟩ | 1/√2 | 1/√2 | 50% | 50% |
| |-⟩ | 1/√2 | -1/√2 | 50% | 50% |

## In Quantum Chess

Each square on the board corresponds to a qubit:
- **|1⟩** means a piece is definitely there
- **|0⟩** means the square is definitely empty
- **Superposition** means the piece might be there with some probability

## Key Takeaways

1. A qubit is the quantum analog of a classical bit
2. Qubits are described by amplitudes α and β
3. Probabilities are the squares of the amplitudes
4. In Quantum Chess, each square is represented by a qubit
""",
            "interactive": {
                "type": "simulation",
                "config": {
                    "title": "Explore Qubit States",
                    "description": "Adjust the amplitudes and see how probabilities change",
                    "type": "qubit_visualizer"
                }
            }
        },
        "superposition": {
            "id": "superposition",
            "title": "Superposition: Being in Two States",
            "content": """
# Superposition: Being in Two States

**Superposition** is the quantum mechanical principle that allows a quantum system to exist in multiple states simultaneously.

## The Classic Analogy: Schrödinger's Cat

Imagine a cat in a box with a quantum device. Until you open the box, the cat is both alive AND dead at the same time. This is superposition.

```
    ┌─────────────────┐
    │   🐱 + 💀      │  ← Cat in superposition
    │    (alive AND   │
    │     dead)       │
    └─────────────────┘
           ↓ Open box
    ┌─────────────────┐
    │      🐱         │  ← Cat collapsed to alive
    └─────────────────┘
```

## Creating Superposition

The **Hadamard gate (H)** is commonly used to create superposition:

**H|0⟩ = |+⟩ = (|0⟩ + |1⟩)/√2**

This means:
- Start with |0⟩ (definitely 0)
- Apply H gate
- End up with equal probability of 0 and 1

## Superposition in Quantum Chess

When you perform a **split move**, your piece enters superposition:

```
Before Split:
    ♞ on e4

After Split:
    ♞~(50%) on f6
    ♞~(50%) on d6
```

The knight now exists in BOTH positions simultaneously!

## Why is This Powerful?

1. **Parallel Threats**: Attack multiple targets at once
2. **Uncertainty**: Opponent doesn't know where your piece really is
3. **Efficiency**: One piece controls multiple squares

## Key Properties

- Superposition exists until **measurement**
- Measurement **collapses** the superposition
- You cannot know the exact state without measuring
- In chess, attempting capture triggers measurement

## Key Takeaways

1. Superposition means existing in multiple states at once
2. The Hadamard gate creates equal superposition
3. Split moves in Quantum Chess create piece superposition
4. Measurement collapses superposition to a single state
""",
            "interactive": {
                "type": "simulation",
                "config": {
                    "title": "Create Superposition",
                    "description": "Apply quantum gates and see superposition form",
                    "type": "gate_sequence",
                    "initial_state": "|0⟩",
                    "available_gates": ["H", "X"]
                }
            }
        },
        "measurement": {
            "id": "measurement",
            "title": "Measurement and Collapse",
            "content": """
# Measurement and Collapse

**Measurement** in quantum mechanics is the process of observing a quantum system, which causes its superposition to **collapse** to a definite state.

## The Measurement Problem

Before measurement:
- Qubit is in superposition: α|0⟩ + β|1⟩
- Has probability |α|² of being 0, |β|² of being 1

After measurement:
- Qubit is definitely 0 OR definitely 1
- The superposition is destroyed
- The result is probabilistic

```
    α|0⟩ + β|1⟩
         ↓
    [MEASUREMENT]
         ↓
    ┌─────────────────┐
    │ |0⟩ with prob   │
    │     |α|²        │
    ├─────────────────┤
    │ |1⟩ with prob   │
    │     |β|²        │
    └─────────────────┘
```

## Measurement in Quantum Chess

Measurement occurs when:

1. **Capture attempts**: Trying to capture a superposed piece
2. **Path blocking**: A sliding piece encounters potential obstacle
3. **Merge moves**: Attempting to merge superposed pieces

### Example: Capture Measurement

```
White Queen attacks Black Knight in superposition:

Black Knight: 50% on f6, 50% on d6
Queen captures on f6...

MEASUREMENT OCCURS!
Result: Knight collapses...

If Knight was on f6 → Captured! ✓
If Knight was on d6 → Queen moves to empty square
```

## The Observer Effect

This is not just a limitation of our knowledge—the act of measurement fundamentally changes the quantum state. This is a core principle of quantum mechanics.

## Strategic Implications

1. **Delayed measurement**: Keep pieces in superposition as long as possible
2. **Forced measurement**: Force opponent's pieces to collapse
3. **Probability calculation**: Always know the odds before measuring

## Key Takeaways

1. Measurement collapses superposition to a definite state
2. The result is probabilistic based on amplitudes
3. In Quantum Chess, captures trigger measurement
4. Strategic timing of measurement is crucial
""",
            "interactive": {
                "type": "simulation",
                "config": {
                    "title": "Measurement Experiment",
                    "description": "Create superposition and measure multiple times to see probability distribution",
                    "type": "measurement_demo",
                    "num_trials": 100
                }
            }
        },
        "entanglement": {
            "id": "entanglement",
            "title": "Entanglement: Spooky Action",
            "content": """
# Entanglement: Spooky Action at a Distance

**Entanglement** is a quantum phenomenon where two or more particles become correlated in such a way that measuring one instantly affects the other, regardless of distance.

## Einstein's "Spooky Action"

Einstein famously called entanglement "spooky action at a distance" because it seemed to violate the principle that information cannot travel faster than light.

## How Entanglement Works

When two qubits are entangled, they share a quantum state:

**|Φ⁺⟩ = (|00⟩ + |11⟩)/√2**

This means:
- 50% chance both are 0
- 50% chance both are 1
- But they're **always** the same!

```
    Entangled Qubits
    ┌─────┐   ┌─────┐
    │ A   │~~~│ B   │
    └─────┘   └─────┘
        │         │
        ↓         ↓
    Measure A   B collapses
    = 0         = 0 instantly!
```

## Entanglement in Quantum Chess

When you split a piece, the two positions become **entangled**:

```
Knight splits: e4 → f6 and d6

The two positions are entangled!
If you measure f6 and find the knight there,
d6 INSTANTLY becomes empty (and vice versa).
```

### Cascade Effects

Entanglement can spread through multiple pieces:

```
1. Knight splits e4 → f6, d6 (entangled)
2. Knight from f6 attacks g8 (slide move)
   Now g8 is entangled with f6 and d6!
3. Measuring any of these affects all others
```

## Strategic Implications

1. **Information chains**: Use entanglement to gain information
2. **Collapse chains**: One measurement can collapse multiple pieces
3. **Trap setting**: Create entanglement webs for tactical advantage

## Key Takeaways

1. Entangled qubits share a quantum state
2. Measuring one instantly affects the other
3. Split moves create entanglement between positions
4. Entanglement can cascade through multiple pieces
""",
            "interactive": {
                "type": "simulation",
                "config": {
                    "title": "Explore Entanglement",
                    "description": "Create an entangled pair and see how measurement of one affects the other",
                    "type": "entanglement_demo"
                }
            }
        }
    },
    "quantum-gates": {
        "gate-basics": {
            "id": "gate-basics",
            "title": "What are Quantum Gates?",
            "content": """
# What are Quantum Gates?

**Quantum gates** are the building blocks of quantum circuits, analogous to logic gates in classical computing.

## Gates as Transformations

A quantum gate transforms the state of one or more qubits. Mathematically, they are represented as **unitary matrices**.

## Key Properties

1. **Reversible**: Every quantum gate can be undone
2. **Unitary**: Preserves the total probability (sums to 1)
3. **No cloning**: Cannot copy a quantum state

## Visual Representation

Quantum circuits are drawn left-to-right:

```
|0⟩ ─────[H]─────[M]───→ result

     │
     └── Hadamard gate
```

## Common Gate Symbols

| Gate | Symbol | Description |
|------|--------|-------------|
| H | ─[H]─ | Hadamard (creates superposition) |
| X | ─[X]─ | NOT gate (flips 0↔1) |
| Z | ─[Z]─ | Phase flip |
| CNOT | ─●─ | Controlled NOT |
|      |  │  |              |
|      | ─⊕─ |              |

## Gates in Quantum Chess

Quantum Chess uses specific gates:
- **iSWAP**: Standard moves
- **√iSWAP**: Split moves
- **Controlled-iSWAP**: Slide moves

## Key Takeaways

1. Quantum gates transform qubit states
2. All quantum gates are reversible
3. Gates are represented as unitary matrices
4. Quantum Chess uses specialized gates like iSWAP
""",
            "interactive": {
                "type": "gate_playground",
                "config": {
                    "available_gates": ["H", "X", "Z", "CNOT"]
                }
            }
        },
        "single-qubit-gates": {
            "id": "single-qubit-gates",
            "title": "Single-Qubit Gates (X, H, Z)",
            "content": """
# Single-Qubit Gates

Single-qubit gates operate on one qubit at a time. Here are the most important ones:

## The X Gate (NOT Gate)

The **X gate** flips the qubit state:
- |0⟩ → |1⟩
- |1⟩ → |0⟩

Matrix:
```
X = | 0  1 |
    | 1  0 |
```

## The Hadamard Gate (H)

The **H gate** creates superposition:
- |0⟩ → (|0⟩ + |1⟩)/√2 = |+⟩
- |1⟩ → (|0⟩ - |1⟩)/√2 = |-⟩

Matrix:
```
H = 1/√2 | 1   1 |
         | 1  -1 |
```

## The Z Gate (Phase Flip)

The **Z gate** flips the phase:
- |0⟩ → |0⟩
- |1⟩ → -|1⟩

Matrix:
```
Z = | 1   0 |
    | 0  -1 |
```

## Effect on the Bloch Sphere

- **X**: Rotation by π around X-axis
- **H**: Rotation that maps Z to X axis
- **Z**: Rotation by π around Z-axis

## In Quantum Chess Context

While Quantum Chess primarily uses iSWAP gates, understanding these basic gates helps you understand:
- How superposition is created
- How quantum states transform
- The mathematics behind quantum moves

## Key Takeaways

1. X gate flips between |0⟩ and |1⟩
2. H gate creates equal superposition
3. Z gate adds a phase of -1 to |1⟩
4. These form the foundation for more complex gates
""",
            "interactive": {
                "type": "simulation",
                "config": {
                    "title": "Single Qubit Gate Explorer",
                    "type": "single_gate_demo",
                    "gates": ["X", "H", "Z"]
                }
            }
        },
        "iswap-gate": {
            "id": "iswap-gate",
            "title": "The iSWAP Gate",
            "content": """
# The iSWAP Gate

The **iSWAP gate** is the fundamental operation in Quantum Chess. It's used for moving pieces on the board.

## What Does iSWAP Do?

The iSWAP gate swaps two qubits and adds a phase of *i*:

- |01⟩ → i|10⟩
- |10⟩ → i|01⟩
- |00⟩ → |00⟩
- |11⟩ → |11⟩

Matrix:
```
iSWAP = | 1  0  0  0 |
        | 0  0  i  0 |
        | 0  i  0  0 |
        | 0  0  0  1 |
```

## iSWAP in Chess Moves

When a piece moves from square A to square B:

1. Square A is qubit with |1⟩ (occupied)
2. Square B is qubit with |0⟩ (empty)
3. iSWAP transforms |10⟩ → i|01⟩
4. Now A is empty, B is occupied!

```
Before: A=♞, B=empty  →  |10⟩
After:  A=empty, B=♞  →  i|01⟩

The piece has moved!
```

## The √iSWAP Gate

The **√iSWAP** (square root of iSWAP) is used for split moves:

- Creates a 50/50 superposition
- Applied twice equals iSWAP

```
|10⟩ ──[√iSWAP]──→ (|10⟩ + i|01⟩)/√2

The piece is now in superposition between both squares!
```

## Split Move Mechanics

A split move uses √iSWAP + iSWAP:

```
Knight on e4, split to f6 and d6:

1. √iSWAP(e4, f6): Creates 50/50 between e4 and f6
2. iSWAP(e4, d6): Moves remaining amplitude to d6

Result: Knight is 50% on f6, 50% on d6
```

## Why iSWAP?

The iSWAP gate is chosen because:
1. It naturally swaps qubit states (perfect for moving pieces)
2. The phase factor helps track quantum interference
3. It's implementable on real quantum hardware
4. Its square root enables split moves

## Key Takeaways

1. iSWAP swaps two qubits with a phase factor of i
2. Standard chess moves use the full iSWAP
3. √iSWAP creates superposition for split moves
4. These gates form the core of Quantum Chess mechanics
""",
            "interactive": {
                "type": "simulation",
                "config": {
                    "title": "iSWAP Gate Demonstration",
                    "type": "iswap_demo"
                }
            }
        },
        "controlled-gates": {
            "id": "controlled-gates",
            "title": "Controlled Gates",
            "content": """
# Controlled Gates

**Controlled gates** apply an operation to a target qubit only when a control qubit is in a specific state.

## CNOT (Controlled-NOT)

The simplest controlled gate:
- If control = |1⟩: Apply X to target
- If control = |0⟩: Do nothing

```
Control: ──●──
           │
Target:  ──⊕──

|00⟩ → |00⟩
|01⟩ → |01⟩
|10⟩ → |11⟩  ← Target flipped
|11⟩ → |10⟩  ← Target flipped
```

## Creating Entanglement

CNOT can create entanglement:

```
|0⟩ ──[H]──●──
           │
|0⟩ ───────⊕──

Start: |00⟩
After H: (|0⟩ + |1⟩)|0⟩/√2 = (|00⟩ + |10⟩)/√2
After CNOT: (|00⟩ + |11⟩)/√2  ← Entangled!
```

## Controlled-iSWAP

In Quantum Chess, **controlled-iSWAP** enables slide moves:

```
Control: ──●──
           │
Qubit A: ──┼──iSWAP──
           │    │
Qubit B: ──┴────┴────

The iSWAP only happens if control qubit = |0⟩ (empty square)
```

## Slide Moves in Quantum Chess

When a rook, bishop, or queen slides past potentially occupied squares:

```
Rook on a1 wants to move to a4, but a2 might be occupied:

a2 is control qubit
a1, a4 are iSWAP targets

If a2 = |0⟩ (empty): Rook moves to a4
If a2 = |1⟩ (blocked): Move is blocked
If a2 is in superposition: Move becomes entangled!
```

## Entanglement Through Slides

This creates powerful tactical situations:

```
1. Knight splits to a2 (50%) and b2 (50%)
2. Rook tries to slide from a1 to a4

Now: Rook's position is ENTANGLED with Knight's position!

If Knight is on a2: Rook stays on a1
If Knight is on b2: Rook is on a4
```

## Key Takeaways

1. Controlled gates apply operations conditionally
2. CNOT creates entanglement between qubits
3. Controlled-iSWAP enables quantum slide moves
4. Slide moves create tactical entanglement
""",
            "interactive": {
                "type": "simulation",
                "config": {
                    "title": "Controlled Gate Explorer",
                    "type": "controlled_gate_demo"
                }
            }
        }
    },
    "quantum-chess-rules": {
        "overview": {
            "id": "overview",
            "title": "Quantum Chess Overview",
            "content": """
# Quantum Chess Overview

Welcome to **Quantum Chess**! This game combines the classical strategy of chess with the mind-bending principles of quantum mechanics.

## What Makes It Different?

In traditional chess, a piece is either on a square or it isn't. In Quantum Chess:

- **Pieces can be in multiple places at once** (superposition)
- **Pieces can be mysteriously connected** (entanglement)
- **The board becomes definite only when observed** (measurement)

## The Board

The board looks like regular chess, but with quantum enhancements:

```
  a b c d e f g h
8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 8
7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 7
6 · · · · · · · · 6
5 · · · · · · · · 5
4 · · · · · · · · 4
3 · · · · · · · · 3
2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ 2
1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 1
  a b c d e f g h

Superposed pieces shown with ~ (e.g., ♞~)
Probability shown as opacity or percentage
```

## Move Types

1. **Standard Moves**: Like regular chess, but quantum
2. **Split Moves**: Put a piece in two places at once
3. **Merge Moves**: Collapse a split piece to one location
4. **Capture Moves**: Trigger measurement when capturing

## Winning

The game ends when a King is **definitively captured**. This might require measurement to confirm the King's location!

## Key Differences from Regular Chess

| Regular Chess | Quantum Chess |
|--------------|---------------|
| Piece on one square | Piece on multiple squares |
| Captures always work | Captures might "miss" |
| Definite board state | Probabilistic board state |
| What you see is what you get | Observation changes reality |

## Ready to Learn More?

The following lessons will teach you each move type in detail!
""",
            "interactive": {
                "type": "board_demo",
                "config": {
                    "title": "Interactive Board",
                    "description": "Click on pieces to see their quantum state"
                }
            }
        },
        "standard-moves": {
            "id": "standard-moves",
            "title": "Standard Quantum Moves",
            "content": """
# Standard Quantum Moves

Standard moves in Quantum Chess work similarly to regular chess, but with quantum mechanics under the hood.

## How Standard Moves Work

When you move a piece from square A to square B:

1. The game applies an **iSWAP gate** between squares A and B
2. The piece's quantum state transfers from A to B
3. If the piece was in a definite state, it remains definite
4. If the piece was in superposition, the superposition moves too!

## Example: Moving a Knight

```
Before:           After:
♞ on e4    →     ♞ on f6

Quantum State:
|e4=1, f6=0⟩  →  |e4=0, f6=1⟩
```

## Moving Superposed Pieces

You can move a piece that's already in superposition:

```
Before:
♞~(50%) on e4
♞~(50%) on g4

Move e4 to f6:

After:
♞~(50%) on f6
♞~(50%) on g4  ← This stays!
```

## Blocked Moves

If a sliding piece (rook, bishop, queen) might be blocked:

```
Rook on a1 wants to reach a4
a2 has a piece in superposition (50%)

What happens?
- If a2 is empty: Rook reaches a4
- If a2 is occupied: Rook is blocked
- The move becomes ENTANGLED with a2!
```

## Rules for Standard Moves

1. Pieces move according to normal chess rules
2. You can only move your own pieces
3. You can move any of your pieces, even if in superposition
4. The move affects one "branch" of the superposition

## Key Takeaways

1. Standard moves use the iSWAP gate
2. Superposed pieces can be moved normally
3. Slide moves through superposed squares create entanglement
4. The quantum state transfers with the piece
""",
            "interactive": {
                "type": "move_tutorial",
                "config": {
                    "move_type": "standard"
                }
            }
        },
        "split-moves": {
            "id": "split-moves",
            "title": "Split Moves: Creating Superposition",
            "content": """
# Split Moves: Creating Superposition

**Split moves** are unique to Quantum Chess. They allow you to put a piece in two places at once!

## Which Pieces Can Split?

- ✓ Knights
- ✓ Bishops
- ✓ Rooks
- ✓ Queens
- ✗ Pawns (cannot split)
- ✗ Kings (cannot split - too important!)

## How to Perform a Split Move

1. Select your piece
2. Choose TWO valid destination squares
3. The piece enters superposition at both locations

## The Mechanics

A split uses **√iSWAP** and **iSWAP** gates:

```
Knight on e4, splitting to f6 and d6:

Step 1: √iSWAP(e4, f6)
   e4: 50%, f6: 50%, d6: 0%

Step 2: iSWAP(e4, d6)
   e4: 0%, f6: 50%, d6: 50%

Result: Knight is equally on f6 AND d6!
```

## Visual Representation

```
Before Split:
    · · · · · · · ·
    · · · ♞ · · · ·    ← Knight on e4
    · · · · · · · ·

After Split:
    · · · · · · · ·
    · · ♞~ · ♞~ · ·    ← 50% on d6, 50% on f6
    · · · · · · · ·

The ~ indicates superposition
```

## Strategic Uses

1. **Double Attack**: Threaten two pieces simultaneously
2. **Control**: Dominate more squares
3. **Confusion**: Opponent must guess your real position
4. **Defense**: Protect multiple areas at once

## Example: Double Fork

```
Split your Knight to attack both the Queen and Rook:

    · ♛ · · · · · ·
    · · · · · · · ·
    · · ♞~· · ♞~· ·    ← Knight threatens both!
    · · · · · · · ·
    · · · · ♜ · · ·

Opponent must deal with BOTH threats!
```

## Key Takeaways

1. Split moves put pieces in superposition
2. Each location has 50% probability
3. Only Knights, Bishops, Rooks, Queens can split
4. Split creates powerful tactical opportunities
""",
            "interactive": {
                "type": "move_tutorial",
                "config": {
                    "move_type": "split"
                }
            }
        },
        "merge-moves": {
            "id": "merge-moves",
            "title": "Merge Moves: Collapsing Superposition",
            "content": """
# Merge Moves: Collapsing Superposition

**Merge moves** attempt to bring a superposed piece back to a single location. This involves quantum measurement!

## When to Merge

You might want to merge when:
- You need a piece at full strength in one location
- You want to resolve uncertainty before a critical move
- You're setting up for a definite capture

## How Merge Works

1. Select one location of your superposed piece
2. Attempt to move from that location
3. **Measurement occurs!**
4. The piece collapses to one definite position

## The Measurement Outcome

```
Knight in superposition: 50% on f6, 50% on d6

You try to move from f6 to e8:

MEASUREMENT!

Outcome A (50% chance):
  Knight was on f6 → Move succeeds → Knight on e8

Outcome B (50% chance):
  Knight was on d6 → Move fails → Knight stays on d6
```

## Visual Example

```
Before Merge Attempt:
    · · · · · · · ·
    · · ♞~ · ♞~ · ·    ← 50% each
    · · · · · · · ·

Try to move f6 to e8:
    [MEASUREMENT]

Possible Result 1:
    · · · ♞ · · · ·    ← Knight on e8 (100%)
    · · · · · · · ·

Possible Result 2:
    · · · · · · · ·
    · · ♞ · · · · ·    ← Knight stayed on d6 (100%)
```

## Strategic Considerations

**Timing matters!**
- Merge too early: Lose quantum advantage
- Merge too late: Risk losing the piece

**Probability awareness:**
- Know the odds before merging
- 50% success might be too risky in critical positions

## Forced Measurement

Sometimes measurement is forced:
- When your piece is captured
- When your piece blocks another's path
- When you capture an opponent's piece

## Key Takeaways

1. Merge moves trigger measurement
2. The piece collapses to one location
3. Outcome is probabilistic
4. Strategic timing is crucial
""",
            "interactive": {
                "type": "move_tutorial",
                "config": {
                    "move_type": "merge"
                }
            }
        }
    },
    "quantum-strategy": {
        "quantum-threats": {
            "id": "quantum-threats",
            "title": "Creating Quantum Threats",
            "content": """
# Creating Quantum Threats

In Quantum Chess, you can threaten multiple pieces simultaneously using superposition!

## The Power of Quantum Threats

A piece in superposition threatens **all** squares it could attack from **all** its possible positions.

```
Knight in superposition on e4 and c4:

Threatens from e4: d6, f6, d2, f2, c5, g5, c3, g3
Threatens from c4: b6, d6, b2, d2, a5, e5, a3, e3

Combined: 14 unique squares under threat!
```

## Creating a Quantum Fork

A fork attacks two pieces at once. A quantum fork can attack **four or more**!

```
Strategy:
1. Split your Knight to two locations
2. Each location forks different pieces
3. Opponent cannot defend everything!

    ♜ · · · ♚ · · ♜
    · · · · · · · ·
    · ♞~· · · ♞~· ·   ← Quantum fork!
    · · · · · · · ·

Left Knight threatens: Queen and Rook
Right Knight threatens: King and Rook
```

## Threatening Superposed Pieces

When you threaten a piece in superposition:

```
Your Queen attacks square e4
Opponent's Knight: 50% on e4, 50% on c4

If you capture on e4:
- 50% chance: You capture the Knight
- 50% chance: Your Queen just moved to e4

This creates interesting risk/reward decisions!
```

## Defensive Quantum Threats

Use superposition defensively:

```
Split your Bishop to protect two pawns:

    · · · · · · · ·
    ♟ · · · ♟ · · ·   ← Two vulnerable pawns
    · · · · · · · ·
    · ♝~ · ♝~ · · ·   ← Both protected!
```

## Key Takeaways

1. Superposed pieces threaten more squares
2. Quantum forks attack multiple targets
3. Threatening superposed pieces involves probability
4. Defense can also use superposition
""",
            "interactive": {
                "type": "puzzle",
                "config": {
                    "title": "Create a Quantum Fork",
                    "puzzle_type": "quantum_fork"
                }
            }
        },
        "probability-thinking": {
            "id": "probability-thinking",
            "title": "Thinking in Probabilities",
            "content": """
# Thinking in Probabilities

In Quantum Chess, you must think in terms of probabilities rather than certainties.

## Expected Value

Calculate the **expected value** of your moves:

```
Your Knight (50% on f6, 50% on d6) can capture:
- Queen on g8 from f6 (value: 9 points)
- Rook on b6 from d6 (value: 5 points)

Expected value = 0.5 × 9 + 0.5 × 5 = 7 points

Compare to alternatives!
```

## Risk Assessment

Consider both best and worst cases:

```
Best case: Capture the Queen (50%)
Worst case: Miss and lose position (50%)

Is the risk worth it?
```

## Probability Tracking

Keep track of piece probabilities:

```
Game state:
- Your Knight: 50% e4, 50% g4
- Opponent Knight: 50% f6, 50% d6
- Your Bishop: 100% c1 (not superposed)
- Opponent Rook: 75% a8, 25% h8 (after partial measurement)

Make decisions based on these numbers!
```

## Cascading Probabilities

When entangled pieces interact:

```
Knight A: 50% on e4, 50% on g4
Knight B: 50% on f6, 50% on d6

If they're entangled (from same split):
- e4 + d6 always together: 50%
- g4 + f6 always together: 50%

If independent:
- e4 + d6: 25%
- e4 + f6: 25%
- g4 + d6: 25%
- g4 + f6: 25%

Know the difference!
```

## Making Probabilistic Decisions

Framework for decisions:
1. Calculate expected material gain/loss
2. Consider positional factors at each probability
3. Weigh risk tolerance (leading vs trailing)
4. Factor in opponent's likely responses

## Key Takeaways

1. Always calculate expected values
2. Track probabilities of all superposed pieces
3. Understand entanglement correlations
4. Balance risk vs reward based on game state
""",
            "interactive": {
                "type": "puzzle",
                "config": {
                    "title": "Calculate the Best Move",
                    "puzzle_type": "probability_calculation"
                }
            }
        },
        "entanglement-tactics": {
            "id": "entanglement-tactics",
            "title": "Entanglement Tactics",
            "content": """
# Entanglement Tactics

Entanglement creates powerful tactical opportunities unique to Quantum Chess.

## Creating Tactical Entanglement

Use slide moves to create entanglement:

```
Setup:
- Opponent Knight: 50% on e4, 50% on g4
- Your Rook on a4

Play:
- Rook slides from a4 toward h4
- If Knight is on e4, Rook stops
- If Knight is on g4, Rook can reach h4

Result:
- Rook's position is ENTANGLED with Knight!
```

## The Information Advantage

Measurement reveals correlated information:

```
After entanglement:
- Knight on e4 ↔ Rook on a4
- Knight on g4 ↔ Rook on h4

If you measure and find Rook on h4:
You KNOW Knight is on g4 without measuring it!
```

## Cascade Attacks

Chain entanglement for devastating attacks:

```
1. Split your Queen: d1 to d4 and d8
2. Opponent's Rook on d6 blocks one path
3. Queen-Rook become entangled

Now:
- If Queen on d4: Rook blocks
- If Queen on d8: Checkmate threat!

Force measurement by threatening the King!
```

## Defensive Entanglement

Use entanglement to complicate attacks:

```
Opponent threatens checkmate on g2

Defense:
1. Split your Knight through g2
2. Knight: 50% blocks g2, 50% elsewhere
3. Now attack is uncertain!

Attacker must consider:
- 50% chance attack fails
- 50% chance loses their piece
```

## Key Takeaways

1. Slide moves through superposed pieces create entanglement
2. Measuring one piece reveals information about entangled pieces
3. Use entanglement chains for complex tactics
4. Entanglement can be defensive too
""",
            "interactive": {
                "type": "puzzle",
                "config": {
                    "title": "Entanglement Puzzle",
                    "puzzle_type": "entanglement_tactics"
                }
            }
        },
        "measurement-timing": {
            "id": "measurement-timing",
            "title": "When to Measure",
            "content": """
# When to Measure

Knowing when to trigger measurement is a key strategic skill.

## Reasons to Delay Measurement

**Keep Options Open:**
- Superposition gives you flexibility
- Don't collapse until you must

**Maintain Threats:**
- Quantum threats are often stronger than definite ones
- Opponent must defend against all possibilities

**Information Hiding:**
- Keep opponent guessing
- Your uncertainty is their uncertainty too

## Reasons to Force Measurement

**Gain Information:**
- Learn opponent's true piece positions
- Make informed tactical decisions

**Resolve Critical Positions:**
- Before a decisive attack
- When probability favors you

**Simplify Winning Positions:**
- Reduce complexity when ahead
- Convert quantum advantage to material

## Timing Framework

```
Game Phase: Opening
→ Delay measurement, create superposition

Game Phase: Middlegame
→ Strategic measurements for tactics

Game Phase: Endgame
→ Often simplify, force measurements
```

## Forcing Opponent's Measurement

Make them measure at bad times:

```
Opponent's Queen: 50% on d4, 50% on h4

Attack d4 with a pawn!
- They must decide: Is Queen there?
- Measurement might collapse to h4
- Now d4 is safely captured for free!
```

## Key Takeaways

1. Delay measurement to maintain flexibility
2. Force measurement when probability favors you
3. Game phase affects measurement strategy
4. Force opponent's measurement at awkward times
""",
            "interactive": {
                "type": "puzzle",
                "config": {
                    "title": "When to Measure",
                    "puzzle_type": "measurement_timing"
                }
            }
        }
    },
    "cirq-introduction": {
        "cirq-setup": {
            "id": "cirq-setup",
            "title": "Setting Up Cirq",
            "content": """
# Setting Up Cirq

**Cirq** is Google's open-source framework for programming quantum computers.

## Installation

```bash
pip install cirq
```

## Basic Import

```python
import cirq
import numpy as np
```

## Your First Qubit

```python
# Create a qubit
q0 = cirq.LineQubit(0)

# Create a second qubit
q1 = cirq.LineQubit(1)

# Or create multiple at once
qubits = cirq.LineQubit.range(5)
```

## Qubit Types

```python
# LineQubit: labeled by integer
q = cirq.LineQubit(0)

# GridQubit: labeled by row, column
q = cirq.GridQubit(0, 1)

# NamedQubit: labeled by string
q = cirq.NamedQubit("my_qubit")
```

## Verifying Installation

```python
import cirq

# Create a simple circuit
qubit = cirq.LineQubit(0)
circuit = cirq.Circuit(cirq.H(qubit))

# Simulate
simulator = cirq.Simulator()
result = simulator.simulate(circuit)

print("Installation successful!")
print(f"Final state: {result.final_state_vector}")
```

## Key Takeaways

1. Install Cirq with pip
2. Create qubits with LineQubit, GridQubit, or NamedQubit
3. Cirq includes a simulator for testing
4. Perfect for quantum chess development!
""",
            "interactive": {
                "type": "code_sandbox",
                "config": {
                    "language": "python",
                    "starter_code": "import cirq\\n\\n# Create your first qubit\\nq = cirq.LineQubit(0)\\nprint(f'Created qubit: {q}')"
                }
            }
        },
        "creating-circuits": {
            "id": "creating-circuits",
            "title": "Creating Quantum Circuits",
            "content": """
# Creating Quantum Circuits

Circuits combine qubits and gates to perform quantum computations.

## Basic Circuit Creation

```python
import cirq

# Create qubits
q0, q1 = cirq.LineQubit.range(2)

# Create an empty circuit
circuit = cirq.Circuit()

# Add gates
circuit.append(cirq.H(q0))  # Hadamard on q0
circuit.append(cirq.CNOT(q0, q1))  # CNOT

print(circuit)
```

Output:
```
0: ───H───@───
          │
1: ───────X───
```

## Adding Multiple Gates

```python
# Method 1: append one at a time
circuit.append(cirq.H(q0))
circuit.append(cirq.X(q1))

# Method 2: append a list
circuit.append([cirq.H(q0), cirq.X(q1)])

# Method 3: create inline
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key='result')
)
```

## Common Gates

```python
# Single qubit gates
cirq.X(q0)    # NOT gate
cirq.Y(q0)    # Y gate
cirq.Z(q0)    # Z gate
cirq.H(q0)    # Hadamard

# Two qubit gates
cirq.CNOT(q0, q1)   # Controlled NOT
cirq.SWAP(q0, q1)   # Swap
cirq.ISWAP(q0, q1)  # iSWAP (used in Quantum Chess!)

# Parameterized gates
cirq.rx(np.pi/4)(q0)  # Rotation around X
cirq.rz(np.pi/2)(q0)  # Rotation around Z
```

## The iSWAP Gate for Chess

```python
# iSWAP is the core of Quantum Chess moves
q_source = cirq.LineQubit(0)  # Source square
q_target = cirq.LineQubit(1)  # Target square

move_circuit = cirq.Circuit(
    cirq.X(q_source),  # Place piece on source
    cirq.ISWAP(q_source, q_target)  # Move!
)

print(move_circuit)
```

## Key Takeaways

1. Circuits are sequences of gates on qubits
2. Use append() or inline creation
3. iSWAP is the key gate for chess moves
4. Cirq provides many built-in gates
""",
            "interactive": {
                "type": "code_sandbox",
                "config": {
                    "language": "python",
                    "starter_code": "import cirq\\n\\n# Create a Bell state circuit\\nq0, q1 = cirq.LineQubit.range(2)\\ncircuit = cirq.Circuit(\\n    cirq.H(q0),\\n    cirq.CNOT(q0, q1)\\n)\\nprint(circuit)"
                }
            }
        },
        "simulation": {
            "id": "simulation",
            "title": "Simulating Circuits",
            "content": """
# Simulating Quantum Circuits

Cirq includes a powerful simulator for testing quantum circuits.

## The Simulator

```python
import cirq
import numpy as np

# Create circuit
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1)
)

# Create simulator
simulator = cirq.Simulator()
```

## State Vector Simulation

Get the full quantum state:

```python
result = simulator.simulate(circuit)

# Final state vector
print(result.final_state_vector)
# Output: [0.707+0j, 0+0j, 0+0j, 0.707+0j]

# This is (|00⟩ + |11⟩)/√2
```

## Sampling (Measurement)

Simulate measurements:

```python
# Add measurement
circuit.append(cirq.measure(q0, q1, key='result'))

# Run and sample
result = simulator.run(circuit, repetitions=1000)

# Get counts
print(result.histogram(key='result'))
# Output: Counter({0: 498, 3: 502})
# 0 = |00⟩, 3 = |11⟩ (in binary)
```

## Getting Probabilities

```python
# Without measurement
result = simulator.simulate(circuit)

# Calculate probabilities
state = result.final_state_vector
probabilities = np.abs(state) ** 2

print("Probabilities:", probabilities)
# For Bell state: [0.5, 0, 0, 0.5]
```

## Simulating Chess Moves

```python
# Simulate a split move
def simulate_split_move():
    source = cirq.LineQubit(0)
    target1 = cirq.LineQubit(1)
    target2 = cirq.LineQubit(2)

    circuit = cirq.Circuit(
        # Place piece on source
        cirq.X(source),
        # Split to two targets
        cirq.ISWAP(source, target1) ** 0.5,  # √iSWAP
        cirq.ISWAP(source, target2)          # iSWAP
    )

    result = cirq.Simulator().simulate(circuit)
    probs = np.abs(result.final_state_vector) ** 2

    return probs

probs = simulate_split_move()
print("Split move probabilities:", probs)
```

## Key Takeaways

1. Simulator gives exact quantum state
2. Use run() with repetitions for sampling
3. Probabilities = |amplitude|²
4. Essential for testing Quantum Chess logic
""",
            "interactive": {
                "type": "code_sandbox",
                "config": {
                    "language": "python",
                    "starter_code": "import cirq\\nimport numpy as np\\n\\n# Simulate a quantum move\\nsource = cirq.LineQubit(0)\\ntarget = cirq.LineQubit(1)\\n\\ncircuit = cirq.Circuit(\\n    cirq.X(source),\\n    cirq.ISWAP(source, target)\\n)\\n\\nresult = cirq.Simulator().simulate(circuit)\\nprint('Final state:', result.final_state_vector)"
                }
            }
        },
        "chess-application": {
            "id": "chess-application",
            "title": "Cirq in Quantum Chess",
            "content": """
# Cirq in Quantum Chess

Let's see how Cirq powers the Quantum Chess game.

## Board Representation

```python
import cirq
import numpy as np

class QuantumBoard:
    def __init__(self):
        # 64 qubits for 64 squares
        self.qubits = [cirq.LineQubit(i) for i in range(64)]
        self.circuit = cirq.Circuit()
        self.simulator = cirq.Simulator()

    def square_to_index(self, square: str) -> int:
        col = ord(square[0]) - ord('a')
        row = int(square[1]) - 1
        return row * 8 + col
```

## Initializing the Board

```python
def initialize_board(self):
    # Place all starting pieces
    # White pieces: rows 1-2, Black pieces: rows 7-8

    starting_squares = [
        'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',  # White back rank
        'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',  # White pawns
        'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',  # Black pawns
        'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',  # Black back rank
    ]

    for square in starting_squares:
        idx = self.square_to_index(square)
        self.circuit.append(cirq.X(self.qubits[idx]))
```

## Standard Move

```python
def standard_move(self, source: str, target: str):
    source_idx = self.square_to_index(source)
    target_idx = self.square_to_index(target)

    # iSWAP exchanges the quantum state
    self.circuit.append(
        cirq.ISWAP(
            self.qubits[source_idx],
            self.qubits[target_idx]
        )
    )
```

## Split Move

```python
def split_move(self, source: str, target1: str, target2: str):
    source_idx = self.square_to_index(source)
    target1_idx = self.square_to_index(target1)
    target2_idx = self.square_to_index(target2)

    # √iSWAP creates superposition
    self.circuit.append(
        cirq.ISWAP(
            self.qubits[source_idx],
            self.qubits[target1_idx]
        ) ** 0.5
    )

    # iSWAP moves remaining amplitude
    self.circuit.append(
        cirq.ISWAP(
            self.qubits[source_idx],
            self.qubits[target2_idx]
        )
    )
```

## Getting Board Probabilities

```python
def get_probabilities(self):
    result = self.simulator.simulate(self.circuit)
    state_vector = result.final_state_vector

    # Calculate probability for each square
    probabilities = []
    # (Simplified - actual implementation more complex)
    for i in range(64):
        # Sum probabilities where qubit i is 1
        prob = calculate_marginal_probability(state_vector, i)
        probabilities.append(prob)

    return probabilities
```

## Complete Example

```python
# Create board
board = QuantumBoard()
board.initialize_board()

# Knight on g1 splits to f3 and h3
board.split_move('g1', 'f3', 'h3')

# Get probabilities
probs = board.get_probabilities()
print(f"f3 probability: {probs[board.square_to_index('f3')]}")
print(f"h3 probability: {probs[board.square_to_index('h3')]}")
# Output: ~0.5 each
```

## Key Takeaways

1. Each square is a qubit (64 total)
2. Standard moves use iSWAP
3. Split moves use √iSWAP + iSWAP
4. Simulator provides probabilities for display
""",
            "interactive": {
                "type": "code_sandbox",
                "config": {
                    "language": "python",
                    "starter_code": "import cirq\\nimport numpy as np\\n\\n# Simulate a Knight split\\ndef knight_split():\\n    g1 = cirq.LineQubit(6)   # g1 = index 6\\n    f3 = cirq.LineQubit(21)  # f3 = index 21\\n    h3 = cirq.LineQubit(23)  # h3 = index 23\\n    \\n    circuit = cirq.Circuit(\\n        cirq.X(g1),  # Knight starts on g1\\n        cirq.ISWAP(g1, f3) ** 0.5,\\n        cirq.ISWAP(g1, h3)\\n    )\\n    \\n    result = cirq.Simulator().simulate(circuit)\\n    return result\\n\\nresult = knight_split()\\nprint('Knight split simulated!')"
                }
            }
        }
    }
}


def get_module_by_id(module_id: str) -> Optional[Dict]:
    """Get a module by its ID"""
    for module in LEARNING_MODULES:
        if module['id'] == module_id:
            return module
    return None


def get_lesson(module_id: str, lesson_id: str) -> Optional[Dict]:
    """Get a specific lesson"""
    if module_id in LESSON_CONTENT:
        if lesson_id in LESSON_CONTENT[module_id]:
            return LESSON_CONTENT[module_id][lesson_id]
    return None
