import json

def generate_html():
    with open('redbook_cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)
    
    cards_per_page = 20
    total_pages = (len(cards) + cards_per_page - 1) // cards_per_page
    
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>巴菲特语录 - Apple Design</title>
    <style>
        :root {
            --sk-focus-color: #0071e3;
            --sk-body-link-color: {light-bg: #0066cc, dark-bg: #2997ff};
            --bg-primary: #000000;
            --bg-secondary: #f5f5f7;
            --text-primary: #1d1d1f;
            --text-secondary: #ffffff;
            --text-tertiary: rgba(0, 0, 0, 0.8);
            --card-shadow: rgba(0, 0, 0, 0.22) 3px 5px 30px 0px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background: var(--bg-secondary);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.47;
            letter-spacing: -0.022em;
            color: var(--text-primary);
        }

        .container {
            max-width: 980px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 24px;
        }

        .card {
            background: var(--bg-primary);
            border-radius: 12px;
            height: 400px;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            overflow: hidden;
        }

        .card.flipped {
            transform: rotateY(180deg);
        }

        .card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            transform-style: preserve-3d;
            transform: rotateY(0deg);
        }

        .card.flipped .card-inner {
            transform: rotateY(180deg);
        }

        .card-front, .card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border-radius: 12px;
            padding: 32px;
            overflow: hidden;
        }

        .card-front {
            background: var(--bg-primary);
            transform: rotateY(0deg);
        }

        .card-back {
            background: var(--sk-focus-color);
            transform: rotateY(180deg);
            color: var(--text-secondary);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .card-number {
            position: absolute;
            top: 16px;
            right: 20px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-tertiary);
            letter-spacing: 0.05em;
        }

        .quote-text {
            font-size: 17px;
            line-height: 1.4;
            color: var(--text-secondary);
            margin-bottom: 24px;
            font-weight: 400;
            letter-spacing: -0.01em;
        }

        .quote-source {
            font-size: 13px;
            color: var(--text-tertiary);
            font-weight: 400;
            letter-spacing: -0.01em;
        }

        .original-text {
            font-size: 15px;
            color: var(--text-secondary);
            font-style: italic;
            line-height: 1.5;
            text-align: center;
            padding: 20px;
            max-height: 280px;
            overflow-y: auto;
            font-weight: 400;
            letter-spacing: -0.005em;
        }

        .original-text::-webkit-scrollbar {
            width: 4px;
        }

        .original-text::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
        }

        .original-text::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 2px;
        }

        .flip-hint {
            position: absolute;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 11px;
            color: var(--text-tertiary);
            opacity: 0;
            transition: opacity 0.3s ease;
            font-weight: 500;
            letter-spacing: 0.02em;
        }

        .card:hover .flip-hint {
            opacity: 1;
        }

        .header {
            text-align: center;
            margin-bottom: 48px;
            padding: 48px 32px;
            background: var(--bg-primary);
            border-radius: 12px;
        }

        .header h1 {
            font-size: 40px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-secondary);
            letter-spacing: -0.02em;
            line-height: 1.1;
        }

        .header p {
            font-size: 17px;
            color: var(--text-tertiary);
            font-weight: 400;
            letter-spacing: -0.005em;
        }

        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 32px;
            justify-content: center;
        }

        .tag {
            padding: 8px 16px;
            background: var(--bg-primary);
            border-radius: 980px;
            font-size: 14px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 400;
            letter-spacing: -0.005em;
            border: 1px solid transparent;
        }

        .tag:hover {
            background: var(--sk-focus-color);
            color: var(--text-secondary);
            transform: translateY(-1px);
        }

        .tag.active {
            background: var(--sk-focus-color);
            color: var(--text-secondary);
            box-shadow: 0 0 0 1px var(--sk-focus-color);
        }

        .search-box {
            max-width: 580px;
            margin: 0 auto 32px;
            position: relative;
        }

        .search-box input {
            width: 100%;
            padding: 14px 20px;
            border: none;
            border-radius: 980px;
            font-size: 17px;
            background: var(--bg-primary);
            color: var(--text-secondary);
            outline: none;
            font-weight: 400;
            letter-spacing: -0.005em;
            transition: all 0.2s ease;
        }

        .search-box input:focus {
            box-shadow: 0 0 0 2px var(--sk-focus-color);
        }

        .search-box input::placeholder {
            color: var(--text-tertiary);
        }

        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 16px;
            margin-top: 48px;
            padding: 20px 0;
        }

        .pagination-btn {
            padding: 10px 20px;
            background: var(--bg-primary);
            border: 1px solid transparent;
            border-radius: 980px;
            font-size: 14px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 400;
            letter-spacing: -0.005em;
            min-width: 80px;
        }

        .pagination-btn:hover:not(:disabled) {
            background: var(--sk-focus-color);
            color: var(--text-secondary);
        }

        .pagination-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }

        .pagination-info {
            font-size: 14px;
            color: var(--text-tertiary);
            font-weight: 400;
            letter-spacing: -0.005em;
            min-width: 120px;
            text-align: center;
        }

        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
                gap: 16px;
            }

            .header h1 {
                font-size: 32px;
            }

            .header p {
                font-size: 15px;
            }

            .quote-text {
                font-size: 15px;
            }

            .tags {
                justify-content: flex-start;
            }

            .search-box {
                margin: 0 auto 24px;
            }

            .pagination {
                margin-top: 32px;
                padding: 16px 0;
            }

            .pagination-btn {
                padding: 8px 16px;
                font-size: 13px;
                min-width: 70px;
            }
        }

        .empty-state {
            text-align: center;
            padding: 80px 20px;
            color: var(--text-tertiary);
        }

        .empty-state p {
            font-size: 17px;
            font-weight: 400;
            letter-spacing: -0.005em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>沃伦·巴菲特经典语录</h1>
        <p>投资哲学 · 人生智慧 · 商业思维</p>
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

    <div class="container" id="card-container">
"""

    for card in cards:
        html_content += f"""
        <div class="card" data-id="{card['id']}">
            <div class="card-inner">
                <div class="card-front">
                    <div class="card-number">NO.{card['id']}</div>
                    <div class="quote-text">{card['text']}</div>
                    <div class="quote-source">
                        {card['source']}
                    </div>
                    <div class="flip-hint">双击查看英文原文</div>
                </div>
                <div class="card-back">
                    <div class="original-text">{card['original_text']}</div>
                    <div class="flip-hint">双击返回中文</div>
                </div>
            </div>
        </div>
"""

    html_content += """
    </div>

    <div class="pagination">
        <button class="pagination-btn" id="prev-btn" disabled>← 上一页</button>
        <span class="pagination-info" id="page-info">第 1 / {total_pages} 页</span>
        <button class="pagination-btn" id="next-btn">下一页 →</button>
    </div>

    <div class="empty-state" id="empty-state" style="display: none;">
        <p>未找到匹配的语录</p>
    </div>

    <script>
        const cards = document.querySelectorAll('.card');
        const totalCards = cards.length;
        const cardsPerPage = 20;
        let currentPage = 1;
        const totalPages = Math.ceil(totalCards / cardsPerPage);
        
        // 初始化显示
        function showPage(page) {
            currentPage = page;
            const startIndex = (page - 1) * cardsPerPage;
            const endIndex = Math.min(startIndex + cardsPerPage, totalCards);
            
            cards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
            
            updatePagination();
        }
        
        // 更新分页控件
        function updatePagination() {
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');
            const pageInfo = document.getElementById('page');
            
            prevBtn.disabled = currentPage === 1;
            nextBtn.disabled = currentPage === totalPages;
            pageInfo.textContent = `第 ${currentPage} / ${totalPages} 页`;
        }
        
        // 卡片翻转功能
        cards.forEach(card => {
            card.addEventListener('dblclick', function() {
                this.classList.toggle('flipped');
            });
        });

        // 分页按钮事件
        document.getElementById('prev-btn').addEventListener('click', function() {
            if (currentPage > 1) {
                showPage(currentPage - 1);
            }
        });

        document.getElementById('next-btn').addEventListener('click', function() {
            if (currentPage < totalPages) {
                showPage(currentPage + 1);
            }
        });

        // 搜索功能
        const searchInput = document.querySelector('.search-box input');
        const tags = document.querySelectorAll('.tag');
        const emptyState = document.getElementById('empty-state');

        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            let foundCount = 0;

            cards.forEach(card => {
                const quoteText = card.querySelector('.quote-text').textContent.toLowerCase();
                const originalText = card.querySelector('.original-text').textContent.toLowerCase();
                const source = card.querySelector('.quote-source').textContent.toLowerCase();

                if (quoteText.includes(searchTerm) || originalText.includes(searchTerm) || source.includes(searchTerm)) {
                    card.style.display = 'block';
                    foundCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // 显示/隐藏空状态
            if (foundCount === 0) {
                document.getElementById('card-container').style.display = 'none';
';
                emptyState.style.display = 'block';
                document.querySelector('.pagination').style.display = 'none';
            } else {
                document.getElementById('card-container').style.display = 'grid';
                emptyState.style.display = 'none';
                document.querySelector('.pagination').style.display = 'flex';
            }
        });

        // 标签筛选功能
        tags.forEach(tag => {
            tag.addEventListener('click', function() {
                // 移除所有标签的 active 类
                tags.forEach(t => t.classList.remove('active'));
                // 给当前点击的标签添加 active 类
                this.classList.add('active');

                const selectedTag = this.getAttribute('data-tag');

                // 显示/隐藏卡片
                cards.forEach(card => {
                    const quoteText = card.querySelector('.quote-text').textContent.toLowerCase();
                    const originalText = card.querySelector('.original-text').textContent.toLowerCase();
                    const source = card.querySelector('.quote-source').textContent.toLowerCase();

                    if (selectedTag === 'all') {
                        card = 'block';
                    } else {
                        const hasTag = quoteText.includes(selectedTag) ||
                                      originalText.includes(selectedTag) ||
                                      source.includes(selectedTag);
                        card.style.display = hasTag ? 'block' : 'none';
                    }
                });

                // 检查是否有匹配的卡片
                const visibleCards = document.querySelectorAll('.card[style*="block"]');
                if (visibleCards.length === 0) {
                    document.getElementById('card-container').style.display = 'none';
                    emptyState.style.display = 'block';
                    document.querySelector('.pagination').style.display = 'none';
                } else {
                    document.getElementById('card-container').style.display = 'grid';
                    emptyState.style.display = 'none';
                    document.querySelector('.pagination').style.display = 'flex';
                }
            });
        });

        // 初始化第一页
        showPage(1);
    </script>
</body>
</html>
"""

    with open('redbook_cards.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"成功生成Apple设计HTML文件，包含{len(cards)}条语录，支持分页功能")

if __name__ == '__main__':
    generate_html()
