import { useState, useEffect } from 'react';
import { FileText, Video, Headphones, Calendar, FolderOpen, RefreshCw } from 'lucide-react';
import { getDocuments, formatFileSize, formatDate } from '../utils/api';
import type { Document } from '../utils/api';

export default function KnowledgePage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedType, setSelectedType] = useState<'all' | 'pdf' | 'video' | 'audio'>('all');

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const docs = await getDocuments();
      setDocuments(docs);
    } catch (error) {
      console.error('Failed to fetch documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredDocs = selectedType === 'all' 
    ? documents 
    : documents.filter(doc => doc.type === selectedType);

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf': return <FileText size={20} />;
      case 'video': return <Video size={20} />;
      case 'audio': return <Headphones size={20} />;
      default: return <FileText size={20} />;
    }
  };

  const getFileTypeLabel = (type: string) => {
    switch (type) {
      case 'pdf': return 'PDF文档';
      case 'video': return '视频文件';
      case 'audio': return '音频文件';
      default: return '未知类型';
    }
  };

  const tabs = [
    { id: 'all', label: '全部' },
    { id: 'pdf', label: 'PDF', icon: <FileText size={16} /> },
    { id: 'video', label: '视频', icon: <Video size={16} /> },
    { id: 'audio', label: '音频', icon: <Headphones size={16} /> },
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">知识库管理</h1>
        <p className="page-subtitle">查看和管理已上传的文档及其摘要内容</p>
      </div>

      <div className="image-placeholder" style={{ maxWidth: '800px', margin: '0 auto 2rem', height: '120px' }}>
        <div>
          <FolderOpen size={36} style={{ marginBottom: '1rem', opacity: 0.6 }} />
          <div>📚 知识库概览视觉图</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSelectedType(tab.id as any)}
            className={`btn-secondary ${selectedType === tab.id ? '' : ''}`}
            style={{ 
              background: selectedType === tab.id ? 'rgba(59,130,246,0.3)' : 'transparent',
              borderColor: selectedType === tab.id ? 'var(--primary-light)' : '',
            }}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
        <button
          onClick={fetchDocuments}
          className="btn-secondary"
          style={{ marginLeft: 'auto' }}
        >
          <RefreshCw size={16} /> 刷新
        </button>
      </div>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '4rem' }}>
          <div className="loading-spinner"></div>
        </div>
      ) : filteredDocs.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '4rem', background: 'var(--card-bg)', borderRadius: '1rem' }}>
          <FolderOpen size={48} style={{ opacity: 0.4, marginBottom: '1rem' }} />
          <div style={{ fontSize: '1.125rem', marginBottom: '0.5rem' }}>暂无文档</div>
          <div style={{ color: 'var(--text-secondary)' }}>
            <a href="/upload" style={{ color: 'var(--primary-light)' }}>点击上传</a> 你的第一个文件
          </div>
        </div>
      ) : (
        <div className="doc-list">
          {filteredDocs.map((doc) => (
            <div key={doc.id} className="doc-card">
              <div className="doc-header">
                <div className="doc-icon">{getFileIcon(doc.type)}</div>
                <div>
                  <div className="doc-name">{doc.filename}</div>
                  <div className="doc-meta">
                    <span style={{ marginRight: '1rem' }}>{getFileTypeLabel(doc.type)}</span>
                    <span>{formatFileSize(doc.size)}</span>
                  </div>
                </div>
              </div>
              <div className="doc-meta" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Calendar size={14} />
                {formatDate(doc.uploaded_at)}
              </div>
              {doc.summary && (
                <div className="doc-summary">
                  <div style={{ fontWeight: 500, marginBottom: '0.5rem', color: 'var(--text-primary)' }}>📝 摘要</div>
                  {doc.summary}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}