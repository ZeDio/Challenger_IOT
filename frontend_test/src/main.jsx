import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Activity, Bot, Droplets, LoaderCircle, Send, Utensils } from 'lucide-react';
import './styles.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Olá! Sou o assistente CLYVO VET. Como posso ajudar com o seu pet?' }
  ]);

  async function enviarMensagem(event) {
    event?.preventDefault();
    const pergunta = message.trim();
    if (!pergunta || loading) return;

    setMessages(prev => [...prev, { role: 'user', text: pergunta }]);
    setMessage('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: pergunta })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Erro na API');
      setMessages(prev => [...prev, { role: 'assistant', text: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', text: `Não consegui processar sua pergunta. ${error.message}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <div className="container">
        <header className="title">
          <div className="brand"><Activity size={24} /><span>CLYVO VET</span></div>
          <h1>CLYVO VET Challenger</h1>
          <p>Monitoramento Inteligente de Pets</p>
        </header>

        <section className="card chat-card">
          <div className="chat-header"><div className="bot-icon"><Bot size={21}/></div><div><h2>Assistente CLYVO VET</h2><p>Consulte os dados do monitoramento por conversa</p></div><span className="online"><i/> Online</span></div>
          <div className="messages">
            {messages.map((item, index) => <div className={`message-row ${item.role}`} key={index}><div className="message"><span className="sender">{item.role === 'user' ? 'Você' : 'CLYVO VET'}</span><p>{item.text}</p></div></div>)}
            {loading && <div className="message-row assistant"><div className="message typing"><LoaderCircle className="spin" size={17}/> Consultando...</div></div>}
          </div>
          <form className="composer" onSubmit={enviarMensagem}><input value={message} onChange={e => setMessage(e.target.value)} placeholder="Digite sua pergunta sobre o seu pet..." disabled={loading}/><button type="submit" disabled={loading || !message.trim()} aria-label="Enviar"><Send size={19}/></button></form>
        </section>
      </div>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
