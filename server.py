# coding: utf-8
"""
LangChain Server (langserve) 部署文件
基于 LangChain 框架实现大模型应用开发
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import shutil
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from backend.config.settings import settings, UPLOAD_DIR, SUMMARIES_DIR
from backend.utils.pdf_processor import extract_text_from_pdf, save_summary_to_file
from backend.chains.summary_chain import SummaryChain
from backend.knowledge_base.rag_system import rag_system

process_media_file = None
check_ffmpeg_available = None
check_whisper_installed = None
try:
    from backend.utils.media_processor import process_media_file, check_ffmpeg_available, check_whisper_installed
    logger.info("媒体处理模块加载成功")
except Exception as e:
    logger.warning(f"媒体处理模块加载失败: {e}")
    process_media_file = None

app = FastAPI(
    title="文旅智答 - 面向文旅场景的 LangChain 智能对话助手",
    description="基于LangChain框架的多媒体摘要与智能问答系统",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

summary_chain = SummaryChain()

class ChatRequest(BaseModel):
    message: str
    document_ids: list = []
    role: str = ""
    style: str = ""

class ChatResponse(BaseModel):
    response: str

class UploadResponse(BaseModel):
    summary: str
    filename: str

@app.post("/api/upload", response_model=UploadResponse)
def upload_and_summarize(file: UploadFile = File(...)):
    """上传文件并生成摘要 - 支持PDF、视频、音频"""
    try:
        logger.info(f"处理文件: {file.filename}")
        
        file_ext = Path(file.filename).suffix.lower()
        file_path = UPLOAD_DIR / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if file_ext == ".pdf":
            text = extract_text_from_pdf(str(file_path))
        elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mp3', '.wav', '.flac', '.aac', '.ogg']:
            if process_media_file is None:
                os.remove(file_path)
                raise HTTPException(status_code=400, detail="媒体处理功能未启用")
            
            text = process_media_file(str(file_path.resolve()))
        else:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="不支持的文件格式")
        
        if not text.strip():
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="未提取到内容")
        
        summary = summary_chain.create_summary(text)
        
        save_summary_to_file(summary, file.filename, SUMMARIES_DIR)
        
        rag_system.add_to_knowledge_base(
            content=summary,
            source=file.filename,
            doc_type="summary",
            metadata={"original_length": len(text), "summary_length": len(summary)}
        )
        
        os.remove(file_path)
        
        return {"summary": summary, "filename": file.filename}
    
    except Exception as e:
        logger.error(f"上传处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_kb(request: ChatRequest):
    """基于知识库的智能问答 - 支持角色和风格选择（同步版本）"""
    try:
        result = rag_system.answer_with_rag(
            request.message,
            request.document_ids,
            request.role,
            request.style
        )
        return {"response": result["answer"]}
    except Exception as e:
        logger.error(f"问答失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge-base/documents")
async def get_documents():
    """获取知识库文档列表"""
    try:
        docs = []
        for doc in rag_system.documents:
            filename = doc.get("source", "unknown")
            content = doc.get("content", "")
            docs.append({
                "id": doc["id"],
                "filename": filename,
                "summary": content[:200] + "..." if len(content) > 200 else content,
                "size": len(content)
            })
        return docs
    except Exception as e:
        logger.error(f"获取文档失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge-base/stats")
async def get_stats():
    """获取知识库统计"""
    try:
        total_docs = len(list(SUMMARIES_DIR.iterdir())) if SUMMARIES_DIR.exists() else 0
        return {"total_docs": total_docs, "total_summaries": total_docs, "total_chats": 0}
    except Exception as e:
        logger.error(f"获取统计失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/roles")
async def get_roles():
    """获取角色列表"""
    return rag_system.get_available_roles()

@app.get("/api/styles")
async def get_styles():
    """获取风格列表"""
    return rag_system.get_available_styles()

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "LangChain Server"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)