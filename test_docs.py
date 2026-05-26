from backend.knowledge_base.rag_system import rag_system

print('文档数量:', len(rag_system.documents))
for i, doc in enumerate(rag_system.documents[:2]):
    print(f'\n--- 文档 {i+1} ---')
    print(f'文档ID: {doc["id"][:8]}...')
    print(f'文档名称: {doc["filename"]}')
    print(f'内容预览: {doc["content"][:150]}...')