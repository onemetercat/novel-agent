"""
MCP Server 快速启动脚本
用于启动AI小说和短剧剧本生成智能体
"""

import subprocess
import sys
import os

def main():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("AI小说和短剧剧本生成智能体 - MCP Server")
    print("=" * 60)
    
    # 检查依赖
    print("\n检查依赖...")
    try:
        import mcp
        print("✓ MCP 已安装")
    except ImportError:
        print("✗ MCP 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp", "--quiet"])
        print("✓ MCP 安装完成")
    
    # 启动服务器
    server_path = os.path.join(script_dir, "server.py")
    
    print(f"\n启动 MCP Server: {server_path}")
    print("-" * 60)
    print("提示: 此服务器使用 stdio 传输模式，供 Trae IDE 调用")
    print("如需单独测试，请使用 MCP Inspector 或 Trae IDE")
    print("-" * 60)
    
    # 运行服务器
    subprocess.run([sys.executable, server_path])

if __name__ == "__main__":
    main()
