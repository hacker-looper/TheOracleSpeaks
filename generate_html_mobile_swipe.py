import json

def fix_english_spacing(text):
    # 在大小写字母连接处添加空格
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

    # 预修复英文空格
    for card in cards:
        card['fixed_original'] = fix_english_spacing(card['original_text'])

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>The Oracle Speaks - Mobile</title>
    <meta name="description" content="Swipe through Warren Buffett quotes randomly. Collect your favorites.">
    <meta name="keywords" content="Warren Buffett, quotes, swipe, mobile, random">
    <meta name="robots" content="index, follow">
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
            overflow-x: hidden;
        }

        .header {
            text-align: center;
            padding: 16px 16px 8px;
            background: #ffffff;
            border-bottom: 1px solid #e6ddd0;
            box-shadow: 0 1px 3px rgba(138, 120, 102, 0.06);
        }

        .header img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            margin-bottom: 8px;
            border: 2px solid #f8f5f0;
        }

        .header h1 {
            font-size: 20px;
            font-weight: 300;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: #5a4a3f;
        }

        .header h2 {
            font-size: 12px;
            font-weight: 300;
            color: #8a7866;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 24px;
            margin-top: 12px;
            font-size: 13px;
            color: #8a7866;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            display: block;
            font-size: 18px;
            font-weight: 600;
            color: #5a4a3f;
        }

        /* 卡片容器 */
        .swipe-container {
            position: relative;
            width: 100%;
            height: calc(100vh - 240px);
            padding: 16px;
            overflow: hidden;
        }

        .card-stack {
            position: relative;
            width: 100%;
            height: 100%;
        }

        .quote-card {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #ffffff;
            border-radius: 16px;
            border: 1px solid #e6ddd0;
            box-shadow: 0 4px 16px rgba(138, 120, 102, 0.15);
            padding: 24px;
            cursor: grab;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            transform-origin: center;
        }

        .quote-card.dragging {
            transition: none;
            cursor: grabbing;
        }

        .quote-card.flipped {
            transform: rotateY(180deg);
        }

        .card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }

        .card-front, .card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .card-front {
            background: #ffffff;
        }

        .card-back {
            background: #f4f0ea;
            transform: rotateY(180deg);
            padding: 20px;
        }

        .quote-text {
            font-size: 22px;
            line-height: 1.8;
            color: #5a4a3f;
            text-align: left;
            letter-spacing: 0.2px;
        }

        .quote-text::before {
            content: '"';
            position: absolute;
            left: 8px;
            top: 0;
            font-size: 48px;
            color: #8a7866;
            opacity: 0.12;
            font-style: normal;
        }

        .quote-source {
            position: absolute;
            bottom: 8px;
            right: 24px;
            font-size: 14px;
            color: #8a7866;
            text-align: right;
        }

        .original-label {
            font-size: 11px;
            color: #8a7866;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
            text-align: left;
        }

        .original-text {
            font-size: 18px;
            line-height: 1.6;
            color: #5a4a3f;
            text-align: left;
            font-style: italic;
        }

        .original-source {
            font-size: 13px;
            color: #8a7866;
            font-style: italic;
            text-align: right;
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid #d4c8b8;
        }

        .flip-hint {
            position: absolute;
            bottom: 8px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 11px;
            color: #a89a8a;
            opacity: 0.7;
        }

        /* 指示器 */
        .swipe-hints {
            position: absolute;
            bottom: 16px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-between;
            padding: 0 32px;
            pointer-events: none;
        }

        .hint-left, .hint-right {
            font-size: 12px;
            color: #8a7866;
            opacity: 0.6;
        }

        .hint-left span {
            color: #ff6b6b;
        }

        .hint-right span {
            color: #51cf66;
        }

        /* 按钮 */
        .action-buttons {
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 16px;
            z-index: 100;
        }

        .action-btn {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        .action-btn:hover {
            transform: scale(1.1);
        }

        .action-btn:active {
            transform: scale(0.95);
        }

        .btn-skip {
            background: #ffebee;
            color: #f44336;
        }

        .btn-favorite {
            background: #e8f5e9;
            color: #4caf50;
        }

        .btn-flip {
            background: #fff3e0;
            color: #ff9800;
        }

        /* 收藏抽屉 */
        .favorites-drawer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #ffffff;
            border-top: 1px solid #e6ddd0;
            border-radius: 16px 16px 0 0;
            box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.08);
            max-height: 50vh;
            overflow-y: auto;
            transform: translateY(calc(100% - 56px));
            transition: transform 0.3s ease;
            z-index: 200;
        }

        .favorites-drawer.open {
            transform: translateY(0);
        }

        .drawer-header {
            padding: 16px 20px;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            background: #ffffff;
            z-index: 10;
        }

        .drawer-header h3 {
            font-size: 16px;
            font-weight: 500;
            color: #5a4a3f;
        }

        .toggle-btn {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #8a7866;
            padding: 4px 8px;
        }

        .favorites-list {
            padding: 12px;
        }

        .favorite-item {
            padding: 12px 16px;
            background: #f8f5f0;
            border-radius: 8px;
            margin-bottom: 8px;
            position: relative;
        }

        .favorite-item .quote-text {
            font-size: 16px;
            line-height: 1.6;
            color: #5a4a3f;
            margin-bottom: 8px;
        }

        .favorite-item .quote-source {
            position: static;
            text-align: right;
            font-size: 12px;
        }

        .remove-favorite {
            position: absolute;
            top: 8px;
            right: 8px;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #ffebee;
            color: #f44336;
            border: none;
            cursor: pointer;
            font-size: 14px;
            line-height: 1;
        }

        .empty-favorites {
            text-align: center;
            padding: 40px 20px;
            color: #8a7866;
            font-size: 14px;
        }

        /* 空状态 */
        .no-more-cards {
            display: none;
            text-align: center;
            padding: 40px 20px;
            color: #8a7866;
        }

        .no-more-cards.show {
            display: block;
        }

        .no-more-cards button {
            margin-top: 16px;
            padding: 12px 24px;
            background: #8a7866;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }

        .card-number {
            position: absolute;
            top: 12px;
            right: 16px;
            font-size: 12px;
            color: #8a7866;
        }

        @media (min-width: 768px) {
            .swipe-container {
                max-width: 480px;
                margin: 0 auto;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="theoraclesays.png" alt="Warren Buffett">
        <h1>The Oracle Speaks</h1>
        <h2>Warren Buffett In His Own Words</h2>
        <div class="stats">
            <div class="stat-item">
                <span class="stat-number" id="remaining-count">""" + str(len(cards)) + """</span>
                <span>Remaining</span>
            </div>
            <div class="stat-item">
                <span class="stat-number" id="favorites-count">0</span>
                <span>Favorites</span>
            </div>
        </div>
    </div>

    <div class="swipe-container">
        <div class="card-stack" id="card-stack"></div>
        <div class="swipe-hints">
            <div class="hint-left"><span>←</span> Skip / Dislike</div>
            <div class="hint-right">Save <span>→</span></div>
        </div>
        <div class="no-more-cards" id="no-more">
            <h3>No more cards!</h3>
            <p>You've seen all {total} quotes.</p>
            <button onclick="resetDeck()">Start Over</button>
        </div>
    </div>

    <div class="action-buttons">
        <button class="action-btn btn-skip" onclick="skipCard()" title="Skip">←</button>
        <button class="action-btn btn-flip" onclick="flipCurrentCard()" title="Flip to English">⟳</button>
        <button class="action-btn btn-favorite" onclick="saveFavorite()" title="Save to Favorites">❤️</button>
    </div>

    <div class="favorites-drawer" id="favorites-drawer">
        <div class="drawer-header">
            <h3>My Favorites (<span id="drawer-count">0</span>)</h3>
            <button class="toggle-btn" onclick="toggleFavorites()" id="toggle-btn">▼</button>
        </div>
        <div class="favorites-list" id="favorites-list">
            <div class="empty-favorites">No favorites yet. Tap the heart button to save quotes you like.</div>
        </div>
    </div>

    <script>
        // All quotes data
        const allQuotes = [
"""

    for card in cards:
        text = card['text'].replace('"', '&quot;')
        original = card['fixed_original'].replace('"', '&quot;')
        source = card['source'].replace('"', '&quot;')
        original_source = card.get('original_source', '').replace('"', '&quot;')
        html_content += f'            {{id: {card["id"]}, text: "{text}", original: "{original}", source: "{source}", original_source: "{original_source}"}},\n'

    html_content += """        ];

        let deck = [];
        let favorites = [];
        let currentCard = null;
        let isDragging = false;
        let startX = 0;
        let currentX = 0;

        // Load favorites from localStorage
        function loadFavorites() {
            const saved = localStorage.getItem('buffett_favorites');
            if (saved) {
                favorites = JSON.parse(saved);
            }
            updateStats();
            renderFavorites();
        }

        // Save favorites to localStorage
        function saveFavorites() {
            localStorage.setItem('buffett_favorites', JSON.stringify(favorites));
            updateStats();
        }

        // Shuffle array using Fisher-Yates
        function shuffle(array) {
            const newArray = [...array];
            for (let i = newArray.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
            }
            return newArray;
        }

        // Start a new deck
        function initDeck() {
            deck = shuffle(allQuotes);
            renderNextCard();
            document.getElementById('no-more').classList.remove('show');
            updateStats();
        }

        // Reset and start over
        function resetDeck() {
            initDeck();
        }

        // Render the next card
        function renderNextCard() {
            if (deck.length === 0) {
                document.getElementById('no-more').classList.add('show');
                currentCard = null;
                return;
            }

            const container = document.getElementById('card-stack');
            // Remove old cards
            container.innerHTML = '';

            const quote = deck[deck.length - 1];
            const cardEl = document.createElement('div');
            cardEl.className = 'quote-card';
            cardEl.dataset.id = quote.id;
            cardEl.innerHTML = `
                <div class="card-inner" id="card-inner-${quote.id}">
                    <div class="card-front">
                        <div class="card-number">${deck.length} / ${allQuotes.length}</div>
                        <div class="quote-text">${quote.text}</div>
                        <div class="quote-source">${quote.source}</div>
                    </div>
                    <div class="card-back">
                        <div class="original-label">Original</div>
                        <div class="original-text">${quote.original}</div>
                        ${quote.original_source ? `<div class="original-source">${quote.original_source}</div>` : ''}
                    </div>
                </div>
            `;

            // Touch events for swipe
            cardEl.addEventListener('touchstart', handleTouchStart);
            cardEl.addEventListener('touchmove', handleTouchMove);
            cardEl.addEventListener('touchend', handleTouchEnd);

            // Mouse events for desktop testing
            cardEl.addEventListener('mousedown', handleMouseDown);

            container.appendChild(cardEl);
            currentCard = cardEl;
            isDragging = false;
        }

        // Touch handlers
        function handleTouchStart(e) {
            if (!isDragging) {
                isDragging = true;
                startX = e.touches[0].clientX;
                currentX = startX;
                e.currentTarget.classList.add('dragging');
            }
        }

        function handleTouchMove(e) {
            if (!isDragging) return;
            currentX = e.touches[0].clientX;
            const diff = currentX - startX;
            const rotate = diff / 10;
            e.currentTarget.style.transform = `translateX(${diff}px) rotate(${rotate}deg)`;
        }

        function handleTouchEnd(e) {
            if (!isDragging) return;
            isDragging = false;
            e.currentTarget.classList.remove('dragging');

            const diff = currentX - startX;
            const threshold = 100;

            if (Math.abs(diff) > threshold) {
                // Swiped enough
                if (diff > 0) {
                    // Swiped right - save to favorites
                    saveFavoriteAndRemove();
                } else {
                    // Swiped left - skip
                    skipCard();
                }
            } else {
                // Snap back
                e.currentTarget.style.transform = '';
            }
        }

        // Mouse handlers (for desktop)
        let isMouseDown = false;
        let startMouseX = 0;
        let currentMouseX = 0;

        function handleMouseDown(e) {
            isMouseDown = true;
            startMouseX = e.clientX;
            currentMouseX = startMouseX;
            e.currentTarget.classList.add('dragging');
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
        }

        function handleMouseMove(e) {
            if (!isMouseDown) return;
            currentMouseX = e.clientX;
            const diff = currentMouseX - startMouseX;
            const rotate = diff / 10;
            e.currentTarget.style.transform = `translateX(${diff}px) rotate(${rotate}deg)`;
        }

        function handleMouseUp(e) {
            if (!isMouseDown) return;
            isMouseDown = false;
            e.currentTarget.classList.remove('dragging');
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);

            const diff = currentMouseX - startMouseX;
            const threshold = 100;

            if (Math.abs(diff) > threshold) {
                if (diff > 0) {
                    saveFavoriteAndRemove();
                } else {
                    skipCard();
                }
            } else {
                e.currentTarget.style.transform = '';
            }
        }

        // Skip current card
        function skipCard() {
            if (!currentCard) return;
            // Animate off to left
            currentCard.style.transform = 'translateX(-150%) rotate(-20deg)';
            setTimeout(() => {
                deck.pop();
                renderNextCard();
                updateStats();
            }, 300);
        }

        // Save current to favorites and remove
        function saveFavoriteAndRemove() {
            if (!currentCard) return;

            const cardId = parseInt(currentCard.dataset.id);
            const quote = deck.find(q => q.id === cardId);

            if (quote && !favorites.find(f => f.id === cardId)) {
                favorites.push(quote);
                saveFavorites();
                renderFavorites();
            }

            // Animate off to right
            currentCard.style.transform = 'translateX(150%) rotate(20deg)';
            setTimeout(() => {
                deck.pop();
                renderNextCard();
                updateStats();
            }, 300);
        }

        // Button save
        function saveFavorite() {
            if (!currentCard) return;
            saveFavoriteAndRemove();
        }

        // Flip current card to see English
        function flipCurrentCard() {
            if (!currentCard) return;
            const inner = currentCard.querySelector('.card-inner');
            inner.classList.toggle('flipped');
        }

        // Toggle favorites drawer
        let favoritesOpen = false;
        function toggleFavorites() {
            const drawer = document.getElementById('favorites-drawer');
            const btn = document.getElementById('toggle-btn');
            favoritesOpen = !favoritesOpen;
            if (favoritesOpen) {
                drawer.classList.add('open');
                btn.textContent = '▲';
            } else {
                drawer.classList.remove('open');
                btn.textContent = '▼';
            }
        }

        // Remove from favorites
        function removeFavorite(id) {
            favorites = favorites.filter(f => f.id !== id);
            saveFavorites();
            renderFavorites();
            updateStats();
        }

        // Render favorites list
        function renderFavorites() {
            const list = document.getElementById('favorites-list');
            if (favorites.length === 0) {
                list.innerHTML = '<div class="empty-favorites">No favorites yet. Tap the heart button to save quotes you like.</div>';
                return;
            }

            list.innerHTML = favorites.map(f => `
                <div class="favorite-item">
                    <button class="remove-favorite" onclick="removeFavorite(${f.id})">×</button>
                    <div class="quote-text">${f.text}</div>
                    <div class="quote-source">${f.source}</div>
                </div>
            `).join('');
        }

        // Update statistics
        function updateStats() {
            document.getElementById('remaining-count').textContent = deck.length;
            document.getElementById('favorites-count').textContent = favorites.length;
            document.getElementById('drawer-count').textContent = favorites.length;
        }

        // Init
        document.addEventListener('DOMContentLoaded', () => {
            loadFavorites();
            initDeck();
        });
    </script>
</body>
</html>
"""

    with open('theoraclesays-mobile-swipe.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"成功生成手机滑动版HTML，包含{len(cards)}条语录")

if __name__ == '__main__':
    generate_html()
