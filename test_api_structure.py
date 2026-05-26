import requests

r = requests.get('http://localhost:8000/api/knowledge-base/documents')
docs = r.json()

print('API返回的文档数量:', len(docs))
print('\n第一个文档结构:')
print('键:', list(docs[0].keys()))
print('内容:', str(docs[0])[:500])