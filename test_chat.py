import requests
import json

# 获取文档列表
r = requests.get('http://localhost:8000/api/knowledge-base/documents')
docs = r.json()
print('文档列表:')
for i, d in enumerate(docs[:5]):
    print(f'{i+1}. {d["filename"]} - ID: {d["id"][:8]}...')

# 测试问答 - 使用第一个文档
first_doc_id = docs[0]['id']
body = {
    'message': '请介绍一下这份文档的内容',
    'document_ids': [first_doc_id],
    'role': '',
    'style': ''
}
r = requests.post('http://localhost:8000/api/chat', json=body)
print('\n问答结果:')
result = r.json()
print(result['response'])

# 测试角色扮演
body2 = {
    'message': '介绍一下旅游景点',
    'document_ids': [],
    'role': 'tour_guide',
    'style': 'meme'
}
r2 = requests.post('http://localhost:8000/api/chat', json=body2)
print('\n角色扮演结果:')
result2 = r2.json()
print(result2['response'])