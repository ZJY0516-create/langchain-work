from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from backend.config.settings import settings

def create_llm() -> BaseChatModel:
    """创建LangChain LLM实例，配置DeepSeek模型"""
    return ChatOpenAI(
        model_name=settings.deepseek_model,
        openai_api_key=settings.deepseek_api_key,
        openai_api_base=settings.deepseek_base_url,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        timeout=120
    )

llm = create_llm()