from backend.langchain import SummaryChain, QAChain

summary_chain = SummaryChain()
qa_chain = QAChain()

def create_summary(text: str) -> str:
    return summary_chain.create_summary(text)

def answer_question(text: str, question: str) -> str:
    return qa_chain.answer_question(text, question)