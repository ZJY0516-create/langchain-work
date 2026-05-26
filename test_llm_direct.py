import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.knowledge_base.rag_system import rag_system

print("测试直接大模型调用...")

# 测试问题
question = "我的专业技能是什么"

# 获取简历文档
resume_doc = None
for doc in rag_system.documents:
    if "简历" in doc.get("source", ""):
        resume_doc = doc
        break

print(f"选中文档: {resume_doc['source']}")

# 直接调用RAG方法
print("\n开始调用大模型...")
result = rag_system.answer_with_rag(
    question,
    selected_doc_ids=[resume_doc['id']] if resume_doc else None
)

print(f"\n大模型返回结果:")
print(result['answer'])
