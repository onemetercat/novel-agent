"""
AI小说和短剧剧本智能体 - Web应用
简单可视化界面，无需登录，显示生成内容
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import sys
from datetime import datetime

app = Flask(__name__)

CONTENT_DIR = os.path.join(os.path.dirname(__file__), 'content')
os.makedirs(CONTENT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp-server'))
from tools.novel import generate_outline, generate_chapter, rewrite_text, polish_text
from tools.script import generate_script_outline, generate_script_scene
from tools.story import continue_story_content

def load_contents():
    contents = []
    if not os.path.exists(CONTENT_DIR):
        return contents
    
    for filename in sorted(os.listdir(CONTENT_DIR), reverse=True):
        if filename.endswith('.json'):
            filepath = os.path.join(CONTENT_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    content['filename'] = filename
                    contents.append(content)
            except:
                pass
    return contents

def save_content(content_data):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{content_data.get('type', 'content')}.json"
    filepath = os.path.join(CONTENT_DIR, filename)
    
    content_data['filename'] = filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(content_data, f, ensure_ascii=False, indent=2)
    
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contents', methods=['GET'])
def get_contents():
    return jsonify(load_contents())

@app.route('/api/content/<filename>', methods=['GET'])
def get_content(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Content not found'}), 404

@app.route('/api/save-content', methods=['POST'])
def api_save_content():
    """MCP工具通过HTTP API保存内容到Web页面。"""
    data = request.json
    
    content_type = data.get('content_type', '')
    if not content_type:
        if 'episode_count' in data or 'episode_number' in data:
            content_type = 'script'
        else:
            content_type = 'novel'
    
    content_data = {
        'type': content_type,
        'title': data.get('title', ''),
        'content': data.get('content', ''),
        'params': data,
        'created_at': datetime.now().isoformat(),
        'source': data.get('source', 'mcp')
    }
    
    filename = save_content(content_data)
    
    return jsonify({
        'success': True,
        'filename': filename,
        'message': f'内容已保存：{filename}'
    })

@app.route('/api/generate/novel', methods=['POST'])
def api_generate_novel():
    data = request.json
    title = data.get('title', '')
    genre = data.get('genre', '玄幻')
    theme = data.get('theme', '')
    main_characters = data.get('main_characters', '')
    world_building = data.get('world_building', '')
    target_chapters = int(data.get('target_chapters', 200))
    target_words = int(data.get('target_words_per_chapter', 3000))
    
    outline_result = generate_outline(
        title=title,
        genre=genre,
        theme=theme,
        main_characters=main_characters,
        world_building=world_building,
        target_chapters=target_chapters,
        target_words_per_chapter=target_words
    )
    
    chapter_result = generate_chapter(
        novel_title=title,
        chapter_number=1,
        chapter_title='',
        outline='',
        previous_chapters=outline_result,
        genre=genre,
        style='流畅通俗'
    )
    
    full_content = f"# 《{title}》完整小说内容\n\n"
    full_content += f"## 小说大纲\n\n{outline_result}\n\n"
    full_content += f"## 第1章示例\n\n{chapter_result}\n\n"
    full_content += "---\n\n> 注：以上为小说大纲和第1章示例内容。\n"
    full_content += f"> 完整{target_chapters}章内容（每章约{target_words}字）需要通过AI逐章生成。\n\n"
    full_content += "## 生成建议\n\n"
    full_content += "1. 根据大纲中的故事线，逐章生成具体内容\n"
    full_content += "2. 每章可指定章节号和剧情要点\n"
    full_content += "3. 保持人物设定和世界观的一致性\n"
    full_content += "4. 注意情节的连贯性和节奏把控\n"
    
    content_data = {
        'type': 'novel',
        'title': title,
        'content': full_content,
        'params': data,
        'created_at': datetime.now().isoformat()
    }
    save_content(content_data)
    
    return jsonify({'success': True, 'content': full_content})

@app.route('/api/generate/script', methods=['POST'])
def api_generate_script():
    data = request.json
    title = data.get('title', '')
    genre = data.get('genre', '都市情感')
    episode_count = int(data.get('episode_count', 80))
    episode_duration = data.get('episode_duration', '3分钟')
    theme = data.get('theme', '')
    main_characters = data.get('main_characters', '')
    plot_summary = data.get('plot_summary', '')
    
    outline_result = generate_script_outline(
        title=title,
        genre=genre,
        episode_count=episode_count,
        episode_duration=episode_duration,
        theme=theme,
        main_characters=main_characters,
        plot_summary=plot_summary
    )
    
    scene_result = generate_script_scene(
        script_title=title,
        episode_number=1,
        scene_number=1,
        scene_outline='',
        previous_scenes=outline_result,
        genre=genre
    )
    
    full_content = f"# 《{title}》完整短剧内容\n\n"
    full_content += f"## 短剧大纲\n\n{outline_result}\n\n"
    full_content += f"## 第1集第1场示例\n\n{scene_result}\n\n"
    full_content += "---\n\n> 注：以上为短剧大纲和第1集示例内容。\n"
    full_content += "> 完整{episode_count}集内容（每集约{episode_duration}）需要通过AI逐集生成。\n\n"
    full_content += "## 生成建议\n\n"
    full_content += "1. 根据大纲中的剧情线，逐集生成具体场景\n"
    full_content += "2. 每集可指定集数和场景要点\n"
    full_content += "3. 保持人物性格和剧情逻辑的一致性\n"
    full_content += "4. 注意节奏把控和悬念设置\n"
    
    content_data = {
        'type': 'script',
        'title': title,
        'content': full_content,
        'params': data,
        'created_at': datetime.now().isoformat()
    }
    save_content(content_data)
    
    return jsonify({'success': True, 'content': full_content})

@app.route('/api/generate/rewrite', methods=['POST'])
def api_rewrite_text():
    data = request.json
    result = rewrite_text(
        text=data.get('text', ''),
        style=data.get('style', '文艺'),
        requirements=data.get('requirements', '')
    )
    
    content_data = {
        'type': 'rewrite',
        'title': f"重写 - {data.get('style', '文艺')}",
        'content': result,
        'params': data,
        'created_at': datetime.now().isoformat()
    }
    save_content(content_data)
    
    return jsonify({'success': True, 'content': result})

@app.route('/api/generate/polish', methods=['POST'])
def api_polish_text():
    data = request.json
    result = polish_text(
        text=data.get('text', ''),
        mode=data.get('mode', '润色'),
        requirements=data.get('requirements', '')
    )
    
    content_data = {
        'type': 'polish',
        'title': f"润色 - {data.get('mode', '润色')}",
        'content': result,
        'params': data,
        'created_at': datetime.now().isoformat()
    }
    save_content(content_data)
    
    return jsonify({'success': True, 'content': result})

@app.route('/api/generate/continue', methods=['POST'])
def api_continue_story():
    data = request.json
    result = continue_story_content(
        previous_content=data.get('previous_content', ''),
        content_type=data.get('content_type', '小说'),
        continuation_length=int(data.get('continuation_length', 1000)),
        direction=data.get('direction', '')
    )
    
    content_data = {
        'type': 'continue',
        'title': f"续写 - {data.get('content_type', '小说')}",
        'content': result,
        'params': data,
        'created_at': datetime.now().isoformat()
    }
    save_content(content_data)
    
    return jsonify({'success': True, 'content': result})

@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_content(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'success': True})
    return jsonify({'error': 'Content not found'}), 404

if __name__ == '__main__':
    print("=" * 60)
    print("AI小说和短剧剧本智能体 - Web界面")
    print("=" * 60)
    print("\n访问地址:")
    print("  本机浏览器: http://localhost:5001")
    print("  局域网:     http://192.168.1.200:5001")
    print("\n按 Ctrl+C 停止服务\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
