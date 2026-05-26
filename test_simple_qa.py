import requests

# 获取简历文档
r = requests.get('http://localhost:8000/api/knowledge-base/documents')
docs = r.json()

resume_doc = None
for d in docs:
    if '简历' in d['filename']:
        resume_doc = d
        break

print(f'选中文档: {resume_doc["filename"]}')

# 测试大模型语义检索
body = {
    'message': '我的专业技能是什么',
    'document_ids': [resume_doc['id']],
    'role': '',
    'style': ''
}
print('\n正在调用大模型进行语义检索...')
try:
    r = requests.post('http://localhost:8000/api/chat', json=body, timeout=120)
    result = r.json()
    print('\n大模型回答结果:')
    print(result['response'])
except Exception as e:
    print(f'错误: {e}')