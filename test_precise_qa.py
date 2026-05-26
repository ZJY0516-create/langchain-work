import requests

# 获取创业计划书文档ID
r = requests.get('http://localhost:8000/api/knowledge-base/documents')
docs = r.json()
plan_doc = None
for d in docs:
    if '创业计划书' in d['filename']:
        plan_doc = d
        break

print(f'选中文档: {plan_doc["filename"]}')

# 测试精准问答
body = {
    'message': '我的创业内容是什么',
    'document_ids': [plan_doc['id']],
    'role': '',
    'style': ''
}
r = requests.post('http://localhost:8000/api/chat', json=body)
result = r.json()
print('\n问答结果:')
print(result['response'])

# 测试另一个问题
body2 = {
    'message': '团队成员有哪些',
    'document_ids': [plan_doc['id']],
    'role': '',
    'style': ''
}
r2 = requests.post('http://localhost:8000/api/chat', json=body2)
result2 = r2.json()
print('\n第二个问题结果:')
print(result2['response'])