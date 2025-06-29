import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router'
import Index from './pages/Index'
import Quiz from './pages/Quiz'

function App() {


  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Index />} />
        <Route path='/quiz/:id/:title/:duration' element={<Quiz />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
