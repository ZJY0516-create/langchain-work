print("Start")
import sys
sys.path.insert(0, '.')
print("Path set")
from backend.knowledge_base.rag_system import RAGSystem
print("Import done")
rag = RAGSystem()
print(f"RAG created, docs: {len(rag.documents)}")
docs = rag._retrieve_relevant_docs('Linux', top_k=2)
print(f"Retrieved: {len(docs)} docs")
