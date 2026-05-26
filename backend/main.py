# coding: utf-8
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import shutil
import os
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from backend.config.settings import settings, UPLOAD_DIR, SUMMARIES_DIR
from backend.utils.pdf_processor import extract_text_from_pdf, save_summary_to_file
from backend.chains.summary_chain import SummaryChain
from backend.knowledge_base import rag_system

# 尝试导入媒体处理模块，如果失败则禁用该功能
process_media_file = None
check_ffmpeg_available = None
check_whisper_installed = None
try:
    from backend.utils.media_processor import process_media_file, check_ffmpeg_available, check_whisper_installed
    logger.info("媒体处理模块加载成功")
except Exception as e:
    logger.warning(f"媒体处理模块加载失败: {e}")
    process_media_file = None

app = FastAPI(title="多媒体摘要工具", description="基于DeepSeek的PDF智能摘要与问答系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

summary_chain = SummaryChain()

document_cache = {}

class SummaryResponse(BaseModel):
    summary: str
    file_path: str

class QuestionRequest(BaseModel):
    task_id: str
    question: str

class QuestionResponse(BaseModel):
    answer: str

class RAGQuestionRequest(BaseModel):
    question: str
    selected_doc_ids: list = None  # 可选，选择特定文档
    role_key: str = None  # 可选，角色选择
    style_key: str = None  # 可选，风格选择

class RAGQuestionResponse(BaseModel):
    answer: str
    sources: list
    retrieved_docs: list

class RoleListResponse(BaseModel):
    roles: list

class StyleListResponse(BaseModel):
    styles: list

class RoleGreetingRequest(BaseModel):
    role_key: str

class RoleGreetingResponse(BaseModel):
    greeting: str

@app.post("/api/summarize", response_model=SummaryResponse)
async def summarize_file(file: UploadFile = File(...)):
    """上传文件并生成摘要"""
    try:
        logger.info(f"========== 开始处理文件 ==========")
        logger.info(f"文件名: {file.filename}")
        logger.info(f"文件大小: {file.size} bytes")
        logger.info(f"内容类型: {file.content_type}")
        
        file_ext = Path(file.filename).suffix.lower()
        logger.info(f"文件扩展名: {file_ext}")
        
        # 保存上传的文件
        file_path = UPLOAD_DIR / file.filename
        logger.info(f"保存路径: {file_path}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 检查文件是否保存成功
        if not file_path.exists():
            raise Exception("文件保存失败")
        
        # 提取文本
        if file_ext == ".pdf":
            logger.info("开始提取PDF文本...")
            try:
                text = extract_text_from_pdf(str(file_path))
                logger.info(f"提取完成，文本长度: {len(text)} 字符")
            except Exception as e:
                logger.error(f"PDF提取失败: {str(e)}")
                os.remove(file_path)
                raise HTTPException(status_code=500, detail=f"PDF提取失败: {str(e)}")
        elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mp3', '.wav', '.flac', '.aac', '.ogg']:
            if process_media_file is None:
                os.remove(file_path)
                raise HTTPException(
                    status_code=400, 
                    detail="视频/音频处理功能未启用，请先安装依赖"
                )
            
            # 检查ffmpeg是否可用
            if check_ffmpeg_available is not None and not check_ffmpeg_available():
                os.remove(file_path)
                raise HTTPException(
                    status_code=400, 
                    detail="无法找到ffmpeg，请运行: pip install imageio-ffmpeg"
                )
            
            # 检查whisper是否安装
            if check_whisper_installed is not None and not check_whisper_installed():
                os.remove(file_path)
                raise HTTPException(
                    status_code=400, 
                    detail="未安装whisper，请运行: pip install openai-whisper"
                )
            
            logger.info(f"开始处理媒体文件 {file_ext}...")
            try:
                abs_file_path = str(file_path.resolve())
                logger.info(f"处理文件绝对路径: {abs_file_path}")
                text = process_media_file(abs_file_path)
                logger.info(f"转录完成，文本长度: {len(text)} 字符")
            except Exception as e:
                logger.error(f"媒体文件处理失败: {str(e)}")
                os.remove(file_path)
                raise HTTPException(status_code=500, detail=f"媒体文件处理失败: {str(e)}")
        else:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="不支持的文件格式，支持的格式：PDF、视频(.mp4, .avi, .mov, .mkv, .flv, .wmv)、音频(.mp3, .wav, .flac, .aac, .ogg)")
        
        # 检查提取的文本
        if not text.strip():
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="PDF文件中未提取到文本内容，可能是扫描件或加密PDF")
        
        # 生成摘要
        logger.info("开始生成摘要...")
        try:
            summary = summary_chain.create_summary(text)
            logger.info("摘要生成完成")
        except Exception as e:
            logger.error(f"摘要生成失败: {str(e)}", exc_info=True)
            os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"摘要生成失败: {str(e)}")
        
        # 缓存文档
        document_cache[file.filename] = text
        logger.info(f"文档已缓存，当前缓存数量: {len(document_cache)}")
        
        # 保存摘要
        summary_path = save_summary_to_file(summary, file.filename, SUMMARIES_DIR)
        logger.info(f"摘要已保存: {summary_path}")
        
        # 存入知识库
        try:
            doc_id = rag_system.add_to_knowledge_base(
                content=summary,
                source=file.filename,
                doc_type="summary",
                metadata={
                    "original_length": len(text),
                    "summary_length": len(summary)
                }
            )
            logger.info(f"摘要已存入知识库，文档ID: {doc_id}")
        except Exception as e:
            logger.error(f"存入知识库失败: {str(e)}")
        
        # 清理上传文件
        os.remove(file_path)
        logger.info("临时文件已删除")
        
        logger.info("========== 处理完成 ==========")
        return {"summary": summary, "file_path": summary_path, "knowledge_base_id": doc_id if 'doc_id' in locals() else None}
    
    except HTTPException as e:
        logger.error(f"HTTP错误: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"处理文件时出错: {str(e)}", exc_info=True)
        error_msg = str(e)
        # 隐藏敏感信息
        if "api_key" in error_msg.lower() or "key" in error_msg.lower():
            error_msg = "服务端处理失败，请稍后重试"
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """对已处理的文件进行问答"""
    try:
        if request.task_id not in document_cache:
            raise HTTPException(status_code=404, detail="任务ID不存在，请先上传文件")
        
        text = document_cache[request.task_id]
        answer = summary_chain.answer_question(text, request.question)
        return {"answer": answer}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"问答时出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/summaries")
async def list_summaries():
    """获取所有已保存的摘要文件列表"""
    summaries = []
    try:
        for file in SUMMARIES_DIR.iterdir():
            if file.is_file():
                summaries.append(file.name)
    except Exception as e:
        logger.error(f"获取摘要列表失败: {str(e)}")
    
    return {"summaries": summaries}

@app.get("/api/summary/{filename}")
async def get_summary(filename: str):
    """获取指定摘要文件内容"""
    safe_filename = filename.replace(' ', '_').replace('/', '_').replace('\\', '_')
    file_path = SUMMARIES_DIR / safe_filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="摘要文件不存在")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {"content": content}

@app.post("/api/rag/ask", response_model=RAGQuestionResponse)
async def rag_ask_question(request: RAGQuestionRequest):
    """基于知识库的RAG问答，支持角色和风格选择"""
    try:
        result = rag_system.answer_with_rag(
            request.question, 
            request.selected_doc_ids,
            request.role_key,
            request.style_key
        )
        return result
    except Exception as e:
        logger.error(f"RAG问答出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/roles", response_model=RoleListResponse)
async def get_roles():
    """获取所有可用角色列表"""
    try:
        roles = rag_system.get_available_roles()
        return {"roles": roles}
    except Exception as e:
        logger.error(f"获取角色列表失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/styles", response_model=StyleListResponse)
async def get_styles():
    """获取所有可用风格列表"""
    try:
        styles = rag_system.get_available_styles()
        return {"styles": styles}
    except Exception as e:
        logger.error(f"获取风格列表失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/role-greeting", response_model=RoleGreetingResponse)
async def get_role_greeting(request: RoleGreetingRequest):
    """获取角色的问候语"""
    try:
        greeting = rag_system.get_role_greeting(request.role_key)
        return {"greeting": greeting}
    except Exception as e:
        logger.error(f"获取角色问候语失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge-base/stats")
async def get_knowledge_base_stats():
    """获取知识库统计信息"""
    try:
        stats = rag_system.get_knowledge_base_stats()
        return stats
    except Exception as e:
        logger.error(f"获取知识库统计失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge-base/documents")
async def list_knowledge_base_documents():
    """获取知识库中的所有文档列表"""
    try:
        from backend.knowledge_base import knowledge_base
        docs = knowledge_base.list_documents()
        return {"documents": docs, "total": len(docs)}
    except Exception as e:
        logger.error(f"获取文档列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge-base/document/{doc_id}")
async def get_knowledge_base_document(doc_id: str):
    """获取知识库中的指定文档"""
    try:
        from backend.knowledge_base import knowledge_base
        doc = knowledge_base.get_document(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="文档不存在")
        return doc
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"获取文档失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/knowledge-base/document/{doc_id}")
async def delete_knowledge_base_document(doc_id: str):
    """删除知识库中的指定文档"""
    try:
        from backend.knowledge_base import knowledge_base
        success = knowledge_base.delete_document(doc_id)
        if success:
            return {"message": "文档删除成功", "doc_id": doc_id}
        else:
            raise HTTPException(status_code=404, detail="文档不存在")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"删除文档失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
