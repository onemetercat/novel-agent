"""短剧剧本生成工具模块"""

def generate_script_outline(
    title: str,
    genre: str = "都市情感",
    episode_count: int = 80,
    episode_duration: str = "3分钟",
    theme: str = "",
    main_characters: str = "",
    plot_summary: str = ""
) -> str:
    """生成短剧剧本大纲 - Demo版本"""
    
    theme_section = f'## 主题\n{theme}\n' if theme else ''
    characters_section = f'## 主要人物\n{main_characters}\n' if main_characters else ''
    plot_section = f'## 剧情简介\n{plot_summary}\n' if plot_summary else ''
    
    start_ep2 = episode_count // 5 + 1
    end_ep2 = episode_count * 2 // 5
    start_ep3 = episode_count * 2 // 5 + 1
    end_ep3 = episode_count * 3 // 5
    start_ep4 = episode_count * 3 // 5 + 1
    end_ep4 = episode_count * 4 // 5
    start_ep5 = episode_count * 4 // 5 + 1
    
    outline = f"""# 《{title}》短剧剧本大纲

## 基本信息
- **类型**：{genre}
- **总集数**：{episode_count}集
- **每集时长**：{episode_duration}
- **总时长**：约{episode_count * 3}分钟

{theme_section}{characters_section}{plot_section}
## 剧本结构

### 第一阶段：开局引入（第1-{episode_count // 5}集）
- 主角出场，设定人物关系
- 展示核心冲突
- 建立剧情基调
- 设置悬念吸引观众

### 第二阶段：矛盾升级（第{start_ep2}-{end_ep2}集）
- 主要矛盾逐步升级
- 人物关系变化
- 增加新角色
- 剧情反转

### 第三阶段：高潮迭起（第{start_ep3}-{end_ep3}集）
- 剧情高潮不断
- 重大秘密揭露
- 角色命运转折
- 情感爆发

### 第四阶段：解决危机（第{start_ep4}-{end_ep4}集）
- 主角面临最大危机
- 最终反派出现
- 团队齐心协力
- 突破困境

### 第五阶段：完美结局（第{start_ep5}-{episode_count}集）
- 大结局
- 所有伏笔揭晓
- 人物归宿
- 圆满收尾

## 短剧特点
- 每集节奏紧凑，信息量大
- 设置多处钩子（Hook）吸引观众
- 注重情感冲突和反转
- 符合短视频平台传播特性

---
*注：这是Demo版本的剧本大纲，后续会接入AI模型生成更详细的内容。*
"""
    
    return outline


def generate_script_scene(
    script_title: str,
    episode_number: int,
    scene_number: int = 1,
    scene_outline: str = "",
    previous_scenes: str = "",
    genre: str = "都市情感"
) -> str:
    """生成短剧剧本场景 - Demo版本"""
    
    scene_outline_section = f'### 场景大纲\n{scene_outline}\n' if scene_outline else ''
    
    scene = f"""# 《{script_title}》

## 第{episode_number}集 - 场景{scene_number}

（Demo版本 - 后续将接入AI模型生成完整内容）

---

### 【场景信息】
- **场景**：[待设定]
- **时间**：[日/夜]
- **地点**：[待设定]
- **人物**：[待设定]

### 【剧情内容】

**[角色A]**
（动作/表情）
台词内容...

**[角色B]**
（动作/表情）
台词内容...

**[角色A]**
（动作/表情）
台词内容...

---

### 【转场】
[转场方式 - 待设定]

---
*生成参数：*
- *类型：{genre}*
- *集数：{episode_number}*
- *场景：{scene_number}*

{scene_outline_section}
*注：这是Demo版本的场景，后续会接入AI模型生成完整内容。*
"""
    
    return scene
