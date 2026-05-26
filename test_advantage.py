import requests

# 获取简历文档
r = requests.get('http://localhost:8000/api/knowledge-base/documents')
docs = r.json()

resume_doc = None
for d in docs:
    if '简历' in d['source']:
        resume_doc = d
        break

print(f'选中文档: {resume_doc["source"]}')

# 测试"我有什么优势"
body = {
    'message': '我有什么优势',
    'document_ids': [resume_doc['id']],
    'role': '',
    'style': ''
}
r = requests.post('http://localhost:8000/api/chat', json=body)
result = r.json()
print('\n问答结果("我有什么优势"):')
print(result['response'])

# 测试其他问题
body2 = {
    'message': '我的专业技能有哪些',
    'document_ids': [resume_doc['id']],
    'role': '',
    'style': ''
}
r2 = requests.post('http://localhost:8000/api/chat', json=body2)
result2 = r2.json()
print('\n问答结果("我的专业技能有哪些"):')
print(result2['response'])