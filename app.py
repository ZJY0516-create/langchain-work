"""
文旅智答 - Streamlit 一体化应用
包含完整的知识库和问答逻辑
"""

import streamlit as st
import time
import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any

# 配置
DEESEEK_API_KEY = "sk-ec718a2e5be24ed3ad3f568f36ea409e"
DEESEEK_BASE_URL = "https://api.deepseek.com/v1"
DEESEEK_MODEL = "deepseek-chat"
TEMPERATURE = 0.7
MAX_TOKENS = 4096

# 数据目录
DATA_DIR = "data"
KB_DIR = os.path.join(DATA_DIR, "knowledge_base")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
SUMMARIES_DIR = os.path.join(DATA_DIR, "summaries")

# 确保目录存在
os.makedirs(KB_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(SUMMARIES_DIR, exist_ok=True)

# 角色列表
ROLES = [
    {"id": "tour_guide", "name": "导游", "description": "专业的旅游向导，熟悉各大景点"},
    {"id": "historian", "name": "历史学家", "description": "精通历史文化，讲解深入浅出"},
    {"id": "foodie", "name": "美食家", "description": "美食达人，推荐地道美味"},
    {"id": "local", "name": "本地居民", "description": "本地人视角，分享地道玩法"},
    {"id": "photographer", "name": "摄影师", "description": "摄影专家，分享拍摄技巧"},
    {"id": "adventurer", "name": "探险家", "description": "户外探险爱好者，分享攻略"},
]

# 风格列表
STYLES = [
    {"id": "normal", "name": "标准"},
    {"id": "elderly", "name": "老年友好"},
    {"id": "kids", "name": "儿童友好"},
    {"id": "meme", "name": "网络热梗"},
]

# 角色系统提示词
ROLE_SYSTEM_PROMPTS = {
    "tour_guide": "你是一位专业的导游，熟悉中国各地的旅游景点、美食和文化。请用热情友好的语言回答问题，提供实用的旅游建议。",
    "historian": "你是一位历史学家，对中国历史和文化有深入研究。请用学术严谨但通俗易懂的语言回答问题。",
    "foodie": "你是一位美食家，精通中国各大菜系。请用生动诱人的语言介绍美食，让听者垂涎欲滴。",
    "local": "你是一位本地居民，熟悉当地的风土人情和生活习惯。请用亲切朴实的语言回答问题。",
    "photographer": "你是一位专业摄影师，擅长捕捉美丽风景。请用富有画面感的语言描述景色。",
    "adventurer": "你是一位探险家，热爱户外探险和极限运动。请用充满激情和冒险精神的语言回答问题。"
}

# 风格后缀
STYLE_SUFFIXES = {
    "normal": "",
    "elderly": "\n（以上内容已简化，适合老年朋友阅读）",
    "kids": "\n✨ 小朋友们觉得有趣吗？快来探索更多吧！✨",
    "meme": "\n家人们谁懂啊！这也太绝了吧！👏"
}

def init_session_state():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents" not in st.session_state:
        st.session_state.documents = load_documents()
    if "selected_docs" not in st.session_state:
        st.session_state.selected_docs = []
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = ""
    if "selected_style" not in st.session_state:
        st.session_state.selected_style = "normal"
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False

def load_documents() -> List[Dict]:
    """加载知识库文档"""
    docs = []
    documents_file = os.path.join(KB_DIR, "documents.json")
    
    if os.path.exists(documents_file):
        try:
            with open(documents_file, 'r', encoding='utf-8') as f:
                docs = json.load(f)
        except Exception as e:
            st.warning(f"加载文档失败: {e}")
    
    # 也加载单独的文档文件
    for filename in os.listdir(KB_DIR):
        if filename.endswith('.json') and filename != "documents.json":
            filepath = os.path.join(KB_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    doc = json.load(f)
                    if doc not in docs:
                        docs.append(doc)
            except Exception as e:
                pass
    
    return docs

def save_document(doc: Dict):
    """保存文档"""
    documents_file = os.path.join(KB_DIR, "documents.json")
    
    try:
        docs = load_documents()
        if doc not in docs:
            docs.append(doc)
        with open(documents_file, 'w', encoding='utf-8') as f:
            json.dump(docs, f, ensure_ascii=False, indent=2)
        
        # 也保存单独的文件
        filepath = os.path.join(KB_DIR, f"{doc['id']}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"保存文档失败: {e}")

def extract_text_from_pdf(file_bytes):
    """从PDF提取文本"""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_bytes)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF解析失败: {e}")

def extract_audio_from_video(file_bytes, filename):
    """从视频提取音频"""
    try:
        import tempfile
        from moviepy.editor import VideoFileClip
        
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            temp_video.write(file_bytes.read())
            temp_video_path = temp_video.name
        
        video = VideoFileClip(temp_video_path)
        audio = video.audio
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
        
        audio.write_audiofile(temp_audio_path)
        video.close()
        
        import os
        os.unlink(temp_video_path)
        
        return temp_audio_path
    
    except Exception as e:
        raise Exception(f"视频处理失败: {e}")

def speech_to_text(audio_path):
    """语音转文字"""
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {DEESEEK_API_KEY}"
        }
        
        with open(audio_path, "rb") as f:
            files = {"file": f}
            data = {"model": "deepseek-audio"}
            
            response = requests.post(
                f"{DEESEEK_BASE_URL}/audio/transcriptions",
                headers=headers,
                files=files,
                data=data,
                timeout=120
            )
        
        import os
        os.unlink(audio_path)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("text", "")
        else:
            raise Exception(f"语音转文字失败: {response.status_code}")
    
    except Exception as e:
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.unlink(audio_path)
        raise Exception(f"语音转文字失败: {e}")

def create_summary(text: str) -> str:
    """生成文档摘要"""
    if len(text) <= 1000:
        return text[:500] + "..." if len(text) > 500 else text
    
    chunks = []
    current_chunk = ""
    for paragraph in text.split('\n'):
        if len(current_chunk) + len(paragraph) + 1 <= 3000:
            current_chunk += paragraph + "\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    summaries = []
    for chunk in chunks:
        summary = call_llm(f"请对以下内容进行详细的总结：\n\n{chunk}\n\n请用中文提供一个清晰、详细的摘要。")
        summaries.append(summary)
    
    if len(summaries) > 1:
        combined_text = "\n\n".join(summaries)
        final_summary = call_llm(f"请将以下多个摘要整合成一个完整、连贯的总结：\n\n{combined_text}\n\n请提供一个统一的、详细的总结报告。")
        return final_summary
    
    return summaries[0]

def call_llm(prompt: str) -> str:
    """调用大模型"""
    import requests
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEESEEK_API_KEY}"
    }
    
    data = {
        "model": DEESEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }
    
    try:
        response = requests.post(
            f"{DEESEEK_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        elif response.status_code == 401:
            return "❌ API密钥无效或已过期，请检查DEESEEK_API_KEY配置"
        elif response.status_code == 403:
            return "❌ 权限不足，请检查API密钥权限"
        elif response.status_code == 429:
            return "❌ 请求过于频繁，请稍后再试"
        else:
            try:
                error_detail = response.json().get('error', {}).get('message', '')
                return f"❌ API调用失败 ({response.status_code}): {error_detail}"
            except:
                return f"❌ API调用失败: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "❌ 网络连接失败，请检查网络或稍后重试"
    except requests.exceptions.Timeout:
        return "❌ 请求超时，请稍后重试"
    except Exception as e:
        return f"❌ 连接失败: {str(e)}"

def answer_with_rag(question: str, context: str = "", role_key: str = "", style_key: str = "") -> str:
    """基于RAG回答问题"""
    system_prompt = ROLE_SYSTEM_PROMPTS.get(role_key, "")
    style_suffix = STYLE_SUFFIXES.get(style_key, "")
    
    prompt = f"""你是一个智能问答助手，擅长根据提供的参考资料精准回答用户问题。

参考资料：
{context}

用户问题：{question}

请仔细阅读参考资料，分析用户问题的核心意图，然后进行以下步骤：
1. 理解问题：明确用户问的是什么，关键信息是什么
2. 检索信息：在参考资料中找到与问题直接相关的内容
3. 分析关联：判断资料中的哪些部分与问题最相关
4. 精准回答：基于相关信息，用简洁、准确、自然的语言回答问题

回答要求：
- 只回答与问题直接相关的内容，不要包含无关信息
- 如果参考资料中有多个相关部分，请整合这些信息给出完整回答
- 如果参考资料中没有相关信息，请明确说明"根据提供的参考资料，无法回答该问题"
- 回答要简洁明了，避免冗长，直击要点
- 如果涉及具体数据或事实，确保准确性

请用中文回答。"""
    
    if system_prompt:
        prompt = system_prompt + "\n\n" + prompt
    
    answer = call_llm(prompt)
    
    if style_suffix:
        answer += style_suffix
    
    return answer

def upload_file(file):
    """上传文件并生成摘要"""
    try:
        file_ext = file.name.split('.')[-1].lower()
        text = ""
        
        if file_ext == 'pdf':
            with st.spinner("正在解析PDF..."):
                text = extract_text_from_pdf(file)
        elif file_ext in ['mp4', 'mov', 'avi', 'mkv', 'webm']:
            with st.spinner("正在提取音频..."):
                audio_path = extract_audio_from_video(file, file.name)
            with st.spinner("正在转写文字..."):
                text = speech_to_text(audio_path)
        else:
            st.error(f"不支持的文件格式: {file_ext}，支持PDF、MP4、MOV、AVI、MKV、WEBM")
            return
        
        if not text.strip():
            st.error("未提取到内容")
            return
        
        with st.spinner("正在生成摘要..."):
            summary = create_summary(text)
        
        doc = {
            "id": str(uuid.uuid4()),
            "content": summary,
            "source": file.name,
            "type": "summary",
            "created_at": datetime.now().isoformat(),
            "metadata": {"original_length": len(text), "summary_length": len(summary), "file_type": file_ext}
        }
        
        save_document(doc)
        st.session_state.documents = load_documents()
        
        st.success(f"文件上传成功！\n\n摘要: {summary[:200]}...")
        
    except Exception as e:
        st.error(f"上传失败: {str(e)}")

def get_stats():
    """获取统计信息"""
    docs = load_documents()
    return {"total_docs": len(docs), "total_summaries": len(docs)}

def main():
    """主应用函数"""
    st.set_page_config(
        page_title="文旅智答",
        page_icon="🏞️",
        layout="wide"
    )
    
    init_session_state()
    
    # 页面标题
    st.title("🏞️ 文旅智答")
    st.subheader("基于知识库的智能问答系统")
    
    # 统计信息
    stats = get_stats()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("知识库文档", f"{stats.get('total_docs', 0)} 个")
    with col2:
        st.metric("文档摘要", f"{stats.get('total_summaries', 0)} 个")
    
    # 侧边栏
    with st.sidebar:
        st.header("设置")
        
        # 角色选择
        st.subheader("选择角色")
        role_options = [""] + [role["name"] for role in ROLES]
        selected_role_name = st.selectbox(
            "请选择回答角色",
            role_options,
            index=role_options.index(next((r["name"] for r in ROLES if r["id"] == st.session_state.selected_role), "")) if st.session_state.selected_role else 0
        )
        st.session_state.selected_role = next((r["id"] for r in ROLES if r["name"] == selected_role_name), "")
        
        # 风格选择
        st.subheader("回答风格")
        style_options = [style["name"] for style in STYLES]
        selected_style_name = st.selectbox(
            "请选择回答风格",
            style_options,
            index=next((i for i, s in enumerate(STYLES) if s["id"] == st.session_state.selected_style), 0)
        )
        st.session_state.selected_style = next((s["id"] for s in STYLES if s["name"] == selected_style_name), "normal")
        
        # 文件上传
        st.subheader("上传文档")
        uploaded_file = st.file_uploader("选择文件 (支持PDF、视频)", type=["pdf", "mp4", "mov", "avi", "mkv", "webm"])
        if uploaded_file:
            upload_file(uploaded_file)
        
        # 文档选择
        st.subheader("选择参考文档")
        if st.session_state.documents:
            for doc in st.session_state.documents:
                is_selected = doc["id"] in st.session_state.selected_docs
                checkbox = st.checkbox(
                    f"{doc['source']}",
                    value=is_selected,
                    key=doc["id"]
                )
                if checkbox and doc["id"] not in st.session_state.selected_docs:
                    st.session_state.selected_docs.append(doc["id"])
                elif not checkbox and doc["id"] in st.session_state.selected_docs:
                    st.session_state.selected_docs.remove(doc["id"])
        
        # 清除选择
        if st.session_state.selected_docs:
            if st.button("清除选择"):
                st.session_state.selected_docs = []
    
    # 聊天区域
    st.header("智能问答")
    
    # 显示消息历史
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # 输入框
    user_input = st.chat_input("请输入您的问题...")
    if user_input:
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # 获取上下文
        context = ""
        if st.session_state.selected_docs:
            selected_docs_content = [
                doc for doc in st.session_state.documents 
                if doc["id"] in st.session_state.selected_docs
            ]
            context = "\n\n".join([f"【{doc['source']}】\n{doc['content']}" for doc in selected_docs_content])
        else:
            # 使用所有文档作为上下文
            context = "\n\n".join([f"【{doc['source']}】\n{doc['content']}" for doc in st.session_state.documents])
        
        # 获取回答
        with st.chat_message("assistant"):
            with st.spinner("正在思考..."):
                response = answer_with_rag(
                    user_input, 
                    context, 
                    st.session_state.selected_role, 
                    st.session_state.selected_style
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
