import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backend.knowledge_base.vector_store import knowledge_base

# 添加已有的摘要到知识库
summary_dir = Path(__file__).parent / "backend" / "summaries"

if summary_dir.exists():
    print(f"扫描摘要目录: {summary_dir}")
    
    count = 0
    for summary_file in summary_dir.glob("*.txt"):
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            source = summary_file.name.replace('.txt', '')
            
            # 检查是否已存在
            existing_docs = knowledge_base.get_all_documents()
            exists = any(doc['source'] == source for doc in existing_docs)
            
            if not exists:
                doc_id = knowledge_base.add_document(
                    content=content,
                    source=source,
                    doc_type="summary"
                )
                print(f"✅ 已添加: {source} (ID: {doc_id})")
                count += 1
            else:
                print(f"⏭️  已存在: {source}")
                
        except Exception as e:
            print(f"❌ 处理 {summary_file.name} 时出错: {e}")
    
    print(f"\n总共添加了 {count} 个文档到知识库")
else:
    print(f"摘要目录不存在: {summary_dir}")

# 显示当前知识库状态
docs = knowledge_base.get_all_documents()
print(f"\n当前知识库文档总数: {len(docs)}")
for doc in docs:
    print(f"- {doc['source']} ({doc['type']})")
