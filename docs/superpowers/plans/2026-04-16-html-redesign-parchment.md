# HTML页面优化 - 羊皮纸拟物风格 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有的巴菲特语录卡片HTML页面重新设计为羊皮纸拟物风格，保持原有搜索和筛选功能不变。

**Architecture:** 修改 `generate_html.py` 文件中的CSS样式部分，将配色和视觉效果更新为羊皮纸拟物风格。重新生成HTML文件即可。架构和功能保持不变，只改样式。

**Tech Stack:** Python生成静态HTML + CSS + 原生JavaScript。不需要引入外部库。

---

### Task 1: 更新CSS样式 - 整体背景和基础样式

**Files:**
- Modify: `generate_html.py:1-244` (CSS样式部分)

- [ ] **Step 1: 更新body和整体背景样式**

将原有的:
```css
body {
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: #f5f5f5;
    min-height: 100vh;
    padding: 20px;
}
```

替换为羊皮纸风格:
```css
body {
    font-family: 'Georgia', 'Times New Roman', serif;
    background: #e8dcc4;
    min-height: 100vh;
    padding: 20px;
}
```

- [ ] **Step 2: 更新卡片样式**

将原有的:
```css
.card {
    background: white;
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, #ff4757, #ffa502, #fffa65);
}
```

替换为羊皮纸风格:
```css
.card {
    background: #f4e9cb;
    background-image: 
        radial-gradient(circle at 0 0, rgba(166, 130, 85, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 100% 100%, rgba(166, 130, 85, 0.15) 0%, transparent 50%);
    border-radius: 4px;
    padding: 28px;
    border: 1px solid #d4c49a;
    box-shadow: inset 0 0 30px rgba(166, 130, 85, 0.1), 1px 1px 3px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}

.card:hover {
    box-shadow: inset 0 0 30px rgba(166, 130, 85, 0.1), 2px 2px 8px rgba(0, 0, 0, 0.15);
}
```

- [ ] **Step 3: 更新文字颜色样式**

将原有的:
```css
.card-number {
    position: absolute;
    top: 20px;
    right: 24px;
    font-size: 14px;
    color: #999;
    font-weight: 500;
}

.quote-text {
    font-size: 18px;
    line-height: 1.7;
    color: #222;
    margin-bottom: 20px;
    font-style: normal;
    padding-left: 20px;
    border-left: 4px solid #ff4757;
    position: relative;
}

.quote-text::before {
    content: '"';
    position: absolute;
    left: -10px;
    top: -10px;
    font-size: 60px;
    color: #ff4757;
    opacity: 0.1;
    font-style: normal;
}

.quote-source {
    font-size: 13px;
    color: #666;
    text-align: right;
    padding-top: 16px;
    border-top: 1px solid #f0f0f0;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.original-text {
    font-size: 12px;
    color: #999;
    margin-top: 8px;
    font-style: italic;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
```

替换为羊皮纸风格:
```css
.card-number {
    position: absolute;
    top: 20px;
    right: 24px;
    font-size: 14px;
    color: #8b6b3d;
    font-weight: 500;
}

.quote-text {
    font-size: 18px;
    line-height: 1.7;
    color: #5c431e;
    margin-bottom: 20px;
    font-style: normal;
    padding-left: 20px;
    border-left: 4px solid #d4c49a;
    position: relative;
    letter-spacing: 0.3px;
}

.quote-text::before {
    content: '"';
    position: absolute;
    left: -10px;
    top: -10px;
    font-size: 60px;
    color: #8b6b3d;
    opacity: 0.15;
    font-style: normal;
}

.quote-source {
    font-size: 13px;
    color: #8b6b3d;
    text-align: right;
    padding-top: 16px;
    border-top: 1px solid #d4c49a;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    font-style: italic;
}

.original-text {
    font-size: 12px;
    color: #a08558;
    margin-top: 8px;
    font-style: italic;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
```

- [ ] **Step 4: 更新Header头部样式**

将原有的:
```css
.header {
    text-align: center;
    margin-bottom: 40px;
    padding: 30px 20px;
    background: linear-gradient(135deg, #ff4757 0%, #ffa502 100%);
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(255, 71, 87, 0.2);
}

.header h1 {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 12px;
    color: white;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
}

.header p {
    font-size: 18px;
    color: white;
    opacity: 0.95;
    font-weight: 300;
}
```

替换为羊皮纸风格:
```css
.header {
    text-align: center;
    margin-bottom: 40px;
    padding: 30px 20px;
    background: linear-gradient(135deg, #8b6b3d 0%, #d4c49a 100%);
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(139, 107, 61, 0.2);
    border: 1px solid #5c431e;
}

.header h1 {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 12px;
    color: #fff9ef;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
}

.header p {
    font-size: 18px;
    color: #fff9ef;
    opacity: 0.95;
    font-weight: 300;
}
```

- [ ] **Step 5: 更新标签和搜索框样式**

将原有的:
```css
.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 30px;
    justify-content: center;
}

.tag {
    padding: 8px 16px;
    background: white;
    border-radius: 20px;
    font-size: 14px;
    color: #666;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.tag:hover {
    background: #ff4757;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(255, 71, 87, 0.3);
}

.tag.active {
    background: #ff4757;
    color: white;
    box-shadow: 0 4px 16px rgba(255, 71, 87, 0.3);
}

.search-box {
    max-width: 600px;
    margin: 0 auto 40px;
    position: relative;
}

.search-box input {
    width: 100%;
    padding: 16px 24px;
    border: none;
    border-radius: 32px;
    font-size: 16px;
    background: white;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
    outline: none;
    font-family: inherit;
}

.search-box input:focus {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.search-box::after {
    content: '🔍';
    position: absolute;
    right: 24px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
    color: #999;
}
```

替换为羊皮纸风格:
```css
.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 30px;
    justify-content: center;
}

.tag {
    padding: 8px 16px;
    background: #f4e9cb;
    border: 1px solid #d4c49a;
    border-radius: 20px;
    font-size: 14px;
    color: #5c431e;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(139, 107, 61, 0.1);
}

.tag:hover {
    background: #8b6b3d;
    color: #fff9ef;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(139, 107, 61, 0.2);
}

.tag.active {
    background: #8b6b3d;
    color: #fff9ef;
    box-shadow: 0 4px 12px rgba(139, 107, 61, 0.2);
}

.search-box {
    max-width: 600px;
    margin: 0 auto 40px;
    position: relative;
}

.search-box input {
    width: 100%;
    padding: 16px 24px;
    border: 1px solid #d4c49a;
    border-radius: 32px;
    font-size: 16px;
    background: #f4e9cb;
    box-shadow: inset 0 1px 3px rgba(139, 107, 61, 0.1);
    outline: none;
    font-family: inherit;
    color: #5c431e;
}

.search-box input::placeholder {
    color: #a08558;
}

.search-box input:focus {
    box-shadow: inset 0 1px 3px rgba(139, 107, 61, 0.1), 0 4px 12px rgba(139, 107, 61, 0.15);
}

.search-box::after {
    content: '🔍';
    position: absolute;
    right: 24px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
    color: #8b6b3d;
}
```

- [ ] **Step 6: 更新空状态样式**

将原有的:
```css
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #999;
}
```

替换为:
```css
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #8b6b3d;
}
```

- [ ] **Step 7: 更新移动端响应式样式**

保持文字颜色继承，不需要大改，确认 `quote-text` 字号适配:

```css
@media (max-width: 768px) {
    .container {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .header h1 {
        font-size: 28px;
    }

    .header p {
        font-size: 16px;
    }

    .quote-text {
        font-size: 16px;
        padding-left: 16px;
    }

    .tags {
        justify-content: flex-start;
    }

    .search-box {
        margin: 0 auto 30px;
    }
}
```

- [ ] **Step 8: 保存修改并重新生成HTML**

运行Python脚本重新生成HTML:
```bash
python generate_html.py
```

- [ ] **Step 9: 验证生成结果**

检查 `redbook_cards.html` 是否成功生成，样式是否正确。

- [ ] **Step 10: Commit**

```bash
git add generate_html.py redbook_cards.html docs/superpowers/plans/2026-04-16-html-redesign-parchment.md
git commit -m "style: redesign HTML to parchment paper (vintage skeuomorphic)

- Update all colors to parchment brown palette
- Add radial gradient texture for paper effect
- Use inset shadows to simulate paper thickness
- Change font to serif for vintage feel
- Keep all original search and filter functionality
"
```

---

### Task 2: 验证功能完整性

**Files:**
- Test: 手动验证 `redbook_cards.html` 在浏览器中打开

- [ ] **Step 1: 在浏览器中打开 redbook_cards.html**

在浏览器中打开文件，验证整体风格是否是羊皮纸拟物效果。

- [ ] **Step 2: 验证搜索功能**

输入关键词搜索，验证筛选是否正常工作。

- [ ] **Step 3: 验证标签筛选功能**

点击各个标签，验证筛选是否正常工作。

- [ ] **Step 4: 验证移动端响应式布局**

调整浏览器窗口大小，验证布局自适应。

