# AI小说和短剧剧本智能体

基于 MCP (Model Context Protocol) 的 AI 小说和短剧剧本生成工具，配合 Trae IDE 内置 AI 使用，可生成完整的小说大纲、章节内容以及短剧剧本。

## 功能特性

- **小说生成**：自动生成小说大纲（五卷结构）、章节内容，支持玄幻、都市、仙侠、科幻等多种类型
- **短剧剧本生成**：生成短剧大纲（五阶段结构）、场景内容，适合短视频平台传播特性
- **内容管理**：支持保存、查看、删除已生成的内容
- **Web 界面**：提供可视化 Web 界面，无需登录即可使用
- **MCP 集成**：完美集成 Trae IDE，通过对话方式生成和保存内容

## 项目结构

```
novel-agent/
├── mcp-server/              # MCP 服务器（Trae 集成）
│   ├── server.py           # MCP Server 主程序
│   ├── start.py            # 启动脚本
│   ├── requirements.txt    # Python 依赖
│   ├── trae-mcp-config.json # MCP 配置文件
│   ├── MCP_CONFIG.md       # MCP 配置说明文档
│   └── tools/              # 生成工具模块
│       ├── novel.py        # 小说生成工具（大纲、章节、重写、润色）
│       ├── script.py       # 短剧生成工具（大纲、场景）
│       ├── story.py        # 故事续写工具
│       └── storage.py      # 存储工具
└── web-app/                # Web 应用
    ├── app.py              # Flask 主应用
    ├── requirements.txt    # Python 依赖
    ├── start.sh            # Web 服务启动脚本
    ├── templates/
    │   └── index.html      # Web 界面模板
    └── content/            # 生成的内容存储目录（JSON 文件）
```

## 快速开始

### 环境要求

- Python 3.8+
- Trae IDE（用于 MCP 集成）

### 安装步骤

1. **克隆或下载项目**

```bash
cd novel-agent
```

2. **安装 Web 应用依赖**

```bash
cd web-app
pip install -r requirements.txt
```

3. **安装 MCP 服务器依赖**

```bash
cd ../mcp-server
pip install -r requirements.txt
```

### 启动服务

#### 方式一：Web 界面（直接生成内容）

```bash
cd web-app
python3 app.py
# 或使用启动脚本
./start.sh
```

访问 http://localhost:5001 即可使用 Web 界面。

#### 方式二：MCP 集成（配合 Trae IDE 使用）

在 Trae IDE 中配置 MCP Server：

1. 打开 Trae 设置，找到 MCP Servers 配置
2. 添加以下配置：

```json
{
  "mcpServers": {
    "novel-script-agent": {
      "command": "python",
      "args": [
        "/你的项目路径/novel-agent/mcp-server/server.py"
      ],
      "env": {},
      "disabled": false
    }
  }
}
```

3. 配置完成后，Trae 即可使用 MCP 工具。

## 使用方式

### Web 界面使用

1. 启动 Web 服务后，访问 http://localhost:5001
2. 选择「小说生成」或「短剧生成」标签
3. 填写基本信息：
   - **小说**：标题、类型、主题思想、人物设定、世界观设定、目标章节数、每章字数
   - **短剧**：标题、类型、总集数、每集时长、主题、人物设定、剧情简介
4. 点击「生成」按钮，即可看到生成的内容
5. 在页面底部「历史记录」中可查看和删除已生成的内容

### Trae IDE MCP 使用

配置好 MCP Server 后，在 Trae 对话框中直接使用自然语言请求生成内容。

#### 小说生成示例

```
请帮我生成一部武侠小说：
- 小说标题：《武松大战松江》
- 小说类型：武侠
- 主题思想：侠义精神
- 主要人物设定：武松（主角）；苏清雪（女主）；宋江（反派）
- 世界观设定：水浒传世界观
- 目标章节数：200
- 每章字数：3000
```

生成后，让 Trae 调用 `save_novel_content` 保存到 Web 页面。

#### 短剧生成示例

```
请帮我生成一部都市情感短剧：
- 短剧标题：《总裁的替身娇妻》
- 短剧类型：都市情感
- 总集数：80
- 每集时长：3分钟
- 主题：替身娇妻逆袭复仇
- 主要人物设定：苏雨薇（女主）；顾寒舟（男主）
- 剧情简介：女主被当作替身嫁入豪门，发现真相后逆袭复仇
```

生成后，让 Trae 调用 `save_script_content` 保存到 Web 页面。

## MCP 工具列表

| 工具名 | 功能说明 | 参数 |
|--------|---------|------|
| `save_novel_content` | 保存小说内容 | title, content, genre, theme, main_characters, world_building, target_chapters, target_words_per_chapter |
| `save_script_content` | 保存短剧内容 | title, content, genre, episode_count, episode_duration, theme, main_characters, plot_summary |
| `list_saved_contents` | 列出已保存内容 | content_type（可选） |
| `get_content_by_title` | 根据标题获取内容 | title |
| `delete_content_by_title` | 根据标题删除内容 | title |
| `get_saved_contents_list` | 列出已保存内容（别名） | content_type（可选） |

## API 接口

Web 应用提供以下 REST API：

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/contents` | GET | 获取所有内容列表 |
| `/api/content/<filename>` | GET | 获取指定内容 |
| `/api/save-content` | POST | 保存新内容 |
| `/api/delete/<filename>` | DELETE | 删除指定内容 |
| `/api/generate/novel` | POST | 生成小说 |
| `/api/generate/script` | POST | 生成短剧 |
| `/api/generate/rewrite` | POST | 重写文本 |
| `/api/generate/polish` | POST | 润色文本 |
| `/api/generate/continue` | POST | 续写故事 |

## 生成内容结构

### 小说大纲（五卷结构）

- **第一卷：启程** - 主角出场，建立人物关系，埋下伏笔
- **第二卷：成长** - 实力提升，结识伙伴，对抗初期反派
- **第三卷：转折** - 剧情转折，重大挫折，心态转变
- **第四卷：决战** - 中期 BOSS 决战，揭示更大阴谋
- **第五卷：终章** - 最终决战，伏笔揭晓，圆满收尾

### 短剧大纲（五阶段结构）

- **第一阶段：开局引入** - 人物出场，核心冲突，设置悬念
- **第二阶段：矛盾升级** - 矛盾升级，人物关系变化，剧情反转
- **第三阶段：高潮迭起** - 剧情高潮，秘密揭露，命运转折
- **第四阶段：解决危机** - 最大危机，最终反派，突破困境
- **第五阶段：完美结局** - 大结局，伏笔揭晓，圆满收尾

## 配置说明

### 环境变量

- `WEB_API_BASE`：Web 服务地址，默认 `http://localhost:5001`

### 内容存储

所有生成的内容以 JSON 格式保存在 `web-app/content/` 目录下，文件名格式为：`YYYYMMDD_HHMMSS_类型.json`

## 技术栈

- **后端**：Python, Flask, MCP (Model Context Protocol)
- **前端**：HTML, CSS, JavaScript
- **依赖库**：
  - `flask>=3.0.0` - Web 框架
  - `mcp>=0.9.0` - MCP 协议支持
  - `httpx>=0.24.0` - HTTP 客户端
  - `pydantic>=2.0.0` - 数据验证

## 注意事项

1. 确保已安装 Python 3.8+ 环境
2. 首次使用需要安装依赖：`pip install -r requirements.txt`
3. 当前为 Demo 版本，生成的是模板大纲内容
4. 后续版本将接入真实的 AI 模型来生成详细内容
5. MCP 配置路径需要根据实际项目路径调整

## 后续规划

- [ ] 接入真实 AI 模型生成详细内容
- [ ] 支持更多小说和短剧类型
- [ ] 增加内容导出功能（PDF, Word, TXT）
- [ ] 支持多语言生成
- [ ] 增加人物关系图谱可视化
