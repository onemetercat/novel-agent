"""内容持久化模块 - 供MCP工具和Web应用共享使用"""

import json
import os
from datetime import datetime

# 内容存储目录（与web-app共享）
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_CONTENT_DIR = os.path.join(_BASE_DIR, '..', 'web-app', 'content')
os.makedirs(_CONTENT_DIR, exist_ok=True)


def save_content(title: str, content: str, content_type: str, params: dict = None) -> str:
    """保存生成内容到共享目录。
    
    Args:
        title: 内容标题
        content: 生成的内容
        content_type: 内容类型（novel_outline, novel_chapter, script_outline, script_scene）
        params: 生成参数（可选）
    
    Returns:
        保存的文件名
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{content_type}.json"
    filepath = os.path.join(_CONTENT_DIR, filename)
    
    content_data = {
        'type': content_type,
        'title': title,
        'content': content,
        'params': params or {},
        'created_at': datetime.now().isoformat(),
        'source': 'mcp'  # 标记来源为MCP调用
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(content_data, f, ensure_ascii=False, indent=2)
    
    return filename


def list_contents(content_type: str = "") -> list:
    """列出所有已保存的内容。
    
    Args:
        content_type: 内容类型过滤（可选）
    
    Returns:
        内容列表
    """
    contents = []
    if not os.path.exists(_CONTENT_DIR):
        return contents
    
    for filename in sorted(os.listdir(_CONTENT_DIR), reverse=True):
        if filename.endswith('.json'):
            if content_type and content_type not in filename:
                continue
            filepath = os.path.join(_CONTENT_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    content['filename'] = filename
                    contents.append(content)
            except:
                pass
    return contents


def get_content(filename: str) -> dict:
    """获取指定文件的内容。
    
    Args:
        filename: 文件名
    
    Returns:
        内容字典，未找到返回None
    """
    filepath = os.path.join(_CONTENT_DIR, filename)
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None


def delete_content(filename: str) -> bool:
    """删除指定文件。
    
    Args:
        filename: 文件名
    
    Returns:
        是否删除成功
    """
    filepath = os.path.join(_CONTENT_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
