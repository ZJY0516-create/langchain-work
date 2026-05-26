import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import KnowledgePage from './pages/KnowledgePage';
import ChatPage from './pages/ChatPage';
import RoleplayPage from './pages/RoleplayPage';

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <main style={{ minHeight: 'calc(100vh - 65px)' }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/knowledge" element={<KnowledgePage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/roleplay" element={<RoleplayPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

const root = createRoot(document.getElementById('root')!);
root.render(<App />);