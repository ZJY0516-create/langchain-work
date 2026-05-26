"""
文旅智答 - Streamlit 前端应用
基于 LangChain 的智能问答系统
"""

import streamlit as st
import requests
import time
from typing import List, Dict

# API 配置
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")

# 角色列表
ROLES = [
    {"id": "tour_guide", "name": "导游", "description": "专业的旅游向导"},
    {"id": "historian", "name": "历史学家", "description": "精通历史文化"},
    {"id": "foodie", "name": "美食家", "description": "美食达人"},
    {"id": "local", "name": "本地居民", "description": "本地人视角"},
    {"id": "photographer", "name": "摄影师", "description": "摄影专家"},
    {"id": "adventurer", "name": "探险家", "description": "户外探险爱好者"},
]

# 风格列表
STYLES = [
    {"id": "normal", "name": "标准"},
    {"id": "elderly", "name": "老年友好"},
    {"id": "kids", "name": "儿童友好"},
    {"id": "meme", "name": "网络热梗"},
]

def init_session_state():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "selected_docs" not in st.session_state:
        st.session_state.selected_docs = []
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = ""
    if "selected_style" not in st.session_state:
        st.session_state.selected_style = "normal"
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False

def fetch_documents():
    """获取文档列表"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/knowledge-base/documents", timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.warning(f"无法连接到知识库: {e}")
    return []

def fetch_stats():
    """获取统计信息"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/knowledge-base/stats", timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return {"total_docs": 0, "total_summaries": 0}

def send_message(message: str):
    """发送消息"""
    st.session_state.is_loading = True
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json={
                "message": message,
                "document_ids": st.session_state.selected_docs,
                "role": st.session_state.selected_role,
                "style": st.session_state.selected_style,
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json().get("response", "未收到回答")
        else:
            return f"错误: {response.status_code}"
    except Exception as e:
        return f"连接失败: {str(e)}"
    finally:
        st.session_state.is_loading = False

def upload_file(file):
    """上传文件"""
    try:
        with st.spinner("正在处理文件..."):
            form_data = {"file": file}
            response = requests.post(
                f"{API_BASE_URL}/api/upload",
                files={"file": file},
                timeout=120
            )
            if response.status_code == 200:
                result = response.json()
                st.success(f"文件上传成功！\n\n摘要: {result.get('summary', '')[:200]}...")
                st.session_state.documents = fetch_documents()
            else:
                st.error(f"上传失败: {response.text}")
    except Exception as e:
        st.error(f"上传失败: {str(e)}")

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
    stats = fetch_stats()
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
        uploaded_file = st.file_uploader("选择PDF文件", type=["pdf"])
        if uploaded_file:
            upload_file(uploaded_file)
        
        # 文档选择
        st.subheader("选择参考文档")
        if not st.session_state.documents:
            st.session_state.documents = fetch_documents()
        
        if st.session_state.documents:
            for doc in st.session_state.documents:
                is_selected = doc["id"] in st.session_state.selected_docs
                checkbox = st.checkbox(
                    f"{doc['filename']}",
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
    
    # 加载状态
    if st.session_state.is_loading:
        with st.chat_message("assistant"):
            with st.spinner("正在思考..."):
                time.sleep(1)
    
    # 输入框
    user_input = st.chat_input("请输入您的问题...")
    if user_input:
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # 获取回答
        with st.chat_message("assistant"):
            response = send_message(user_input)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()