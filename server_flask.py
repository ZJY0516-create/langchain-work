# coding: utf-8
"""
Flask服务器 - 更稳定的部署方式
基于 LangChain 框架实现大模型应用开发
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
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

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

summary_chain = SummaryChain()

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/api/health")
def health_check():
    return jsonify({"status": "ok", "service": "LangChain Server"})

@app.route("/api/upload", methods=["POST"])
def upload_and_summarize():
    """上传文件并生成摘要 - 支持PDF、视频、音频"""
    try:
        if "file" not in request.files:
            return jsonify({"detail": "没有上传文件"}), 400
        
        file = request.files["file"]
        logger.info(f"处理文件: {file.filename}")
        
        file_ext = Path(file.filename).suffix.lower()
        file_path = UPLOAD_DIR / file.filename
        
        file.save(str(file_path))
        
        if file_ext == ".pdf":
            text = extract_text_from_pdf(str(file_path))
        elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mp3', '.wav', '.flac', '.aac', '.ogg']:
            if process_media_file is None:
                os.remove(file_path)
                return jsonify({"detail": "媒体处理功能未启用"}), 400
            
            text = process_media_file(str(file_path.resolve()))
        else:
            os.remove(file_path)
            return jsonify({"detail": "不支持的文件格式"}), 400
        
        if not text.strip():
            os.remove(file_path)
            return jsonify({"detail": "未提取到内容"}), 400
        
        summary = summary_chain.create_summary(text)
        
        save_summary_to_file(summary, file.filename, SUMMARIES_DIR)
        
        rag_system.add_to_knowledge_base(
            content=summary,
            source=file.filename,
            doc_type="summary",
            metadata={"original_length": len(text), "summary_length": len(summary)}
        )
        
        os.remove(file_path)
        
        return jsonify({"summary": summary, "filename": file.filename})
    
    except Exception as e:
        logger.error(f"上传处理失败: {str(e)}", exc_info=True)
        return jsonify({"detail": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat_with_kb():
    """基于知识库的智能问答 - 支持角色和风格选择"""
    try:
        data = request.json
        message = data.get("message", "")
        document_ids = data.get("document_ids", [])
        role = data.get("role", "")
        style = data.get("style", "")
        
        logger.info(f"收到问答请求: {message[:50]}...")
        
        result = rag_system.answer_with_rag(
            message,
            document_ids,
            role,
            style
        )
        
        return jsonify({"response": result["answer"]})
    except Exception as e:
        logger.error(f"问答失败: {str(e)}", exc_info=True)
        return jsonify({"detail": str(e)}), 500

@app.route("/api/knowledge-base/documents", methods=["GET"])
def get_documents():
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
        return jsonify(docs)
    except Exception as e:
        logger.error(f"获取文档失败: {str(e)}", exc_info=True)
        return jsonify({"detail": str(e)}), 500

@app.route("/api/knowledge-base/stats", methods=["GET"])
def get_stats():
    """获取知识库统计"""
    try:
        total_docs = len(list(SUMMARIES_DIR.iterdir())) if SUMMARIES_DIR.exists() else 0
        return jsonify({"total_docs": total_docs, "total_summaries": total_docs, "total_chats": 0})
    except Exception as e:
        logger.error(f"获取统计失败: {str(e)}", exc_info=True)
        return jsonify({"detail": str(e)}), 500

@app.route("/api/roles", methods=["GET"])
def get_roles():
    """获取角色列表"""
    return jsonify(rag_system.get_available_roles())

@app.route("/api/styles", methods=["GET"])
def get_styles():
    """获取风格列表"""
    return jsonify(rag_system.get_available_styles())

if __name__ == "__main__":
    logger.info("启动 Flask 服务器...")
    app.run(host="0.0.0.0", port=8000, debug=False)
