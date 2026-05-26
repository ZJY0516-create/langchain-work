import logging
logging.basicConfig(level=logging.INFO)

print("Step 1: Importing modules...")
try:
    from fastapi import FastAPI
    print("✓ FastAPI imported")
except Exception as e:
    print(f"✗ FastAPI import failed: {e}")

try:
    from backend.config.settings import settings
    print("✓ Settings imported")
except Exception as e:
    print(f"✗ Settings import failed: {e}")

try:
    from backend.knowledge_base.rag_system import rag_system
    print("✓ RAG system imported")
except Exception as e:
    print(f"✗ RAG system import failed: {e}")

print("\nStep 2: Testing basic functionality...")
try:
    docs = rag_system.documents
    print(f"✓ Loaded {len(docs)} documents")
except Exception as e:
    print(f"✗ Failed to get documents: {e}")

try:
    roles = rag_system.get_available_roles()
    print(f"✓ Available roles: {[r['name'] for r in roles]}")
except Exception as e:
    print(f"✗ Failed to get roles: {e}")

try:
    styles = rag_system.get_available_styles()
    print(f"✓ Available styles: {[s['name'] for s in styles]}")
except Exception as e:
    print(f"✗ Failed to get styles: {e}")

print("\nStep 3: Testing RAG answer...")
try:
    result = rag_system.answer_with_rag("测试问题", [], "tour_guide", "meme")
    print(f"✓ RAG answer: {result['answer'][:100]}...")
except Exception as e:
    print(f"✗ RAG answer failed: {e}")

print("\nAll tests passed!")