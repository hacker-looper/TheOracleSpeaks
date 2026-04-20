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
            background: #e8dcc4;
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
            color: #8b6b3d;
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

    with open('redbook_cards.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"成功生成HTML文件，包含{len(cards)}条语录")

if __name__ == '__main__':
    generate_html()
