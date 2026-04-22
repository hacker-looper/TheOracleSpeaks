# The Oracle Speaks - 巴菲特智慧语录

[English](README_ZH.md) | 中文

基于电子书： The Oracle Speaks - David Andrews.epub为内容将epub内容转化为json格式，再生成的 Warren Buffett语录展示网站，精选投资/商业/财富/人生等智慧语录，支持中英文对照和交互式卡片翻转效果。
![alt text](docs/image.png)
@see https://xooper.cn/web/theoraclespeaks/index.html

## 功能特性

- 📚 **精选语录** - 收录巴菲特经典投资智慧
- 🌐 **中英对照** - 每条语录包含中文翻译和英文原文
- 🎴 **卡片翻转效果** - 双击卡片查看英文原文
- 🎨 **精美设计** - 采用Apple风格设计系统
- 🔍 **搜索功能** - 支持按内容搜索语录
- 📄 **分页显示** - 每页显示20条语录
- 📱 **响应式设计** - 支持桌面和移动设备

## 项目结构

```
TheOracleSpeaks/
├── README_ZH.md                    # 项目说明文档（中文）
├── README.md                       # 项目说明文档（英文）
├── redbook_cards.json              # 语录数据
├── redbook_cards.html              # 生成的HTML文件
├── redbook_cards_flip_warmbeige.html  # 温暖米色翻转效果HTML
├── redbook_cards_warmbeige.html    # 温暖米色HTML
├── parse_quotes.py                 # 解析EPUB语录脚本
├── generate_html.py                # 生成HTML的主脚本
├── generate_apple_design.py        # Apple风格HTML生成器
├── generate_html_flip.py           # 带翻转效果的HTML生成器
├── generate_html_flip_warmbeige.py # 温暖米色翻转效果HTML生成器
├── generate_html_warmbeige.py      # 温暖米色HTML生成器
├── generate_html_mobile_swipe.py   # 移动端滑动效果HTML生成器
├── start-server.ps1                # 本地服务器启动脚本
├── theoraclesays.png               # 项目图标/LOGO
├── docs/                           # 文档目录
│   ├── The Oracle Speaks - David Andrews.epub  # 原始EPUB书籍
│   └── image.png                   # 项目截图
└── temp/                           # 临时文件目录
```

## 快速开始

### 1. 生成HTML文件

```powershell / cmd
python generate_html_flip_warmbeige.py
```

### 2. 启动本地服务器

```powershell
# 使用PowerShell启动服务器
.\start-server.ps1
```

服务器将在 `http://localhost:8000/` 启动

### 3. 访问网站

在浏览器中打开 `http://localhost:8000/redbook_cards_flip_warmbeige.html`

## 使用说明

### 查看英文原文
- 双击任意语录卡片即可翻转查看英文原文
- 再次双击返回中文版本

### 搜索语录
- 在页面顶部的搜索框中输入关键词
- 支持搜索中文翻译、英文原文和来源信息

### 分页导航
- 使用底部的"上一页"和"下一页"按钮浏览
- 每页显示20条语录

## 数据格式

每条语录包含以下字段：

```json
{
    "id": 1,
    "text": "中文翻译内容",
    "source": "——来源信息",
    "original_text": "英文原文",
    "original_source": "—英文来源"
}
```

## 数据处理流程

项目使用 `parse_quotes.py` 脚本从EPUB电子书中提取和处理语录数据，主要流程如下：

### 1. 提取语录 (extract_quotes)
- 从 `temp/OEBPS/xhtml` 目录中读取EPUB解压后的XHTML文件
- 使用BeautifulSoup解析HTML，查找包含语录的段落标签（`quote`, `quotec`, `quote-in`）
- 提取语录文本和对应的来源信息
- 返回原始语录列表

### 2. 翻译文本 (translate_text)
- 使用 `translators` 库进行翻译
- 优先使用百度翻译API，失败时自动切换到Google翻译
- 支持重试机制（默认3次）和延迟递增策略
- 翻译失败时保留原文并记录错误

### 3. 生成卡片数据 (generate_redbook_cards)
- 遍历提取的语录列表
- 对每条语录的文本和来源进行中文翻译
- 构建包含中英文对照的卡片数据结构
- 添加延迟避免API频率限制

### 4. 保存数据 (save_cards)
- 将处理完成的卡片数据保存为JSON格式
- 输出文件：`redbook_cards.json`
- 使用UTF-8编码确保中文字符正确保存

### 5. 生成与其他HTML生成脚本
- `generate_html.py` - 基础HTML生成器
- `generate_apple_design.py` - Apple风格设计HTML生成器
- `generate_html_flip.py` - 带翻转效果的HTML生成器
- `generate_html_flip_warmbeige.py` - 温暖米色翻转效果HTML生成器
- `generate_html_warmbeige.py` - 温暖米色HTML生成器
- `generate_html_mobile_swipe.py` - 移动端滑动效果HTML生成器

### 依赖库
- `BeautifulSoup` - HTML解析
- `translators` - 多引擎翻译支持
- `json` - 数据序列化
- `time` - 延迟控制

## 设计规范

项目采用温暖的米色调设计系统，营造优雅舒适的阅读体验：

- **配色方案**：
  - 页面背景：#f8f5f0（温暖米色）
  - 卡片正面：#ffffff（纯白）
  - 卡片背面：#f4f0ea（浅米色）
  - 主要文字：#5a4a3f（深棕色）
  - 次要文字：#8a7866（中棕色）
  - 边框装饰：#e6ddd0, #d4c8b8（浅棕色）

- **字体**：Georgia和Times New Roman衬线字体，营造经典阅读体验

- **卡片设计**：
  - 圆角边框（12px）
  - 微妙的阴影效果
  - 顶部渐变装饰条
  - 3D翻转动画效果

- **交互反馈**：
  - 双击卡片翻转查看英文原文
  - 流畅的0.8秒过渡动画
  - 悬停效果增强视觉反馈

## 技术栈

- **HTML5** - 页面结构
- **CSS3** - 样式和动画效果
- **JavaScript** - 交互逻辑（翻转、搜索、分页）
- **Python** - HTML生成脚本
- **PowerShell** - 本地服务器

## 浏览器兼容性

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## 许可证

本项目内容来源于《The Oracle Speaks - David Andrews》，仅供学习参考使用。

## 贡献

欢迎提交问题和改进建议！
