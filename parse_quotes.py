import os
import re
import json
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def extract_quotes():
    temp_dir = 'temp/OEBPS/xhtml'
    quotes = []

    for filename in os.listdir(temp_dir):
        if filename.endswith('.xhtml'):
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

                # 提取所有语录
                quote_tags = soup.find_all('p', class_=['quote', 'quotec', 'quote-in'])
                for quote_tag in quote_tags:
                    quote_text = quote_tag.get_text(strip=True)

                    # 找到来源
                    source = ''
                    next_tag = quote_tag.find_next_sibling()
                    while next_tag:
                        if next_tag.name == 'p' and (next_tag.get('class') == ['right'] or next_tag.get('class') == ['center1']):
                            source = next_tag.get_text(strip=True)
                            break
                        next_tag = next_tag.find_next_sibling()

                    if quote_text:
                        quotes.append({
                            'text': quote_text,
                            'source': source,
                            'filename': filename
                        })
    return quotes

import time
import translators as ts

def translate_text(text, target_lang='zh-CN', retry=3, delay=2):
    # 使用translators库，支持多种翻译引擎
    for i in range(retry):
        try:
            # 尝试使用百度翻译
            return ts.baidu(text, to_language=target_lang)
        except Exception as e:
            print(f"百度翻译失败: {e}，尝试使用Google翻译")
            try:
                return ts.google(text, to_language=target_lang)
            except Exception as e2:
                print(f"Google翻译失败: {e2}，第 {i+1} 次重试")
                time.sleep(delay)
                delay *= 2
    print(f"翻译失败，保留原文: {text}")
    return text

def generate_redbook_cards(quotes):
    cards = []

    for i, quote in enumerate(quotes, 1):
        print(f"正在翻译第 {i} 条语录")
        translated_text = translate_text(quote['text'])
        translated_source = translate_text(quote['source'])

        card = {
            'id': i,
            'text': translated_text,
            'source': translated_source,
            'original_text': quote['text'],
            'original_source': quote['source']
        }
        cards.append(card)
        time.sleep(0.5)  # 避免频率限制

    return cards

def save_cards(cards, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)

def main():
    print("提取语录...")
    quotes = extract_quotes()
    print(f"提取到 {len(quotes)} 条语录")

    print("翻译语录...")
    cards = generate_redbook_cards(quotes)

    print("保存卡片...")
    save_cards(cards, 'redbook_cards.json')

    print("生成小红书卡片HTML...")
    generate_html(cards)

    print("完成！")

def generate_html(cards):
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>巴菲特语录 - 小红书卡片</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['PingFang SC', 'Microsoft YaHei', 'sans-serif']
                    },
                    colors: {
                        primary: '#ff4757',
                        secondary: '#ffa502'
                    }
                }
            }
        }
    </script>
    <style type="text/tailwindcss">
        @layer utilities {
            .card-gradient {
                background: linear-gradient(90deg, #ff4757, #ffa502, #fffa65);
            }
            .header-gradient {
                background: linear-gradient(135deg, #ff4757 0%, #ffa502 100%);
            }
            .quote-mark {
                content: '"';
                position: absolute;
                left: -10px;
                top: -10px;
                font-size: 60px;
                color: #ff4757;
                opacity: 0.1;
                font-style: normal;
            }
            .search-icon {
                content: '🔍';
                position: absolute;
                right: 24px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 20px;
                color: #999;
            }
        }
    </style>
</head>
<body class="font-sans bg-gray-100 min-h-screen p-5 sm:p-5">
    <div class="header-gradient text-center mb-10 p-7 rounded-2xl shadow-lg">
        <h1 class="text-3xl sm:text-4xl font-bold mb-3 text-white text-shadow">📚 沃伦·巴菲特经典语录</h1>
        <p class="text-lg sm:text-xl text-white/95 font-light">投资哲学 · 人生智慧 · 商业思维</p>
    </div>

    <div class="max-w-2xl mx-auto mb-10 relative">
        <input type="text" placeholder="搜索语录关键词..." class="w-full p-4 pl-6 pr-12 rounded-full text-base bg-white shadow-md focus:outline-none focus:shadow-lg transition-all">
        <div class="search-icon"></div>
    </div>

    <div class="flex flex-wrap gap-2 justify-center mb-8">
        <div class="tag active px-4 py-2 bg-white rounded-full text-sm text-gray-600 cursor-pointer transition-all shadow-sm hover:bg-primary hover:text-white hover:-translate-y-0.5 hover:shadow-md" data-tag="all">全部</div>
        <div class="tag px-4 py-2 bg-white rounded-full text-sm text-gray-600 cursor-pointer transition-all shadow-sm hover:bg-primary hover:text-white hover:-translate-y-0.5 hover:shadow-md" data-tag="投资">投资</div>
        <div class="tag px-4 py-2 bg-white rounded-full text-sm text-gray-600 cursor-pointer transition-all shadow-sm hover:bg-primary hover:text-white hover:-translate-y-0.5 hover:shadow-md" data-tag="商业">商业</div>
        <div class="tag px-4 py-2 bg-white rounded-full text-sm text-gray-600 cursor-pointer transition-all shadow-sm hover:bg-primary hover:text-white hover:-translate-y-0.5 hover:shadow-md" data-tag="财富">财富</div>
        <div class="tag px-4 py-2 bg-white rounded-full text-sm text-gray-600 cursor-pointer transition-all shadow-sm hover:bg-primary hover:text-white hover:-translate-y-0.5 hover:shadow-md" data-tag="人生">人生</div>
    </div>

    <div class="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
"""

    for card in cards:
        html_content += f"""
        <div class="bg-white rounded-2xl p-7 shadow-md hover:shadow-xl hover:-translate-y-2 transition-all relative overflow-hidden">
            <div class="card-gradient absolute top-0 left-0 right-0 h-1.5"></div>
            <div class="absolute top-5 right-6 text-sm text-gray-400 font-medium">NO.{card['id']}</div>
            <div class="text-lg leading-relaxed text-gray-800 mb-5 pl-5 border-l-4 border-primary relative">
                <div class="quote-mark"></div>
                {card['text']}
            </div>
            <div class="text-sm text-gray-600 text-right pt-4 border-t border-gray-100 flex flex-col items-end">
                {card['source']}
                <div class="text-xs text-gray-400 mt-2 italic truncate w-full">{card['original_text']}</div>
            </div>
        </div>
"""

    html_content += """
    </div>

    <div class="text-center py-16 text-gray-400" style="display: none;">
        <p class="text-lg">未找到匹配的语录</p>
    </div>

    <script>
        // 搜索功能
        const searchInput = document.querySelector('input[placeholder="搜索语录关键词..."]');
        const cards = document.querySelectorAll('[class*="bg-white rounded-2xl"]');
        const tags = document.querySelectorAll('.tag');
        const emptyState = document.querySelector('[class*="text-center py-16"]');

        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            let foundCount = 0;

            cards.forEach(card => {
                const quoteText = card.querySelector('[class*="text-lg leading-relaxed"]').textContent.toLowerCase();
                const originalText = card.querySelector('[class*="text-xs text-gray-400"]').textContent.toLowerCase();
                const source = card.querySelector('[class*="text-sm text-gray-600"]').textContent.toLowerCase();

                if (quoteText.includes(searchTerm) || originalText.includes(searchTerm) || source.includes(searchTerm)) {
                    card.style.display = 'block';
                    foundCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // 显示/隐藏空状态
            if (foundCount === 0) {
                document.querySelector('[class*="max-w-6xl mx-auto grid"]').style.display = 'none';
                emptyState.style.display = 'block';
            } else {
                document.querySelector('[class*="max-w-6xl mx-auto grid"]').style.display = 'grid';
                emptyState.style.display = 'none';
            }
        });

        // 标签筛选功能
        tags.forEach(tag => {
            tag.addEventListener('click', function() {
                // 重置所有标签的样式
                tags.forEach(t => {
                    t.classList.remove('bg-primary', 'text-white', 'shadow-md');
                    t.classList.add('bg-white', 'text-gray-600', 'shadow-sm');
                });
                // 设置当前标签的激活样式
                this.classList.remove('bg-white', 'text-gray-600', 'shadow-sm');
                this.classList.add('bg-primary', 'text-white', 'shadow-md');

                const selectedTag = this.getAttribute('data-tag');

                // 显示/隐藏卡片
                cards.forEach(card => {
                    const quoteText = card.querySelector('[class*="text-lg leading-relaxed"]').textContent.toLowerCase();
                    const originalText = card.querySelector('[class*="text-xs text-gray-400"]').textContent.toLowerCase();
                    const source = card.querySelector('[class*="text-sm text-gray-600"]').textContent.toLowerCase();

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
                const visibleCards = document.querySelectorAll('[class*="bg-white rounded-2xl"][style*="block"]');
                if (visibleCards.length === 0) {
                    document.querySelector('[class*="max-w-6xl mx-auto grid"]').style.display = 'none';
                    emptyState.style.display = 'block';
                } else {
                    document.querySelector('[class*="max-w-6xl mx-auto grid"]').style.display = 'grid';
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

if __name__ == '__main__':
    main()
