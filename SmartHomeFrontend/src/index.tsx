import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';  // Adjust the import path based on the current directory
import reportWebVitals from './reportWebVitals';  // Adjust the import path based on the current directory

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();
