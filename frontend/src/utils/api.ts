export interface Document {
  id: string;
  filename: string;
  type: 'pdf' | 'video' | 'audio';
  summary: string;
  uploaded_at: string;
  size: number;
}

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'bot';
  timestamp: string;
}

export interface Role {
  id: string;
  name: string;
  description: string;
  icon: string;
}

export const API_BASE_URL = 'http://localhost:8000';

export async function uploadFile(file: File): Promise<{ summary: string; filename: string }> {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/api/upload`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || '上传失败');
  }
  
  return response.json();
}

export async function getDocuments(): Promise<Document[]> {
  const response = await fetch(`${API_BASE_URL}/api/knowledge-base/documents`);
  
  if (!response.ok) {
    throw new Error('获取文档列表失败');
  }
  
  return response.json();
}

export async function getStats(): Promise<{ total_docs: number; total_summaries: number; total_chats: number }> {
  const response = await fetch(`${API_BASE_URL}/api/knowledge-base/stats`);
  
  if (!response.ok) {
    throw new Error('获取统计数据失败');
  }
  
  return response.json();
}

export async function chatWithKB(
  message: string,
  selectedDocs: string[] = [],
  role: string = '',
  style: string = ''
): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      document_ids: selectedDocs,
      role,
      style,
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || '对话失败');
  }
  
  const data = await response.json();
  return data.response;
}

export const roles: Role[] = [
  { id: 'tour_guide', name: '导游', description: '专业的旅游向导，熟悉各大景点', icon: 'MapPin' },
  { id: 'historian', name: '历史学家', description: '精通历史文化，讲解深入浅出', icon: 'BookOpen' },
  { id: 'foodie', name: '美食家', description: '美食达人，推荐地道美味', icon: 'UtensilsCrossed' },
  { id: 'local', name: '本地居民', description: '本地人视角，分享地道玩法', icon: 'Users' },
  { id: 'photographer', name: '摄影师', description: '摄影专家，分享拍摄技巧', icon: 'Camera' },
  { id: 'adventurer', name: '探险家', description: '户外探险爱好者，分享攻略', icon: 'Compass' },
];

export const styles = [
  { id: 'normal', name: '标准' },
  { id: 'elderly', name: '老年友好' },
  { id: 'kids', name: '儿童友好' },
  { id: 'meme', name: '网络热梗' },
];

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}