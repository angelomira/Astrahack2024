// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Registration from './Registration';
import Chat from './Chat';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/registration" element={<Registration />} />
        <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

function ProtectedRoute() {
  const isLoggedIn = localStorage.getItem('loggedInUser');

  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }
  return <Chat />;
}
export default App;
