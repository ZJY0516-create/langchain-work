import { useState, useEffect, useRef, useCallback } from 'react';
import { Send, MessageSquare, MapPin, BookOpen, UtensilsCrossed, Users, Camera, Compass, RefreshCw } from 'lucide-react';
import { chatWithKB, roles, styles } from '../utils/api';
import type { Message } from '../utils/api';

const iconMap: { [key: string]: React.ReactNode } = {
  MapPin: <MapPin size={32} />,
  BookOpen: <BookOpen size={32} />,
  UtensilsCrossed: <UtensilsCrossed size={32} />,
  Users: <Users size={32} />,
  Camera: <Camera size={32} />,
  Compass: <Compass size={32} />,
};

export default function RoleplayPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedRole, setSelectedRole] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('normal');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = useCallback(async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatWithKB(input, [], selectedRole, selectedStyle);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response,
        role: 'bot',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: error instanceof Error ? error.message : '抱歉，发生了错误',
        role: 'bot',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, selectedRole, selectedStyle]);

  const handleKeyPress = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  const resetChat = () => {
    setMessages([]);
    setSelectedRole('');
    setSelectedStyle('normal');
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">角色扮演助手</h1>
        <p className="page-subtitle">选择不同角色和风格，体验沉浸式对话</p>
      </div>

      <div className="image-placeholder" style={{ maxWidth: '600px', margin: '0 auto 2rem', height: '120px' }}>
        <div>
          <Users size={36} style={{ marginBottom: '1rem', opacity: 0.6 }} />
          <div>🎭 角色扮演界面视觉图</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: '2rem' }}>
        <div className="chat-container">
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                <Users size={48} style={{ opacity: 0.4, marginBottom: '1rem' }} />
                <div>选择一个角色开始对话</div>
                <div style={{ marginTop: '0.5rem', fontSize: '0.875rem' }}>
                  从右侧选择角色和说话风格
                </div>
              </div>
            ) : (
              messages.map((msg) => (
                <div key={msg.id} className={`chat-message ${msg.role}`}>
                  <div className="chat-bubble">{msg.content}</div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="chat-message bot">
                <div className="chat-bubble">
                  <div className="loading-spinner" style={{ width: '1.25rem', height: '1.25rem', margin: '0 auto' }}></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="chat-input-area">
            <input
              type="text"
              className="chat-input"
              placeholder="输入你的问题..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading || !selectedRole}
            />
            <button
              className="btn-primary"
              onClick={handleSend}
              disabled={isLoading || !input.trim() || !selectedRole}
            >
              <Send size={18} />
            </button>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <div style={{ background: 'var(--card-bg)', borderRadius: '1rem', padding: '1.5rem', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h3 style={{ fontWeight: 600 }}>👤 选择角色</h3>
              <button
                onClick={resetChat}
                className="btn-secondary"
                style={{ padding: '0.375rem 0.75rem', fontSize: '0.875rem' }}
              >
                <RefreshCw size={14} /> 重置
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
              {roles.map((role) => (
                <div
                  key={role.id}
                  onClick={() => setSelectedRole(role.id)}
                  className={`role-card ${selectedRole === role.id ? 'selected' : ''}`}
                  style={{ padding: '1rem' }}
                >
                  <div className="role-icon" style={{ width: '3.5rem', height: '3.5rem', fontSize: '1.5rem' }}>
                    {iconMap[role.icon] || <Users size={24} />}
                  </div>
                  <div style={{ fontWeight: 500, fontSize: '0.9rem' }}>{role.name}</div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                    {role.description}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div style={{ background: 'var(--card-bg)', borderRadius: '1rem', padding: '1.5rem', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontWeight: 600, marginBottom: '1rem' }}>🎨 说话风格</h3>

            <div style={{ display: 'flex', flexWrap: 'wrap' }}>
              {styles.map((style) => (
                <div
                  key={style.id}
                  onClick={() => setSelectedStyle(style.id)}
                  className={`style-badge ${selectedStyle === style.id ? 'selected' : ''}`}
                >
                  {style.name}
                </div>
              ))}
            </div>
          </div>

          {selectedRole && (
            <div style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.3) 0%, rgba(5,150,105,0.3) 100%)', borderRadius: '1rem', padding: '1.5rem', border: '1px solid var(--border-color)' }}>
              <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}>✨ 当前角色</div>
              <div style={{ fontSize: '1.25rem', fontWeight: 600 }}>
                {roles.find(r => r.id === selectedRole)?.name}
              </div>
              <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                {roles.find(r => r.id === selectedRole)?.description}
              </div>
              <div style={{ marginTop: '0.75rem', fontSize: '0.875rem' }}>
                风格: <span style={{ color: 'var(--accent-color)' }}>{styles.find(s => s.id === selectedStyle)?.name}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}