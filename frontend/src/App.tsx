import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import TweetsDashboard from './pages/TweetsDashboard'
import InstagramDashboard from './pages/InstagramDashboard'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">Ferta Social Media Manager</h1>
            <div className="nav-links">
              <Link to="/" className="nav-link">Tweets</Link>
              <Link to="/instagram" className="nav-link">Instagram</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<TweetsDashboard />} />
            <Route path="/instagram" element={<InstagramDashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
