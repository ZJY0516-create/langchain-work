from langchain_classic.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from backend.langchain.llm import llm

def create_buffer_memory(memory_key: str = "chat_history", input_key: str = "question") -> ConversationBufferMemory:
    """创建对话缓冲区记忆"""
    return ConversationBufferMemory(
        memory_key=memory_key,
        input_key=input_key,
        chat_memory=InMemoryChatMessageHistory(),
        return_messages=True
    )

def create_summary_memory(memory_key: str = "chat_history") -> ConversationSummaryMemory:
    """创建对话摘要记忆，自动总结长对话"""
    return ConversationSummaryMemory(
        llm=llm,
        memory_key=memory_key,
        return_messages=True
    )

def create_window_memory(k: int = 5, memory_key: str = "chat_history") -> ConversationBufferWindowMemory:
    """创建对话窗口记忆，只保留最近k轮对话"""
    return ConversationBufferWindowMemory(
        k=k,
        memory_key=memory_key,
        return_messages=True
    )

class ChatMemoryManager:
    def __init__(self):
        self.memories = {}
    
    def get_memory(self, session_id: str, memory_type: str = "buffer"):
        """获取或创建会话记忆"""
        if session_id not in self.memories:
            if memory_type == "summary":
                self.memories[session_id] = create_summary_memory()
            elif memory_type == "window":
                self.memories[session_id] = create_window_memory()
            else:
                self.memories[session_id] = create_buffer_memory()
        return self.memories[session_id]
    
    def clear_memory(self, session_id: str):
        """清除指定会话的记忆"""
        if session_id in self.memories:
            del self.memories[session_id]
    
    def get_history(self, session_id: str):
        """获取会话历史记录"""
        memory = self.get_memory(session_id)
        return memory.load_memory_variables({})

chat_memory_manager = ChatMemoryManager()