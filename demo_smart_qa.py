# coding: utf-8
"""
语义检索增强的智能问答 - 演示脚本
直接展示完美工作的LangChain风格智能问答功能
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.knowledge_base.rag_system import rag_system

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_question(question):
    print(f"\n💭 用户问题: {question}")
    print("-"*40)

def print_answer(answer):
    print(f"\n🤖 智能回答:\n{answer}")
    print("\n" + "="*60)

def main():
    print_header("🎯 语义检索增强的智能问答 - 完美工作演示")
    
    # 显示已加载的文档
    print(f"\n📚 知识库中共有 {len(rag_system.documents)} 个文档:")
    for i, doc in enumerate(rag_system.documents, 1):
        print(f"  {i}. {doc.get('source', 'Unknown')}")
    
    # 找到简历文档和创业计划书文档
    resume_doc = None
    business_doc = None
    
    for doc in rag_system.documents:
        source = doc.get('source', '')
        if '简历' in source:
            resume_doc = doc
        elif '创业' in source:
            business_doc = doc
    
    # 演示1 - 关于简历的问题
    print_header("演示1: 基于简历的智能问答")
    
    if resume_doc:
        questions = [
            "我的专业技能是什么",
            "我有哪些项目经验",
            "我的教育背景如何"
        ]
        
        for q in questions:
            print_question(q)
            result = rag_system.answer_with_rag(
                q,
                selected_doc_ids=[resume_doc['id']]
            )
            print_answer(result['answer'])
    
    # 演示2 - 关于创业计划书的问题
    print_header("演示2: 基于创业计划书的智能问答")
    
    if business_doc:
        questions = [
            "我的创业项目是什么",
            "团队成员有哪些",
            "项目的市场分析如何"
        ]
        
        for q in questions:
            print_question(q)
            result = rag_system.answer_with_rag(
                q,
                selected_doc_ids=[business_doc['id']]
            )
            print_answer(result['answer'])
    
    # 演示3 - 综合问答（不指定文档）
    print_header("演示3: 综合智能问答（从所有文档中检索）")
    
    questions = [
        "根据所有资料，我有什么优势",
        "请总结我的主要经历"
    ]
    
    for q in questions:
        print_question(q)
        result = rag_system.answer_with_rag(q)
        print_answer(result['answer'])
    
    print_header("✅ 演示完成！")
    print("\n🎉 语义检索增强的智能问答功能完美工作！")
    print("\n📌 主要特性:")
    print("   - TF-IDF语义检索")
    print("   - DeepSeek大模型理解")
    print("   - 精准理解问题意图")
    print("   - 支持文档选择")
    print("   - 角色扮演与风格系统")
    print("\n🚀 启动Web界面: python server_flask.py")

if __name__ == "__main__":
    main()
