import json

def generate_html():
    with open('redbook_cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>巴菲特语录 - 小红书卡片</title>
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

        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 24px;
        }

        .card {
            background: #ffffff;
            border-radius: 12px;
            padding: 28px;
            box-shadow: 0 2px 8px rgba(138, 120, 102, 0.08);
            transition: box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #d4c8b8, #e6ddd0);
        }

        .card:hover {
            box-shadow: 0 6px 20px rgba(138, 120, 102, 0.15);
        }

        .card-number {
            position: absolute;
            top: 20px;
            right: 24px;
            font-size: 14px;
            color: #8a7866;
            font-weight: 500;
        }

        .quote-text {
            font-size: 18px;
            line-height: 1.7;
            color: #5a4a3f;
            margin-bottom: 20px;
            font-style: normal;
            padding-left: 20px;
            border-left: 4px solid #d4c8b8;
            position: relative;
            letter-spacing: 0.2px;
        }

        .quote-text::before {
            content: '"';
            position: absolute;
            left: -10px;
            top: -10px;
            font-size: 60px;
            color: #8a7866;
            opacity: 0.12;
            font-style: normal;
        }

        .quote-source {
            font-size: 13px;
            color: #8a7866;
            text-align: right;
            padding-top: 16px;
            border-top: 1px solid #e6ddd0;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }

        .original-text {
            font-size: 12px;
            color: #a89a8a;
            margin-top: 8px;
            font-style: italic;
            max-width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 20px;
            background: linear-gradient(135deg, #8a7866 0%, #d4c8b8 100%);
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(138, 120, 102, 0.15);
        }

        .header h1 {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 12px;
            color: #ffffff;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.15);
        }

        .header p {
            font-size: 18px;
            color: #ffffff;
            opacity: 0.95;
            font-weight: 300;
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
            margin: 0 auto 40px;
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

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #8a7866;
        }

        .empty-state svg {
            width: 120px;
            height: 120px;
            margin-bottom: 20px;
            opacity: 0.3;
        }

        .empty-state p {
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 沃伦·巴菲特经典语录</h1>
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

    <div class="container">
"""

    for card in cards:
        html_content += f"""
        <div class="card">
            <div class="card-number">NO.{card['id']}</div>
            <div class="quote-text">{card['text']}</div>
            <div class="quote-source">
                {card['source']}
                <div class="original-text">{card['original_text']}</div>
            </div>
        </div>
"""

    html_content += """
    </div>

    <div class="empty-state" style="display: none;">
        <p>未找到匹配的语录</p>
    </div>

    <script>
        // 搜索功能
        const searchInput = document.querySelector('.search-box input');
        const cards = document.querySelectorAll('.card');
        const tags = document.querySelectorAll('.tag');
        const emptyState = document.querySelector('.empty-state');

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
                document.querySelector('.container').style.display = 'none';
                emptyState.style.display = 'block';
            } else {
                document.querySelector('.container').style.display = 'grid';
                emptyState.style.display = 'none';
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
                        card.style.display = 'block';
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
                    document.querySelector('.container').style.display = 'none';
                    emptyState.style.display = 'block';
                } else {
                    document.querySelector('.container').style.display = 'grid';
                    emptyState.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>
"""

    with open('redbook_cards_warmbeige.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"成功生成暖米色HTML文件，包含{len(cards)}条语录")

if __name__ == '__main__':
    generate_html()
