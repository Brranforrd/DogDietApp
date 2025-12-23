/**
 * Example App component showing how to integrate the ChatBot
 * Replace your App.jsx or add this as a separate route/page
 */

import ChatBot from './components/ChatBot';
import './App.css';

function AppWithChat() {
  return (
    <div className="app-container">
      <header>
        <h1>🐾 WhiskerWorthy</h1>
      </header>

      <main>
        {/* Your existing content can go here */}
        
        {/* ChatBot Integration */}
        <ChatBot apiUrl="http://localhost:5000/api/chat" />
        

      </main>
    </div>
  );
}

export default AppWithChat;

