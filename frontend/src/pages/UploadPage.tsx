import { useState, useCallback } from 'react';
import { Upload, FileText, Video, Headphones, CheckCircle, AlertCircle } from 'lucide-react';
import { uploadFile } from '../utils/api';

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string; summary?: string } | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setResult(null);
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      setSelectedFile(file);
      setResult(null);
    }
  }, []);

  const handleUpload = useCallback(async () => {
    if (!selectedFile) return;
    
    setIsUploading(true);
    setResult(null);
    
    try {
      const data = await uploadFile(selectedFile);
      setResult({
        success: true,
        message: `文件 "${data.filename}" 处理成功！`,
        summary: data.summary,
      });
    } catch (error) {
      setResult({
        success: false,
        message: error instanceof Error ? error.message : '处理失败，请重试',
      });
    } finally {
      setIsUploading(false);
    }
  }, [selectedFile]);

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    if (ext === 'pdf') return <FileText size={20} />;
    if (['mp4', 'avi', 'mov', 'mkv'].includes(ext || '')) return <Video size={20} />;
    if (['mp3', 'wav', 'flac', 'aac'].includes(ext || '')) return <Headphones size={20} />;
    return <FileText size={20} />;
  };

  const acceptedTypes = [
    { name: 'PDF文档', extensions: '.pdf', icon: <FileText size={16} /> },
    { name: '视频文件', extensions: '.mp4, .avi, .mov, .mkv, .flv, .wmv', icon: <Video size={16} /> },
    { name: '音频文件', extensions: '.mp3, .wav, .flac, .aac, .ogg', icon: <Headphones size={16} /> },
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">智能摘要生成</h1>
        <p className="page-subtitle">上传PDF、视频或音频文件，AI自动生成内容摘要</p>
      </div>

      <div className="image-placeholder" style={{ maxWidth: '600px', margin: '0 auto 2rem', height: '150px' }}>
        <div>
          <Upload size={36} style={{ marginBottom: '1rem', opacity: 0.6 }} />
          <div>📤 文件上传区域视觉图</div>
        </div>
      </div>

      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <div
          className={`upload-area ${isDragging ? 'dragover' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <input
            id="file-input"
            type="file"
            accept=".pdf,.mp4,.avi,.mov,.mkv,.flv,.wmv,.mp3,.wav,.flac,.aac,.ogg"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          
          <div className="upload-icon">
            <Upload size={48} />
          </div>
          <div className="upload-text">
            {selectedFile ? (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem' }}>
                {getFileIcon(selectedFile.name)}
                <span>{selectedFile.name}</span>
              </div>
            ) : (
              '点击或拖拽文件到此处上传'
            )}
          </div>
          <div className="upload-hint">
            支持 PDF、MP4、AVI、MOV、MP3、WAV 等格式
          </div>
        </div>

        {selectedFile && (
          <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
            <button
              className="btn-primary"
              onClick={handleUpload}
              disabled={isUploading}
            >
              {isUploading ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span className="loading-spinner" style={{ width: '1.25rem', height: '1.25rem' }}></span>
                  处理中...
                </span>
              ) : (
                '生成摘要'
              )}
            </button>
          </div>
        )}

        {result && (
          <div className={result.success ? 'success-message' : 'error-message'}>
            {result.success ? (
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
                <CheckCircle size={20} style={{ flexShrink: 0 }} />
                <div>
                  <div>{result.message}</div>
                  {result.summary && (
                    <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                      <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}>📝 内容摘要</div>
                      <div style={{ fontSize: '0.875rem', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
                        {result.summary}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <AlertCircle size={20} />
                {result.message}
              </div>
            )}
          </div>
        )}

        <div style={{ marginTop: '2rem', padding: '1.5rem', background: 'var(--card-bg)', borderRadius: '0.75rem' }}>
          <h3 style={{ marginBottom: '1rem', fontWeight: 600 }}>支持的文件类型</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            {acceptedTypes.map((type, index) => (
              <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ width: '2rem', height: '2rem', background: 'rgba(59,130,246,0.2)', borderRadius: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  {type.icon}
                </span>
                <div>
                  <div style={{ fontWeight: 500 }}>{type.name}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{type.extensions}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}