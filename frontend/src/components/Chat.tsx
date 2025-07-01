import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';

interface ChatMessage {
  id: number;
  sender_id: number;
  sender_name: string;
  content: string;
  timestamp: string;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const { isAuthenticated } = useAuth();
  const [userId, setUserId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!isAuthenticated) return;
    // User-ID dynamisch aus dem Token holen
    const token = localStorage.getItem('access');
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      setUserId(payload.user_id);
      ws.current = new WebSocket('ws://' + window.location.host + '/ws/chat/?token=' + token);
      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'chat_message') {
          setMessages(prev => [...prev, {
            id: Date.now(),
            sender_id: data.user_id,
            sender_name: data.username,
            content: data.message,
            timestamp: data.timestamp
          }]);
        }
      };
    }
    return () => { ws.current?.close(); };
  }, [isAuthenticated]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (newMessage.trim() && ws.current && userId) {
      ws.current.send(JSON.stringify({ message: newMessage, user_id: userId }));
      setNewMessage('');
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map(msg => (
          <div key={msg.id} className={msg.sender_id === userId ? 'my-message' : 'other-message'}>
            <div className="message-header">
              <span className="sender-name">{msg.sender_name}</span>
              <span className="timestamp">{msg.timestamp}</span>
            </div>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form className="chat-input" onSubmit={handleSend}>
        <input
          type="text"
          value={newMessage}
          onChange={e => setNewMessage(e.target.value)}
          placeholder="Nachricht eingeben..."
        />
        <button type="submit">Senden</button>
      </form>
    </div>
  );
};

export default Chat;
