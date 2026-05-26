"""
LangChain Server 启动脚本
支持高并发访问，使用多进程模式
"""

import subprocess
import sys

def main():
    cmd = [
        sys.executable, "-m", "uvicorn",
        "server_langserve:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--workers", "4",
        "--timeout-keep-alive", "120"
    ]
    
    print(f"启动命令: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()