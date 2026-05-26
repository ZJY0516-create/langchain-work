# 文旅智答 - 部署指南

## 项目概述

这是一个基于 LangChain 的文旅智能问答系统，支持文档上传、智能问答和角色扮演功能。

## 目录结构

```
├── backend/              # 后端代码
│   ├── langchain/        # LangChain 核心模块
│   ├── chains/           # 链式调用模块
│   ├── knowledge_base/   # 知识库系统
│   ├── utils/            # 工具函数
│   └── config/           # 配置文件
├── frontend/             # React 前端
├── server_langserve.py   # LangServe 部署入口
├── requirements.txt      # 依赖清单
├── Dockerfile            # Docker 配置
├── fly.toml              # Fly.io 配置
└── render.yaml           # Render 配置
```

## 本地开发

### 环境要求

- Python 3.12+
- Node.js 18+ (仅前端开发)

### 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件：

```env
DEESEEK_API_KEY=your-deepseek-api-key
DEESEEK_BASE_URL=https://api.deepseek.com/v1
DEESEEK_MODEL=deepseek-chat
TEMPERATURE=0.7
MAX_TOKENS=4096
```

### 启动开发服务器

```bash
# 方式一：直接运行
python server_langserve.py

# 方式二：使用 uvicorn
uvicorn server_langserve:app --host 0.0.0.0 --port 8000 --reload
```

访问地址：http://localhost:8000

## 部署到 GitHub

### 1. 创建仓库

```bash
# 初始化 git
git init

# 添加文件
git add .

# 提交
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/your-username/your-repo-name.git

# 推送到 GitHub
git push -u origin main
```

### 2. GitHub Actions CI/CD

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: pytest
```

## 部署到云端平台

### 选项一：Fly.io (推荐)

#### 1. 安装 Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# macOS/Linux
curl -L https://fly.io/install.sh | sh
```

#### 2. 登录

```bash
fly auth login
```

#### 3. 部署

```bash
# 创建应用
fly launch

# 设置环境变量
fly secrets set DEESEEK_API_KEY=your-api-key
fly secrets set DEESEEK_BASE_URL=https://api.deepseek.com/v1

# 部署
fly deploy
```

### 选项二：Render

#### 1. 创建账户

访问 https://render.com 并注册账户

#### 2. 创建 Web Service

- **Repository**: 选择你的 GitHub 仓库
- **Branch**: main
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn server_langserve:app --host 0.0.0.0 --port $PORT --workers 4`

#### 3. 设置环境变量

在 Render 控制台添加以下环境变量：
- DEESEEK_API_KEY
- DEESEEK_BASE_URL
- DEESEEK_MODEL
- TEMPERATURE
- MAX_TOKENS

### 选项三：Docker

#### 1. 构建镜像

```bash
docker build -t wenlv-chatbot .
```

#### 2. 运行容器

```bash
docker run -d -p 8000:8000 \
  -e DEESEEK_API_KEY=your-api-key \
  -e DEESEEK_BASE_URL=https://api.deepseek.com/v1 \
  wenlv-chatbot
```

#### 3. 推送到 Docker Hub

```bash
docker tag wenlv-chatbot your-username/wenlv-chatbot
docker push your-username/wenlv-chatbot
```

## API 接口

### 文件上传

```bash
POST /api/upload
Content-Type: multipart/form-data

# 示例
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.pdf"
```

### 智能问答

```bash
POST /api/chat
Content-Type: application/json

{
  "message": "你的问题",
  "document_ids": [],
  "role": "tour_guide",
  "style": "normal"
}
```

### LangChain Chain 路由

- `/chain/summary` - 文档摘要链
- `/chain/qa` - 问答链
- `/chain/summary/playground/` - 摘要链测试界面
- `/chain/qa/playground/` - 问答链测试界面

## 环境变量说明

| 变量名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| DEESEEK_API_KEY | string | - | DeepSeek API 密钥 |
| DEESEEK_BASE_URL | string | https://api.deepseek.com/v1 | API 基础地址 |
| DEESEEK_MODEL | string | deepseek-chat | 模型名称 |
| TEMPERATURE | float | 0.7 | 温度参数 |
| MAX_TOKENS | int | 4096 | 最大 token 数 |

## 注意事项

1. **API 密钥安全**: 不要将 API 密钥提交到版本控制
2. **文件大小限制**: 默认上传文件大小限制为 50MB
3. **内存使用**: 建议至少 1GB 内存
4. **并发处理**: 生产环境建议使用多个 worker 进程

## 故障排除

### 常见问题

1. **端口被占用**:
   ```bash
   lsof -ti:8000 | xargs kill -9  # macOS/Linux
   taskkill /F /PID <pid>          # Windows
   ```

2. **依赖安装失败**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   ```

3. **环境变量未加载**:
   - 确保 `.env` 文件存在于项目根目录
   - 检查环境变量名称是否正确

## 许可证

MIT License