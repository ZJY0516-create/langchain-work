import { useState, useEffect } from 'react';
import { FileText, Video, Headphones, MessageCircle, BarChart3, Globe } from 'lucide-react';
import { getStats } from '../utils/api';

export default function HomePage() {
  const [stats, setStats] = useState({ total_docs: 0, total_summaries: 0, total_chats: 0 });
  
  useEffect(() => {
    getStats().then(setStats).catch(() => {});
  }, []);

  const features = [
    {
      icon: <FileText size={28} />,
      title: 'PDF智能摘要',
      description: '上传PDF文档，AI自动提取关键信息，生成简明扼要的摘要内容',
    },
    {
      icon: <Video size={28} />,
      title: '视频内容解析',
      description: '上传视频文件，自动提取音频并转录，生成视频内容摘要',
    },
    {
      icon: <Headphones size={28} />,
      title: '音频转写服务',
      description: '支持多种音频格式，精准语音转文字，生成完整文稿摘要',
    },
    {
      icon: <MessageCircle size={28} />,
      title: '智能问答系统',
      description: '基于RAG技术的知识库问答，精准匹配相关文档内容',
    },
    {
      icon: <Users size={28} />,
      title: '角色扮演对话',
      description: '多种角色可选，不同风格回复，沉浸式对话体验',
    },
    {
      icon: <Globe size={28} />,
      title: '文旅知识图谱',
      description: '丰富的文旅知识储备，带你探索世界各地的风土人情',
    },
  ];

  return (
    <div>
      <section className="hero-section">
        <div className="image-placeholder" style={{ maxWidth: '800px', margin: '0 auto 3rem', height: '250px' }}>
          <div>
            <Globe size={48} style={{ marginBottom: '1rem', opacity: 0.6 }} />
            <div style={{ fontSize: '1.125rem' }}>🏞️ 文旅智慧助手主视觉图</div>
            <div style={{ fontSize: '0.875rem', marginTop: '0.5rem', color: 'var(--text-secondary)' }}>
              请将你的文旅主题图片放在此处
            </div>
          </div>
        </div>
        
        <h1 className="hero-title">探索文旅世界</h1>
        <p className="hero-subtitle">
          智能解析文档、视频、音频，让文旅知识触手可及。上传你的资料，AI帮你提炼精华。
        </p>
        <div className="hero-cta">
          <a href="/upload" className="btn-primary">开始体验</a>
          <a href="/knowledge" className="btn-secondary">浏览知识库</a>
        </div>
      </section>

      <section className="feature-cards">
        {features.map((feature, index) => (
          <div key={index} className="feature-card">
            <div className="feature-icon">{feature.icon}</div>
            <h3 className="feature-title">{feature.title}</h3>
            <p className="feature-desc">{feature.description}</p>
          </div>
        ))}
      </section>

      <section className="stats-section">
        <div className="stats-container">
          <div className="stat-item">
            <div className="stat-number">{stats.total_docs}</div>
            <div className="stat-label">文档总数</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">{stats.total_summaries}</div>
            <div className="stat-label">摘要文档</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">{stats.total_chats}</div>
            <div className="stat-label">对话轮次</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">24/7</div>
            <div className="stat-label">全天候服务</div>
          </div>
        </div>
      </section>

      <section className="page-container">
        <h2 style={{ fontSize: '1.75rem', fontWeight: 600, marginBottom: '2rem', textAlign: 'center' }}>
          热门推荐
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
          <div className="image-placeholder" style={{ height: '200px' }}>
            <div>
              <span style={{ fontSize: '2rem' }}>🌄</span>
              <div>自然风光探索</div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>点击了解更多</div>
            </div>
          </div>
          <div className="image-placeholder" style={{ height: '200px' }}>
            <div>
              <span style={{ fontSize: '2rem' }}>🏯</span>
              <div>历史文化之旅</div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>点击了解更多</div>
            </div>
          </div>
          <div className="image-placeholder" style={{ height: '200px' }}>
            <div>
              <span style={{ fontSize: '2rem' }}>🍜</span>
              <div>美食探店指南</div>
              <div style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>点击了解更多</div>
            </div>
          </div>
        </div>
      </section>

      <footer className="footer">
        <p className="footer-text">© 2026 文旅智慧助手 - 让旅行更智慧</p>
        <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'center', gap: '2rem' }}>
          <span className="footer-text">关于我们</span>
          <span className="footer-text">使用帮助</span>
          <span className="footer-text">联系我们</span>
        </div>
      </footer>
    </div>
  );
}