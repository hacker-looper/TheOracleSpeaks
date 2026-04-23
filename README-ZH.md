# The Oracle Speaks

[English](README.md) | [中文](README-ZH.md)

这是一个以沃伦·巴菲特语录为主题的展示网站项目，基于结构化语录数据生成网页，采用暖米色编辑感视觉风格，并支持搜索、分类筛选和分页阅读。

![项目截图](docs/image.png)

## 当前版本特性

- 英文优先的语录卡片
- 暖米色编辑感页面风格
- 类别标签：`Investing`、`Business`、`Wealth`、`Life`
- 支持按语录正文和来源搜索
- 支持类别筛选
- 每页 12 条分页浏览
- 顶部提供亚马逊购书链接
- 兼容桌面端和移动端

## 主要文件

```text
TheOracleSpeaks/
├── README.md
├── README-ZH.md
├── redbook_cards.json
├── redbook_cards.html
├── redbook_cards_warmbeige.html
├── redbook_cards_flip_warmbeige.html
├── redbook_cards_flip_warmbeige_redesign.html
├── generate_html.py
├── generate_html_warmbeige.py
├── generate_html_flip.py
├── generate_html_flip_warmbeige.py
├── generate_html_mobile_swipe.py
├── generate_apple_design.py
├── parse_quotes.py
├── start-server.ps1
├── theoraclesays.png
├── docs/
│   └── image.png
└── temp/
```

## 推荐入口页面

当前推荐直接打开：

```text
redbook_cards_flip_warmbeige_redesign.html
```

## 快速开始

### 1. 直接打开页面

```powershell
start .\redbook_cards_flip_warmbeige_redesign.html
```

### 2. 或启动本地服务

```powershell
.\start-server.ps1
```

然后访问：

```text
http://localhost:8000/redbook_cards_flip_warmbeige_redesign.html
```

## 数据格式

`redbook_cards.json` 中每条语录包含以下字段：

```json
{
  "id": 1,
  "text": "中文译文",
  "source": "中文来源",
  "original_text": "英文原文",
  "original_source": "英文来源"
}
```

## 当前说明

- 当前改版页以英文语录展示为主
- 仓库中已不再保留本地 EPUB 原文件
- 首页按钮已改为跳转到亚马逊购书入口，而不是下载本地电子书

## 技术栈

- HTML5
- CSS3
- JavaScript
- Python
- PowerShell

## 许可证

项目采用 Apache License 2.0，详见 [LICENSE](LICENSE)。
