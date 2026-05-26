import sys
sys.path.insert(0, '.')

from backend.knowledge_base.rag_system import RAGSystem

rag = RAGSystem()

query = 'Linux系统中如何查看CPU信息'
doc_contents = [doc['content'] for doc in rag.documents]

print(f"查询: {query}")
print(f"文档数量: {len(doc_contents)}")
print(f"文档1长度: {len(doc_contents[0])}")

query_tokens = rag._tokenize(query)
print(f"\n查询分词: {query_tokens}")

doc_tokens = rag._tokenize(doc_contents[0][:1000])
print(f"\n文档1分词(前1000字符): {doc_tokens[:20]}...")

print("\n--- 计算TF-IDF ---")
try:
    scores = rag._compute_tfidf(query, doc_contents)
    print(f"相似度分数: {scores}")
    print(f"最高分: {max(scores)}")
except Exception as e:
    print(f"TF-IDF计算错误: {e}")
    import traceback
    traceback.print_exc()
