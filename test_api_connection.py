import requests
import os

api_key = os.environ.get('DEEPSEEK_API_KEY', 'sk-ec718a2e5be24ed3ad3f568f36ea409e')
url = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "你好"}],
    "temperature": 0.3,
    "max_tokens": 100
}

print(f"测试DeepSeek API连接...")
print(f"URL: {url}")
print(f"API Key: {api_key[:10]}...")

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("响应成功!")
        print(f"回答: {result['choices'][0]['message']['content']}")
    else:
        print(f"响应失败: {response.text}")
        
except Exception as e:
    print(f"错误: {e}")