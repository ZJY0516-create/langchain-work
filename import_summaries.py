import sys
import io
from pathlib import Path

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from backend.knowledge_base.vector_store import knowledge_base

# 添加已有的摘要到知识库
summary_dir = Path(__file__).parent / "backend" / "summaries"

if summary_dir.exists():
    print(f"Scanning summary directory: {summary_dir}")
    
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
                print(f"Added: {source} (ID: {doc_id})")
                count += 1
            else:
                print(f"Exists: {source}")
                
        except Exception as e:
            print(f"Error processing {summary_file.name}: {e}")
    
    print(f"\nTotal added: {count} documents")
else:
    print(f"Summary directory not found: {summary_dir}")

# 显示当前知识库状态
docs = knowledge_base.get_all_documents()
print(f"\nCurrent knowledge base documents: {len(docs)}")
for doc in docs:
    print(f"- {doc['source']} ({doc['type']})")
