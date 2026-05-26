from typing import Optional, Type, List, Dict, Any
from pydantic import BaseModel, Field
from backend.knowledge_base.vector_store import knowledge_base

class SearchKnowledgeBaseArgs(BaseModel):
    query: str = Field(description="搜索查询词")
    top_k: Optional[int] = Field(default=3, description="返回结果数量")

class DocumentSummaryArgs(BaseModel):
    content: str = Field(description="需要总结的文档内容")

class QuestionAnsweringArgs(BaseModel):
    context: str = Field(description="参考上下文内容")
    question: str = Field(description="用户问题")

def search_knowledge_base_tool(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """搜索知识库中的相关文档"""
    results = knowledge_base.search_documents(query, top_k)
    return results

def document_summary_tool(content: str) -> str:
    """对文档内容进行摘要总结"""
    from backend.langchain.chains import SummaryChain
    summary_chain = SummaryChain()
    return summary_chain.create_summary(content)

def question_answering_tool(context: str, question: str) -> str:
    """根据提供的上下文回答问题"""
    from backend.langchain.chains import QAChain
    qa_chain = QAChain()
    return qa_chain.answer_question(context, question)

class ToolInfo:
    def __init__(self, name: str, description: str, args_schema: Type[BaseModel], func):
        self.name = name
        self.description = description
        self.args_schema = args_schema
        self.func = func

def get_all_tools() -> List[ToolInfo]:
    """获取所有可用工具"""
    return [
        ToolInfo(
            name="search_knowledge_base",
            description="搜索知识库中的相关文档，用于回答用户问题时查找参考资料",
            args_schema=SearchKnowledgeBaseArgs,
            func=search_knowledge_base_tool
        ),
        ToolInfo(
            name="document_summary",
            description="对文档内容进行摘要总结",
            args_schema=DocumentSummaryArgs,
            func=document_summary_tool
        ),
        ToolInfo(
            name="question_answering",
            description="根据提供的上下文回答问题",
            args_schema=QuestionAnsweringArgs,
            func=question_answering_tool
        )
    ]