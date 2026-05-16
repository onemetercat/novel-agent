"""
AI小说和短剧剧本智能体 - MCP Server
使用 Trae 内置 AI 模型生成内容，通过 HTTP API 保存到 Web 页面
"""

from mcp.server.fastmcp import FastMCP
import urllib.request
import urllib.error
import urllib.parse
import json
import os

# Web服务API地址
WEB_API_BASE = os.environ.get("WEB_API_BASE", "http://localhost:5001")

# 创建MCP服务器实例
mcp = FastMCP(
    name="novel-script-agent",
    instructions="AI小说和短剧剧本智能体，配合Trae内置AI使用"
)


def _http_post(url: str, data: dict) -> dict:
    """发送HTTP POST请求。"""
    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        raise ConnectionError(f"无法连接到Web服务（{WEB_API_BASE}）") from e


def _http_get(url: str) -> dict:
    """发送HTTP GET请求。"""
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        raise ConnectionError(f"无法连接到Web服务（{WEB_API_BASE}）") from e


def _http_delete(url: str) -> dict:
    """发送HTTP DELETE请求。"""
    req = urllib.request.Request(url, method='DELETE')
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        raise ConnectionError(f"无法连接到Web服务（{WEB_API_BASE}）") from e


def _save_via_api(endpoint: str, data: dict) -> str:
    """通过HTTP API保存内容到Web服务。"""
    try:
        url = f"{WEB_API_BASE}{endpoint}"
        result = _http_post(url, data)
        if result.get("success"):
            return "内容已保存！\n\n你可以在Web页面（http://localhost:5001）的历史记录中查看。"
        return f"保存失败：{result.get('error', '未知错误')}"
    except ConnectionError as e:
        return f"无法连接到Web服务。\n请确保Web服务正在运行：\n  cd web-app && python3 app.py"
    except Exception as e:
        return f"保存失败：{str(e)}"


@mcp.tool()
def save_novel_content(title: str, content: str, genre: str = "", theme: str = "", main_characters: str = "", world_building: str = "", target_chapters: int = 0, target_words_per_chapter: int = 0) -> str:
    """保存Trae生成的小说内容到Web页面（包含大纲和章节）。
    
    Args:
        title: 小说标题
        content: Trae生成的小说内容
        genre: 小说类型
        theme: 主题思想
        main_characters: 主要人物设定
        world_building: 世界观设定
        target_chapters: 目标章节数
        target_words_per_chapter: 每章字数
    
    Returns:
        保存成功信息
    """
    data = {
        "title": title,
        "genre": genre,
        "theme": theme,
        "main_characters": main_characters,
        "world_building": world_building,
        "target_chapters": target_chapters,
        "target_words_per_chapter": target_words_per_chapter,
        "content": content,
        "content_type": "novel",
        "source": "mcp"
    }
    return _save_via_api("/api/save-content", data)


@mcp.tool()
def save_script_content(title: str, content: str, genre: str = "", episode_count: int = 0, episode_duration: str = "", theme: str = "", main_characters: str = "", plot_summary: str = "") -> str:
    """保存Trae生成的短剧内容到Web页面（包含大纲和场景）。
    
    Args:
        title: 短剧标题
        content: Trae生成的短剧内容
        genre: 短剧类型
        episode_count: 总集数
        episode_duration: 每集时长
        theme: 主题
        main_characters: 主要人物设定
        plot_summary: 剧情简介
    
    Returns:
        保存成功信息
    """
    data = {
        "title": title,
        "genre": genre,
        "episode_count": episode_count,
        "episode_duration": episode_duration,
        "theme": theme,
        "main_characters": main_characters,
        "plot_summary": plot_summary,
        "content": content,
        "content_type": "script",
        "source": "mcp"
    }
    return _save_via_api("/api/save-content", data)


@mcp.tool()
def list_saved_contents(content_type: str = "") -> str:
    """列出所有已保存的内容。
    
    Args:
        content_type: 内容类型过滤（novel_outline, novel_chapter, script_outline, script_scene）
    
    Returns:
        内容列表
    """
    try:
        url = f"{WEB_API_BASE}/api/contents"
        if content_type:
            url += f"?type={content_type}"
        contents = _http_get(url)
        if not contents:
            return "暂无已保存的内容。"
        
        result = f"已保存的内容列表（共{len(contents)}条）：\n\n"
        for item in contents[:10]:
            type_name = {
                "novel": "小说",
                "script": "短剧",
                "novel_outline": "小说大纲",
                "novel_chapter": "小说章节",
                "script_outline": "短剧大纲",
                "script_scene": "短剧场景"
            }.get(item.get("type", ""), item.get("type", ""))
            result += f"- 【{type_name}】{item.get('title', '未命名')}\n"
            result += f"  时间：{item.get('created_at', '')}\n\n"
        
        result += "或在Web页面 http://localhost:5001 中查看"
        return result
    except Exception as e:
        return f"获取失败：{str(e)}"


@mcp.tool()
def get_content_by_title(title: str) -> str:
    """根据标题获取指定内容。
    
    Args:
        title: 内容标题
    
    Returns:
        文件内容
    """
    try:
        url = f"{WEB_API_BASE}/api/contents"
        contents = _http_get(url)
        for item in contents:
            if title.lower() in item.get("title", "").lower():
                return item.get("content", "内容为空")
        return f"未找到标题包含「{title}」的内容"
    except Exception as e:
        return f"获取失败：{str(e)}"


@mcp.tool()
def delete_content_by_title(title: str) -> str:
    """根据标题删除指定内容。
    
    Args:
        title: 内容标题
    
    Returns:
        删除结果
    """
    try:
        url = f"{WEB_API_BASE}/api/contents"
        contents = _http_get(url)
        for item in contents:
            if title.lower() in item.get("title", "").lower():
                filename = item.get("filename", "")
                if filename:
                    delete_url = f"{WEB_API_BASE}/api/delete/{filename}"
                    _http_delete(delete_url)
                    return f"已删除：{item.get('title', '')}"
                return f"删除失败"
        return f"未找到标题包含「{title}」的内容"
    except Exception as e:
        return f"删除失败：{str(e)}"


@mcp.tool()
def get_saved_contents_list(content_type: str = "") -> str:
    """列出所有已保存的内容（别名工具）。
    
    Args:
        content_type: 内容类型过滤（novel_outline, novel_chapter, script_outline, script_scene）
    
    Returns:
        内容列表
    """
    return list_saved_contents(content_type)


if __name__ == "__main__":
    mcp.run()
