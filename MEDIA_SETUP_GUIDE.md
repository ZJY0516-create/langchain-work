# 多媒体摘要工具 - 安装说明

## 📋 当前状态

✅ **服务器已启动成功！** 你可以使用PDF摘要功能！

## 🎯 功能说明

### 已启用的功能
- ✅ PDF 文件摘要生成
- ✅ 知识库存储与检索
- ✅ RAG 智能问答
- ✅ 角色扮演AI助手

### 待安装启用的功能
- 📹 视频文件处理 (MP4, AVI, MOV, MKV, FLV, WMV)
- 🎵 音频文件处理 (MP3, WAV, FLAC, AAC, OGG)

## 🛠️ 安装视频/音频处理依赖

### 方法1: 使用提供的安装脚本

在项目目录下运行：

```powershell
# Windows PowerShell
.\install_media_deps.ps1
```

### 方法2: 手动安装

在你的虚拟环境中运行：

```powershell
# 激活虚拟环境
.\new_venv\Scripts\Activate.ps1

# 安装依赖
pip install moviepy
pip install openai-whisper
pip install ffmpeg-python
```

### 方法3: 完整安装（推荐）

```powershell
# 激活虚拟环境
.\new_venv\Scripts\Activate.ps1

# 安装所有多媒体处理依赖
pip install moviepy openai-whisper ffmpeg-python

# 验证安装
python -c "import moviepy; import whisper; print('依赖安装成功！')"
```

## 📝 使用说明

### 1. 启动服务器
```powershell
.\new_venv\Scripts\Activate.ps1
$env:PYTHONPATH = '.'
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 2. 使用方法
- 访问 http://localhost:8000
- 选择 PDF/视频/音频文件上传
- 系统自动生成摘要并存入知识库
- 使用聊天功能与知识库内容对话

## ⚠️ 注意事项

1. **首次使用 Whisper 会下载模型**（约 700MB - 1.5GB），请确保网络连接
2. **处理大文件时需要耐心**，音频/视频转录可能需要较长时间
3. **需要 ffmpeg 系统支持**，moviepy 通常会自动处理
4. 如果遇到 ffmpeg 问题，可以单独安装 ffmpeg 并添加到系统 PATH

## 🔧 故障排除

### 问题1: 提示媒体处理功能未启用
**解决方案**: 运行 `pip install moviepy openai-whisper ffmpeg-python`

### 问题2: Whisper 模型下载失败
**解决方案**: 可以手动下载模型到 `~/.cache/whisper/` 目录

### 问题3: ffmpeg 错误
**解决方案**: 从 https://ffmpeg.org/download.html 下载安装

## 📂 文件结构

```
langchain work 5.22/
├── backend/
│   ├── utils/
│   │   ├── pdf_processor.py      # PDF处理
│   │   └── media_processor.py    # 音视频处理（新增）
│   ├── knowledge_base/
│   └── main.py
├── frontend/
├── uploads/
└── summaries/
```

## 🎉 完成

所有依赖安装完成后，重启服务器即可享受完整的多媒体摘要功能！
