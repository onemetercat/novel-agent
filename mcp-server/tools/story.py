"""故事续写工具模块"""

def continue_story_content(
    previous_content: str,
    content_type: str = "小说",
    continuation_length: int = 1000,
    direction: str = ""
) -> str:
    """续写故事内容 - Demo版本"""
    
    text_preview = previous_content[:200]
    direction_section = f'### 续写方向\n{direction}\n' if direction else ''
    
    continuation = f"""## 续写内容（类型：{content_type}）

### 原文摘要
{text_preview}...

{direction_section}
### 续写内容
[续写内容 - 待AI生成]

预计字数：{continuation_length}字

---
*注：这是Demo版本，后续会接入AI模型进行实际续写。*
"""
    
    return continuation
