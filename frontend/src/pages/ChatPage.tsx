import { useState, useEffect, useRef, useCallback } from 'react';
import { Send, MessageSquare, RefreshCw, FileText, Video, Headphones } from 'lucide-react';
import { chatWithKB, getDocuments, formatFileSize } from '../utils/api';
import type { Document, Message } from '../utils/api';

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocs, setSelectedDocs] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getDocuments().then(setDocuments).catch(() => {});
  }, []);

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
      const response = await chatWithKB(input, selectedDocs);
      
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
  }, [input, isLoading, selectedDocs]);

  const handleKeyPress = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  const toggleDocSelection = (docId: string) => {
    setSelectedDocs(prev => 
      prev.includes(docId) 
        ? prev.filter(id => id !== docId)
        : [...prev, docId]
    );
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf': return <FileText size={16} />;
      case 'video': return <Video size={16} />;
      case 'audio': return <Headphones size={16} />;
      default: return <FileText size={16} />;
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">智能问答</h1>
        <p className="page-subtitle">基于知识库的智能问答系统，精准匹配相关文档内容</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: '2rem' }}>
        <div className="chat-container">
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                <MessageSquare size={48} style={{ opacity: 0.4, marginBottom: '1rem' }} />
                <div>你好！我是你的智能助手</div>
                <div style={{ marginTop: '0.5rem', fontSize: '0.875rem' }}>
                  可以从右侧选择文档，然后向我提问
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
              disabled={isLoading}
            />
            <button
              className="btn-primary"
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
            >
              <Send size={18} />
            </button>
          </div>
        </div>

        <div style={{ background: 'var(--card-bg)', borderRadius: '1rem', padding: '1.5rem', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h3 style={{ fontWeight: 600 }}>📄 选择文档</h3>
            <button
              onClick={() => getDocuments().then(setDocuments).catch(() => {})}
              className="btn-secondary"
              style={{ padding: '0.375rem 0.75rem', fontSize: '0.875rem' }}
            >
              <RefreshCw size={14} />
            </button>
          </div>

          {documents.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
              <FileText size={32} style={{ opacity: 0.4, marginBottom: '0.5rem' }} />
              <div>暂无文档</div>
              <a href="/upload" style={{ color: 'var(--primary-light)', fontSize: '0.875rem' }}>点击上传</a>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '400px', overflowY: 'auto' }}>
              {documents.map((doc) => (
                <label
                  key={doc.id}
                  style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '0.75rem', 
                    padding: '0.75rem',
                    background: selectedDocs.includes(doc.id) ? 'rgba(59,130,246,0.3)' : 'transparent',
                    border: `1px solid ${selectedDocs.includes(doc.id) ? 'var(--primary-light)' : 'var(--border-color)'}`,
                    borderRadius: '0.5rem',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease'
                  }}
                >
                  <input
                    type="checkbox"
                    checked={selectedDocs.includes(doc.id)}
                    onChange={() => toggleDocSelection(doc.id)}
                    style={{ accentColor: 'var(--primary-light)' }}
                  />
                  <span>{getFileIcon(doc.type)}</span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: '0.875rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {doc.filename}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                      {formatFileSize(doc.size)}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          )}

          {selectedDocs.length > 0 && (
            <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)' }}>
              <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                已选择 {selectedDocs.length} 个文档
              </div>
              <button
                onClick={() => setSelectedDocs([])}
                className="btn-close"
                style={{ marginTop: '0.75rem', fontSize: '0.75rem' }}
              >
                清除选择
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}