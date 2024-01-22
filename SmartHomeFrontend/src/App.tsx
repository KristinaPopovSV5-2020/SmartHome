import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Index from './components/Index'
import History from './components/History'
import './App.css';

function App() {
  return (
      <Router>
          <Routes>
              <Route path={'/'} element={<Index />} />
              <Route path="/history" element={<History />} />
          </Routes>
      </Router>
  );
}

export default App;
