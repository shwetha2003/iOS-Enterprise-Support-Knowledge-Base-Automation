import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

// Components
import Header from './components/Header';
import MobileView from './components/MobileView';
import Home from './pages/Home';
import KnowledgeBasePage from './pages/KnowledgeBasePage';
import DashboardPage from './pages/DashboardPage';
import ToolsPage from './pages/ToolsPage';

function App() {
  const [isMobileView, setIsMobileView] = useState(false);

  useEffect(() => {
    // Check if user is on mobile device
    const checkMobile = () => {
      setIsMobileView(window.innerWidth <= 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <Router>
      <div className="App">
        <Header />
        
        {isMobileView ? (
          <MobileView />
        ) : (
          <>
            <nav className="main-nav">
              <Link to="/">Home</Link>
              <Link to="/knowledge-base">Knowledge Base</Link>
              <Link to="/tools">Troubleshooting Tools</Link>
              <Link to="/dashboard">Dashboard</Link>
            </nav>
            
            <main className="content">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/knowledge-base" element={<KnowledgeBasePage />} />
                <Route path="/tools" element={<ToolsPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
              </Routes>
            </main>
          </>
        )}
        
        <footer className="footer">
          <p>© 2024 iOS Enterprise Support Portal | IT Department</p>
          <p>For urgent issues, contact IT Support: x5555</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
