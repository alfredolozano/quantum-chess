import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { HomePage } from './pages/HomePage'
import { PlayPage } from './pages/PlayPage'
import { LearnPage } from './pages/LearnPage'
import { LessonPage } from './pages/LessonPage'
import { GamePage } from './pages/GamePage'
import { LobbyPage } from './pages/LobbyPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="play" element={<PlayPage />} />
          <Route path="play/lobby" element={<LobbyPage />} />
          <Route path="play/game/:gameId" element={<GamePage />} />
          <Route path="learn" element={<LearnPage />} />
          <Route path="learn/:moduleId/:lessonId" element={<LessonPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
