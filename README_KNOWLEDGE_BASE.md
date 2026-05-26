# 多媒体摘要工具 + 知识库对话系统

## 🎉 功能概述

本工具结合了多媒体内容智能摘要与基于RAG技术的私有知识库对话系统。

### 核心功能

1. **多媒体摘要生成**
   - 支持PDF文档内容提取和智能摘要
   - 自动保存摘要到本地文件
   - 后续将支持视频、音频等多模态内容

2. **私有知识库 (RAG)**
   - 所有摘要自动存入知识库
   - 基于向量相似度的智能检索
   - 支持跨文档的关联问答

## 🚀 快速开始

### 1. 启动服务

```powershell
# 方式一：使用启动脚本
.\run_server.ps1

# 方式二：手动启动
$env:PYTHONPATH = "."
& "c:\Users\31639\Desktop\langchain work 5.22\venv\scripts\python.exe" -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

服务启动后访问：**http://localhost:8000**

### 2. 使用流程

#### 第一步：上传PDF生成摘要

1. 点击上传区域或拖拽PDF文件
2. 点击"上传并生成摘要"按钮
3. 等待系统处理（包含文本提取+AI摘要）
4. 查看生成的摘要内容

**自动存储：** 摘要生成后会自动存入知识库！

#### 第二步：知识库对话

在"知识库对话 (RAG)"区域：

1. **查看知识库状态**
   - 文档总数
   - 摘要文档数
   - 对话轮次

2. **智能问答**
   - 在输入框输入问题
   - 按Enter或点击"提问"按钮
   - 系统从知识库中检索相关内容
   - AI基于检索结果生成答案
   - 显示参考来源和相似度

3. **管理知识库文档**
   - 查看所有已存储的文档
   - 查看文档详情
   - 删除不需要的文档

## 📡 API接口

### 现有API

#### 上传PDF并生成摘要
```http
POST /api/summarize
Content-Type: multipart/form-data

file: <PDF文件>
```

**响应示例：**
```json
{
  "summary": "这是一段摘要内容...",
  "file_path": "/path/to/summary.txt",
  "knowledge_base_id": "uuid-xxx"
}
```

#### 单文档问答
```http
POST /api/ask
Content-Type: application/json

{
  "task_id": "原文件名.pdf",
  "question": "文档的主要内容是什么？"
}
```

### 新增RAG API

#### 知识库问答
```http
POST /api/rag/ask
Content-Type: application/json

{
  "question": "系统支持哪些功能？"
}
```

**响应示例：**
```json
{
  "answer": "系统支持PDF摘要生成、知识库存储和智能问答等功能...",
  "sources": [
    {
      "source": "Linux操作系统期末练习.pdf",
      "type": "summary",
      "score": 0.85
    }
  ],
  "retrieved_docs": [...]
}
```

#### 获取知识库统计
```http
GET /api/knowledge-base/stats
```

#### 获取知识库文档列表
```http
GET /api/knowledge-base/documents
```

#### 获取单个文档详情
```http
GET /api/knowledge-base/document/{doc_id}
```

#### 删除知识库文档
```http
DELETE /api/knowledge-base/document/{doc_id}
```

## 📁 项目结构

```
langchain work 5.22/
├── backend/
│   ├── main.py                      # 主应用入口
│   ├── config/
│   │   └── settings.py             # 配置管理
│   ├── utils/
│   │   ├── pdf_processor.py         # PDF处理
│   │   └── media_processor.py       # 媒体处理（待扩展）
│   ├── chains/
│   │   └── summary_chain.py         # 摘要生成链
│   └── knowledge_base/              # ⭐ 新增：知识库模块
│       ├── __init__.py
│       ├── vector_store.py          # 向量存储
│       ├── embeddings.py            # Embedding生成
│       └── rag_system.py            # RAG检索系统
├── frontend/
│   └── index.html                   # 前端界面（已更新）
├── uploads/                        # 上传文件目录
├── summaries/                      # 摘要保存目录
├── knowledge_base/                 # ⭐ 知识库存储目录
├── .env                           # 环境配置
├── requirements.txt                # 依赖列表
└── run_server.ps1                 # 启动脚本
```

## 💡 工作原理

### RAG检索流程

1. **文档入库**
   - PDF → 文本提取 → AI摘要 → 向量化 → 存储

2. **用户提问**
   - 用户问题 → 向量化 → 相似度检索 → 选取Top-K相关文档

3. **答案生成**
   - 检索结果 + 用户问题 → Prompt构建 → LLM生成答案 → 返回结果

### 向量相似度计算

使用TF-IDF + 余弦相似度：
- 无需外部API，本地即可计算
- 支持中英文文档
- 自动更新索引

## 🔧 配置说明

### 环境变量 (.env)

```env
DEEPSEEK_API_KEY=你的API密钥
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
MAX_TOKENS=4096
TEMPERATURE=0.3
```

### 知识库配置

知识库默认存储在 `knowledge_base/` 目录，包含：
- `documents.json` - 文档内容
- `metadata.json` - 文档元数据

## ⚠️ 注意事项

1. **API Key**
   - 确保`.env`文件中有有效的DeepSeek API Key
   - API Key仅用于摘要生成和RAG问答

2. **PDF限制**
   - 当前仅支持文本型PDF
   - 扫描件PDF无法提取文本

3. **知识库容量**
   - 当前使用本地JSON存储
   - 适合小规模个人使用
   - 大规模应用建议迁移到ChromaDB/FAISS

4. **性能**
   - 摘要生成约需10-30秒（取决于文档长度）
   - RAG问答约需5-15秒
   - 知识库检索为毫秒级

## 🛠️ 故障排除

### 常见问题

1. **端口被占用**
   - 修改`run_server.ps1`中的端口号
   - 或使用：`python -m uvicorn backend.main:app --port 8001`

2. **模块导入错误**
   - 确保设置PYTHONPATH： `$env:PYTHONPATH = "."`
   - 检查是否在项目根目录运行

3. **API Key错误**
   - 检查`.env`文件
   - 确认API Key格式正确
   - 确认API Key有足够额度

4. **知识库为空**
   - 需要先上传PDF生成摘要
   - 摘要会自动存入知识库
   - 可以通过API手动添加文档

## 📋 下一步计划

- [ ] 支持更多文档格式（Word、PPT等）
- [ ] 添加视频/音频转录和摘要
- [ ] 集成更强大的向量数据库（ChromaDB）
- [ ] 支持多用户和权限管理
- [ ] 添加文档分类和标签功能
- [ ] 实现增量更新而非全量覆盖

## 🎓 技术栈

- **后端**: FastAPI + Uvicorn
- **前端**: 原生HTML/CSS/JavaScript
- **AI模型**: DeepSeek API (GPT兼容)
- **向量存储**: 本地JSON + TF-IDF
- **PDF处理**: PyPDF2

## 📝 许可证

MIT License

---

**享受智能文档处理与知识库对话的便捷！** 🚀
