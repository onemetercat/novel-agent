# Trae MCP 配置 - AI小说和短剧剧本智能体

## 配置方法

在 Trae IDE 中，打开设置，找到 MCP Servers 配置，添加以下配置：

### 方法一：使用 Python 直接运行（推荐）

```json
{
  "mcpServers": {
    "novel-script-agent": {
      "command": "python",
      "args": [
        "/Users/riceballs/Desktop/code/trae_app/novel/novel-agent/mcp-server/server.py"
      ],
      "env": {},
      "disabled": false
    }
  }
}
```

### 方法二：使用虚拟环境

```json
{
  "mcpServers": {
    "novel-script-agent": {
      "command": "/Users/riceballs/Desktop/code/trae_app/novel/novel-agent/venv/bin/python",
      "args": [
        "/Users/riceballs/Desktop/code/trae_app/novel/novel-agent/mcp-server/server.py"
      ],
      "env": {},
      "disabled": false
    }
  }
}
```

## 可用工具

配置完成后，Trae 可以使用以下工具：

### 小说工具

1. **save_novel_content** - 保存小说内容（包含大纲和章节）
   - 参数：标题、内容、类型、主题、人物设定、世界观、目标章节数、每章字数

### 短剧工具

2. **save_script_content** - 保存短剧内容（包含大纲和场景）
   - 参数：标题、内容、类型、集数、每集时长、主题、人物设定、剧情简介

### 通用工具

3. **list_saved_contents** - 列出已保存的内容
4. **get_content_by_title** - 按标题获取内容
5. **delete_content_by_title** - 按标题删除内容

## 使用示例

在 Trae 的对话框中，你可以这样使用：

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

## 注意事项

1. 确保已安装 Python 3.8+ 环境
2. 首次使用需要安装依赖：`pip install -r mcp-server/requirements.txt`
3. 当前是 Demo 版本，生成的是模板内容
4. 后续会接入真实的 AI 模型来生成内容
5. 配置路径需要根据实际项目路径调整
