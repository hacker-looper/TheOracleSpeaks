import json

def fix_english_spacing(text):
    # 在大小写字母连接处添加空格
    # 例如: WHENIBUYa -> WHEN I BUY a
    result = ''
    for i in range(len(text)):
        result += text[i]
        if i < len(text) - 1:
            # 当前是小写，下一个是大写，插入空格
            if text[i].islower() and text[i+1].isupper():
                result += ' '
            # 当前是大写，下一个是小写，但前一个不是大写 (处理比如 ICALL -> I CALL)
            elif text[i].isupper() and text[i+1].islower() and i > 0 and not text[i-1].isupper():
                result += ' '
    return result

def generate_html():
    with open('redbook_cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Oracle Speaks - Warren Buffett In His Own Words</title>
    <meta name="description" content="Collection of famous quotes and wisdom from Warren Buffett. Flip cards to see original English text. Inspirational investment and life philosophy from the Oracle of Omaha.">
    <meta name="keywords" content="Warren Buffett, quotes, investing, value investing, business wisdom, life philosophy, The Oracle of Omaha, Buffett quotes, investment philosophy">
    <meta name="author" content="The Oracle Speaks">
    <meta name="robots" content="index, follow">

    <!-- Open Graph for social sharing -->
    <meta property="og:title" content="The Oracle Speaks - Warren Buffett In His Own Words">
    <meta property="og:description" content="Browse Warren Buffett's famous quotes with interactive flip cards.">
    <meta property="og:type" content="website">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="The Oracle Speaks - Warren Buffett In His Own Words">
    <meta name="twitter:description" content="Interactive collection of Warren Buffett quotes with bilingual Chinese-English.">

    <!-- Schema.org structured data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "The Oracle Speaks",
        "description": "Interactive collection of Warren Buffett quotes and investment wisdom",
        "author": {
            "@type": "Person",
            "name": "Warren Buffett"
        },
        "keywords": "Warren Buffett, investing quotes, value investing, business wisdom"
    }
    </script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #f8f5f0;
            min-height: 100vh;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 20px;
            background: #ffffff;
            border-radius: 16px;
            border: 1px solid #e6ddd0;
            box-shadow: 0 1px 3px rgba(138, 120, 102, 0.06);
        }

        .header-image {
            width: 120px;
            height: 120px;
            margin: 0 auto 20px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #f8f5f0;
            box-shadow: 0 2px 8px rgba(138, 120, 102, 0.15);
        }

        .header-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .header h1 {
            font-size: 42px;
            font-weight: 300;
            letter-spacing: 8px;
            text-transform: uppercase;
            margin-bottom: 8px;
            color: #5a4a3f;
            text-shadow: none;
        }

        .header h2 {
            font-size: 20px;
            font-weight: 300;
            letter-spacing: 4px;
            color: #8a7866;
            margin-bottom: 0;
            text-transform: uppercase;
        }

        .header .hint {
            font-size: 14px;
            margin-top: 8px;
            color: #a89a8a;
            font-weight: 300;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
            perspective: 1000px;
            margin-bottom: 40px;
            align-items: stretch;
        }

        .card-container {
            perspective: 1000px;
            min-height: 280px;
            cursor: pointer;
            width: 100%;
        }

        .card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
            transform-style: preserve-3d;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(138, 120, 102, 0.15);
        }

        .card-container.flipped .card-inner {
            transform: rotateY(180deg);
        }

        .card-front, .card-back {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            width: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border-radius: 12px;
            padding: 28px;
            height: auto;
            min-height: 100%;
        }

        .card-front {
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(138, 120, 102, 0.08);
        }

        .card-front::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #d4c8b8, #e6ddd0);
            border-radius: 12px 12px 0 0;
        }

        .card-back {
            background: #f4f0ea;
            transform: rotateY(180deg);
            display: flex;
            flex-direction: column;
            justify-content: center;
            border: 1px solid #e6ddd0;
            height: 100%;
        }

        .card-number {
            position: absolute;
            top: 16px;
            right: 20px;
            font-size: 13px;
            color: #8a7866;
            font-weight: 500;
        }

        .quote-text {
            font-size: 18px;
            line-height: 1.7;
            color: #5a4a3f;
            margin-top: 12px;
            letter-spacing: 0.2px;
            text-align: left;
        }

        .quote-text::before {
            content: '"';
            position: absolute;
            left: 18px;
            top: 30px;
            font-size: 50px;
            color: #8a7866;
            opacity: 0.12;
            font-style: normal;
        }

        .quote-source {
            position: absolute;
            bottom: 20px;
            right: 28px;
            font-size: 13px;
            color: #8a7866;
            text-align: right;
        }

        .original-text {
            font-size: 16px;
            line-height: 1.6;
            color: #5a4a3f;
            text-align: left;
            font-style: italic;
        }

        .original-label {
            font-size: 12px;
            color: #8a7866;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
            text-align: left;
        }

        .original-source {
            font-size: 12px;
            color: #8a7866;
            font-style: italic;
            text-align: right;
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid #d4c8b8;
        }

        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 30px;
            justify-content: center;
        }

        .tag {
            padding: 8px 16px;
            background: #ffffff;
            border: 1px solid #e6ddd0;
            border-radius: 20px;
            font-size: 14px;
            color: #5a4a3f;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(138, 120, 102, 0.05);
        }

        .tag:hover {
            background: #8a7866;
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(138, 120, 102, 0.15);
        }

        .tag.active {
            background: #8a7866;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(138, 120, 102, 0.15);
        }

        .search-box {
            max-width: 600px;
            margin: 0 auto 30px;
            position: relative;
        }

        .search-box input {
            width: 100%;
            padding: 16px 24px;
            border: 1px solid #e6ddd0;
            border-radius: 32px;
            font-size: 16px;
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(138, 120, 102, 0.05);
            outline: none;
            font-family: inherit;
            color: #5a4a3f;
        }

        .search-box input::placeholder {
            color: #a89a8a;
        }

        .search-box input:focus {
            box-shadow: 0 4px 16px rgba(138, 120, 102, 0.1);
        }

        .search-box::after {
            content: '🔍';
            position: absolute;
            right: 24px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 20px;
            color: #8a7866;
        }

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
                font-size: 17px;
            }

            .tags {
                justify-content: flex-start;
            }

            .search-box {
                margin: 0 auto 30px;
            }

            .card-container {
                min-height: 300px;
            }
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #8a7866;
            grid-column: 1 / -1;
        }

        .empty-state p {
            font-size: 18px;
        }

        /* 分页样式 */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
            margin: 30px auto 0 auto;
            padding-bottom: 40px;
            width: 100%;
            max-width: 1600px;
        }

        .page-btn {
            min-width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #e6ddd0;
            background: #ffffff;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            color: #5a4a3f;
            transition: all 0.2s ease;
        }

        .page-btn:hover {
            background: #f8f5f0;
            border-color: #8a7866;
        }

        .page-btn.active {
            background: #8a7866;
            color: #ffffff;
            border-color: #8a7866;
        }

        .page-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .page-info {
            margin: 0 16px;
            color: #8a7866;
            font-size: 14px;
        }

        /* 搜索关键词高亮 */
        .search-highlight {
            background: #ffeb3b;
            color: #333333;
            padding: 1px 4px;
            border-radius: 2px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-image">
            <img src="theoraclesays.png" alt="Warren Buffett">
        </div>
        <h1>The Oracle Speaks</h1>
        <h2>Warren Buffett In His Own Words</h2>
    </div>

    <div class="search-box">
        <input type="text" placeholder="搜索语录关键词...">
    </div>

    <div class="tags">
        <div class="tag active" data-tag="all">全部</div>
        <div class="tag" data-tag="投资">投资</div>
        <div class="tag" data-tag="商业">商业</div>
        <div class="tag" data-tag="财富">财富</div>
        <div class="tag" data-tag="人生">人生</div>
    </div>

    <div class="container">
"""

    for card in cards:
        # Escape quotes for JavaScript
        text = card['text'].replace('"', '&quot;')
        # Fix English spacing in original text
        fixed_original = fix_english_spacing(card['original_text'])
        original_text = fixed_original.replace('"', '&quot;')
        source = card['source'].replace('"', '&quot;')
        original_source = card.get('original_source', '').replace('"', '&quot;')

        # For search indexing, use the fixed original text
        search_original = original_text.lower()

        html_content += f"""
        <div class="card-container" data-id="{card['id']}" data-text="{text.lower()}" data-original="{search_original}" data-source="{source.lower()}">
            <div class="card-inner">
                <div class="card-front">
                    <div class="card-number">NO.{card['id']}</div>
                    <div class="quote-text">{text}</div>
                    <div class="quote-source">{source}</div>
                </div>
                <div class="card-back">
                    <div class="original-label">Original / 英文原文</div>
                    <div class="original-text">{original_text}</div>
                    {'<div class="original-source">' + original_source + '</div>' if original_source else ''}
                </div>
            </div>
        </div>
"""

    html_content += """
        <div class="empty-state" style="display: none;">
            <p>未找到匹配的语录</p>
        </div>

        <div class="pagination" id="pagination">
            <!-- 分页由JS动态生成 -->
        </div>
    </div>

    <script>
        // 分页配置
        const CARDS_PER_PAGE = 80; // 4列 x 20行 = 80张/页
        let currentPage = 1;
        let filteredCards = [];
        let allCards = [];

        // 保存原始HTML用于恢复高亮
        allCards = Array.from(document.querySelectorAll('.card-container'));
        filteredCards = allCards;

        // 保存原始HTML
        // 计算每个卡片的正确高度：取正反面中较大值，确保内容完整显示
        // CSS Grid 会自动让同一行所有卡片等高，匹配该行最高卡片
        allCards.forEach(container => {
            const quoteText = container.querySelector('.quote-text');
            const originalText = container.querySelector('.original-text');
            container.dataset.originalHtml = quoteText.innerHTML;
            container.dataset.originalOriginal = originalText.innerHTML;

            const inner = container.querySelector('.card-inner');
            const front = container.querySelector('.card-front');
            const back = container.querySelector('.card-back');

            // 临时不翻转获取真实高度
            container.classList.remove('flipped');
            const frontHeight = front.scrollHeight;

            // 临时翻转获取背面高度
            container.classList.add('flipped');
            const backHeight = back.scrollHeight;

            // 恢复初始状态
            container.classList.remove('flipped');

            // 取最大值设置给容器，确保内容不溢出
            const maxHeight = Math.max(frontHeight, backHeight);
            container.style.minHeight = maxHeight + 'px';
            inner.style.minHeight = maxHeight + 'px';

            // 卡片翻转功能
            container.addEventListener('click', function() {
                this.classList.toggle('flipped');
            });
        });

        // 高亮关键词函数
        function highlightKeyword(element, keyword) {
            if (!keyword) return;
            const text = element.textContent;
            const regex = new RegExp('(' + keyword + ')', 'gi');
            element.innerHTML = text.replace(regex, '<span class="search-highlight">$1</span>');
        }

        // 清除所有高亮
        function clearHighlights() {
            allCards.forEach(container => {
                const quoteText = container.querySelector('.quote-text');
                const originalText = container.querySelector('.original-text');
                quoteText.innerHTML = container.dataset.originalHtml;
                originalText.innerHTML = container.dataset.originalOriginal;
            });
        }

        // 渲染分页
        function renderPagination() {
            const paginationEl = document.getElementById('pagination');
            const totalPages = Math.ceil(filteredCards.length / CARDS_PER_PAGE);

            if (totalPages <= 1) {
                paginationEl.style.display = 'none';
                return;
            } else {
                paginationEl.style.display = 'flex';
            }

            let html = '';

            // 上一页按钮
            html += `<div class="page-btn" id="prev-btn" ${currentPage === 1 ? 'disabled' : ''}>‹</div>`;

            // 页码按钮
            for (let i = 1; i <= totalPages; i++) {
                if (
                    i === 1 ||
                    i === totalPages ||
                    (i >= currentPage - 2 && i <= currentPage + 2)
                ) {
                    html += `<div class="page-btn ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</div>`;
                } else if (
                    (i === currentPage - 3) ||
                    (i === currentPage + 3)
                ) {
                    html += `<span style="align-self:center;color:#8a7866;">...</span>`;
                }
            }

            // 下一页按钮
            html += `<div class="page-btn" id="next-btn" ${currentPage === totalPages ? 'disabled' : ''}>›</div>`;

            // 页码信息
            html += `<span class="page-info">${currentPage} / ${totalPages}，共 ${filteredCards.length} 条</span>`;

            paginationEl.innerHTML = html;

            // 绑定事件
            document.querySelectorAll('.page-btn[data-page]').forEach(btn => {
                btn.addEventListener('click', function() {
                    goToPage(parseInt(this.getAttribute('data-page')));
                });
            });

            document.getElementById('prev-btn').addEventListener('click', function() {
                if (currentPage > 1) {
                    goToPage(currentPage - 1);
                }
            });

            document.getElementById('next-btn').addEventListener('click', function() {
                if (currentPage < totalPages) {
                    goToPage(currentPage + 1);
                }
            });
        }

        // 跳转到指定页
        function goToPage(page) {
            currentPage = page;
            showCurrentPage();
            renderPagination();
            // 滚动到顶部
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // 显示当前页的卡片
        function showCurrentPage() {
            const start = (currentPage - 1) * CARDS_PER_PAGE;
            const end = start + CARDS_PER_PAGE;

            // 先隐藏所有卡片
            allCards.forEach(card => card.style.display = 'none');

            // filteredCards 已经只包含筛选后可见的卡片，直接显示当前页
            filteredCards.slice(start, end).forEach(card => {
                card.style.display = 'block';
            });
        }

        // 重新筛选后更新分页
        function updateFilteredCards() {
            filteredCards = allCards.filter(card => card.style.display !== 'none');
            currentPage = 1;
            showCurrentPage();
            renderPagination();
        }

        // 搜索功能
        const searchInput = document.querySelector('.search-box input');
        const containers = document.querySelectorAll('.card-container');
        const tags = document.querySelectorAll('.tag');
        const emptyState = document.querySelector('.empty-state');
        const containerEl = document.querySelector('.container');

        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase().trim();
            let foundCount = 0;

            // 先清除之前的高亮
            clearHighlights();

            containers.forEach(container => {
                const text = container.getAttribute('data-text');
                const original = container.getAttribute('data-original');
                const source = container.getAttribute('data-source');

                if (text.includes(searchTerm) || original.includes(searchTerm) || source.includes(searchTerm)) {
                    container.style.display = 'block';
                    foundCount++;

                    // 如果有关键词，高亮它
                    if (searchTerm) {
                        const quoteTextEl = container.querySelector('.quote-text');
                        const originalTextEl = container.querySelector('.original-text');
                        highlightKeyword(quoteTextEl, searchTerm);
                        highlightKeyword(originalTextEl, searchTerm);
                    }
                } else {
                    container.style.display = 'none';
                }
            });

            // 显示/隐藏空状态
            if (foundCount === 0) {
                containerEl.style.display = 'none';
                emptyState.style.display = 'block';
                document.getElementById('pagination').style.display = 'none';
            } else {
                containerEl.style.display = 'grid';
                emptyState.style.display = 'none';
                updateFilteredCards();
            }
        });

        // 标签筛选功能
        tags.forEach(tag => {
            tag.addEventListener('click', function() {
                // 移除所有标签的 active 类
                tags.forEach(t => t.classList.remove('active'));
                // 给当前点击的标签添加 active 类
                this.classList.add('active');

                // 清除搜索高亮
                clearHighlights();
                // 清空搜索框
                searchInput.value = '';

                const selectedTag = this.getAttribute('data-tag');

                // 显示/隐藏卡片
                let foundCount = 0;
                containers.forEach(container => {
                    const text = container.getAttribute('data-text');
                    const original = container.getAttribute('data-original');
                    const source = container.getAttribute('data-source');

                    if (selectedTag === 'all') {
                        container.style.display = 'block';
                        foundCount++;
                    } else {
                        const hasTag = text.includes(selectedTag) ||
                                      original.includes(selectedTag) ||
                                      source.includes(selectedTag);
                        container.style.display = hasTag ? 'block' : 'none';
                        if (hasTag) foundCount++;
                    }
                });

                // 检查是否有匹配的卡片
                if (foundCount === 0) {
                    containerEl.style.display = 'none';
                    emptyState.style.display = 'block';
                    document.getElementById('pagination').style.display = 'none';
                } else {
                    containerEl.style.display = 'grid';
                    emptyState.style.display = 'none';
                    updateFilteredCards();
                }
            });
        });

        // 初始化分页
        renderPagination();
        showCurrentPage();
    </script>
</body>
</html>
"""

    with open('redbook_cards_flip_warmbeige.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"成功生成翻转卡片暖米色HTML文件，包含{len(cards)}条语录")

if __name__ == '__main__':
    generate_html()
