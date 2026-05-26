from backend.knowledge_base.rag_system import rag_system

print('文档数量:', len(rag_system.documents))
for i, doc in enumerate(rag_system.documents[:1]):
    print(f'\n--- 文档 {i+1} ---')
    print('文档键:', list(doc.keys()))
    print('文档内容:', str(doc)[:300])