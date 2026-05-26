# 运行多媒体摘要工具
$env:PYTHONPATH = "."
& "c:\Users\31639\Desktop\langchain work 5.22\venv\scripts\python.exe" -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
