# 文旅智慧助手 - LangChain 大模型应用

基于 LangChain 框架开发的多媒体摘要与智能问答系统，支持 PDF、视频、音频等多种格式的智能处理。

## 技术架构

### 后端 (LangChain Server)
- **框架**: FastAPI + LangChain
- **核心组件**:
  - LLM 调用 (DeepSeek API)
  - Prompt 工程
  - Chain 链式调用
  - RAG (Retrieval-Augmented Generation)
  - 向量数据库 (FAISS)

### 前端
- **技术栈**: 原生 HTML/CSS/JavaScript
- **特点**: 清新浅色调、响应式设计、无需构建工具

## 功能特性

1. **多媒体摘要生成**
   - PDF文档智能摘要
   - 视频内容解析 (使用 Whisper 语音转文字)
   - 音频文件转写

2. **知识库管理**
   - 文档存储与检索
   - 语义搜索增强

3. **智能问答系统**
   - RAG 技术支持
   - 多文档关联问答

4. **角色扮演AI助手**
   - 6种角色选择 (导游、历史学家、美食家、本地居民、摄影师、探险家)
   - 4种说话风格 (标准、老年友好、儿童友好、网络热梗)

## 快速开始

### 环境要求
- Python 3.10+
- 依赖包: 见 requirements.txt

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件:

```env
DEEPSEEK_API_KEY=your_api_key_here
```

### 启动服务

```bash
python server.py
```

服务将在 `http://localhost:8000` 运行

### API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/upload` | POST | 上传文件并生成摘要 |
| `/api/chat` | POST | 基于知识库的智能问答 |
| `/api/knowledge-base/documents` | GET | 获取文档列表 |
| `/api/knowledge-base/stats` | GET | 获取知识库统计 |
| `/api/roles` | GET | 获取角色列表 |
| `/api/styles` | GET | 获取风格列表 |
| `/api/health` | GET | 健康检查 |

## 项目结构

```
.
├── backend/
│   ├── chains/           # LangChain 链定义
│   │   └── summary_chain.py
│   ├── config/          # 配置文件
│   │   └── settings.py
│   ├── knowledge_base/  # RAG 知识库系统
│   │   ├── rag_system.py
│   │   ├── vector_store.py
│   │   └── role_style_system.py
│   ├── utils/           # 工具模块
│   │   ├── pdf_processor.py
│   │   └── media_processor.py
│   ├── uploads/         # 上传文件目录
│   ├── summaries/       # 摘要文件目录
│   └── main.py          # 原始 FastAPI 应用
├── frontend/
│   └── index.html       # 单页面前端应用
├── server.py            # LangChain Server 部署文件
└── requirements.txt     # 依赖列表
```

## LangChain 核心要素实现

### 1. LLM 调用
```python
from langchain.chat_models import ChatDeepSeek
llm = ChatDeepSeek(model="deepseek-chat", api_key=api_key)
```

### 2. Prompt 工程
使用结构化提示模板，支持多角色和多风格定制

### 3. Chain 链式调用
```python
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
```

### 4. RAG (检索增强生成)
结合 FAISS 向量数据库实现语义检索

### 5. Memory 记忆机制
支持对话历史管理

## 许可证

MIT License

## 参考项目

本项目基于以下开源项目构建:
- [LangChain](https://github.com/langchain-ai/langchain) - 大模型应用开发框架
- [FastAPI](https://github.com/tiangolo/fastapi) - 高性能 API 框架
- [FAISS](https://github.com/facebookresearch/faiss) - 向量数据库
- [Whisper](https://github.com/openai/whisper) - 语音转文字模型