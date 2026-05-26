from langchain_classic.chains import LLMChain, SimpleSequentialChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from backend.langchain.llm import llm
from backend.langchain.prompts import SUMMARY_PROMPT, QA_PROMPT, RAG_PROMPT, ROLE_SYSTEM_PROMPTS, STYLE_SUFFIXES

class SummaryChain:
    def __init__(self):
        self.llm = llm
        self.summary_chain = LLMChain(
            llm=self.llm,
            prompt=SUMMARY_PROMPT,
            output_parser=StrOutputParser()
        )
        self.combine_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["summaries"],
                template="""请将以下多个摘要整合成一个完整、连贯的总结：

{summaries}

请提供一个统一的、详细的总结报告。"""
            ),
            output_parser=StrOutputParser()
        )

    def create_summary(self, text: str) -> str:
        chunks = self._split_text(text, 3000)
        
        summaries = []
        for chunk in chunks:
            summary = self.summary_chain.run(text=chunk)
            summaries.append(summary)
        
        if len(summaries) > 1:
            combined_text = "\n\n".join(summaries)
            final_summary = self.combine_chain.run(summaries=combined_text)
            return final_summary
        
        return summaries[0]

    def _split_text(self, text: str, max_length: int) -> list:
        chunks = []
        current_chunk = ""
        for paragraph in text.split('\n'):
            if len(current_chunk) + len(paragraph) + 1 <= max_length:
                current_chunk += paragraph + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n"
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

class QAChain:
    def __init__(self):
        self.llm = llm
        self.qa_chain = LLMChain(
            llm=self.llm,
            prompt=QA_PROMPT,
            output_parser=StrOutputParser()
        )

    def answer_question(self, context: str, question: str) -> str:
        return self.qa_chain.run(context=context, question=question)

class RAGChain:
    def __init__(self):
        self.llm = llm

    def answer_with_rag(self, question: str, context: str, role_key: str = "", style_key: str = "") -> str:
        system_prompt = ROLE_SYSTEM_PROMPTS.get(role_key, "")
        style_suffix = STYLE_SUFFIXES.get(style_key, "")
        
        rag_chain = LLMChain(
            llm=self.llm,
            prompt=RAG_PROMPT,
            output_parser=StrOutputParser()
        )
        
        answer = rag_chain.run(
            system_prompt=system_prompt,
            context=context,
            question=question
        )
        
        if style_suffix:
            answer += style_suffix
        
        return answer