import html
import json
import re
from pathlib import Path


SOURCE_JSON = Path("redbook_cards.json")
OUTPUT_HTML = Path("redbook_cards_flip_warmbeige_redesign.html")


MANUAL_LEXICON = {
    "a", "able", "about", "additionally", "afghanistan", "all", "always", "american",
    "and", "annual", "anybody", "at", "basically", "berkshire", "book", "bought",
    "business", "buy", "call", "candies", "capital", "card", "cash", "cbs", "charge",
    "chronically", "citizens", "columbia", "company", "corporate", "daily", "deal",
    "described", "diligence", "due", "earnings", "early", "else", "essential", "essays",
    "exactly", "fielders", "financial", "florida", "forbes", "foundation", "friedman",
    "general", "get", "got", "greatest", "hathaway", "highest", "hitting", "i", "if",
    "in", "into", "investing", "investment", "is", "it", "its", "jewelry", "job",
    "just", "key", "leaking", "letter", "life", "look", "lottery", "many", "meeting",
    "mirror", "motors", "my", "news", "nobody", "not", "notre", "november", "of",
    "officials", "on", "or", "our", "ovarian", "owners", "participate", "people",
    "philosophy", "pitch", "priced", "problem", "productive", "public", "racing",
    "right", "science", "see", "selling", "sheet", "should", "state", "steel", "store",
    "taxes", "ted", "that", "the", "there", "think", "thinks", "this", "those", "to",
    "united", "university", "vessels", "wait", "want", "wanting", "wealth", "we",
    "well", "when", "williams", "with", "world", "you", "your"
}


def can_split_with_known_words(token: str, lexicon: set[str]) -> bool:
    if len(token) < 6:
        return False
    for first_end in range(1, len(token)):
        first = token[:first_end]
        second = token[first_end:]
        if first in lexicon and second in lexicon:
            return True
    for first_end in range(1, len(token) - 1):
        for second_end in range(first_end + 1, len(token)):
            first = token[:first_end]
            second = token[first_end:second_end]
            third = token[second_end:]
            if first in lexicon and second in lexicon and third in lexicon:
                return True
    return False


def build_lexicon(cards: list[dict]) -> set[str]:
    lexicon = set(MANUAL_LEXICON)
    token_pattern = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
    for card in cards:
        for field in ("original_text", "original_source"):
            for token in token_pattern.findall(card[field]):
                token = token.replace("’", "'")
                if token.lower() == token or token.istitle():
                    candidate = token.lower()
                    if can_split_with_known_words(candidate, lexicon):
                        continue
                    lexicon.add(candidate)
    return lexicon


def split_token_by_lexicon(token: str, lexicon: set[str]) -> str:
    if not token.isalpha() or len(token) < 4:
        return token

    lower = token.lower()
    if lower in lexicon and not any(char.isupper() for char in token[1:]):
        return token

    brute_force_segments: list[int] | None = None
    brute_force_score = -10**9

    for first_end in range(1, len(token)):
        first = lower[:first_end]
        second = lower[first_end:]
        if first in lexicon and second in lexicon:
            score = len(first) * len(first) + len(second) * len(second) - 1.5
            if score > brute_force_score:
                brute_force_score = score
                brute_force_segments = [len(first), len(second)]

    for first_end in range(1, len(token) - 1):
        for second_end in range(first_end + 1, len(token)):
            first = lower[:first_end]
            second = lower[first_end:second_end]
            third = lower[second_end:]
            if first in lexicon and second in lexicon and third in lexicon:
                score = (
                    len(first) * len(first)
                    + len(second) * len(second)
                    + len(third) * len(third)
                    - 3.0
                )
                if score > brute_force_score:
                    brute_force_score = score
                    brute_force_segments = [len(first), len(second), len(third)]

    if brute_force_segments:
        segments = []
        offset = 0
        for piece_len in brute_force_segments:
            segments.append(token[offset:offset + piece_len])
            offset += piece_len
        return " ".join(segments)

    max_word_len = min(20, len(token))
    best: list[tuple[float, list[int]]] = [(-10**9, []) for _ in range(len(token) + 1)]
    best[0] = (0.0, [])

    for start in range(len(token)):
        score, lengths = best[start]
        if score <= -10**8:
            continue
        for end in range(start + 1, min(len(token), start + max_word_len) + 1):
            piece = lower[start:end]
            piece_len = end - start
            if piece in lexicon:
                piece_score = piece_len * piece_len
                if piece_len == 1 and piece not in {"a", "i"}:
                    piece_score -= 6
                candidate = score + piece_score - 1.15
            else:
                if piece_len < 4:
                    continue
                candidate = score - (piece_len * 2.6)
            if candidate > best[end][0]:
                best[end] = (candidate, lengths + [piece_len])

    final_score, segment_lengths = best[len(token)]
    if len(segment_lengths) < 2 or final_score < len(token) * 1.2:
        return token

    segments = []
    offset = 0
    for piece_len in segment_lengths:
        segments.append(token[offset:offset + piece_len])
        offset += piece_len

    return " ".join(segments)


def fix_english_spacing(text: str, lexicon: set[str]) -> str:
    token_pattern = re.compile(r"[A-Za-z]+")

    def replacer(match: re.Match[str]) -> str:
        return split_token_by_lexicon(match.group(0), lexicon)

    normalized = token_pattern.sub(replacer, text)
    normalized = re.sub(r"(?<=[,;:!?])(?=\S)", " ", normalized)
    normalized = re.sub(r"(?<=\w)—(?=\w)", " — ", normalized)
    normalized = re.sub(r"(?<=,)(?=[A-Za-z])", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def build_card(card: dict, lexicon: set[str]) -> str:
    original_text_fixed = fix_english_spacing(card["original_text"], lexicon)
    original_text = html.escape(original_text_fixed)
    original_source = html.escape(card["original_source"])
    payload = html.escape(
        json.dumps(
            {
                "id": card["id"],
                "original_text": original_text_fixed,
                "original_source": card["original_source"],
            },
            ensure_ascii=False,
        ),
        quote=True,
    )
    return f"""
        <article class="quote-card" data-card='{payload}'>
            <div class="quote-card__inner">
                <section class="quote-face quote-face--front quote-face--single">
                    <div class="quote-face__topline">
                        <span class="quote-index">No. {card["id"]:03d}</span>
                        <span class="quote-badge">English</span>
                    </div>
                    <div class="quote-mark" aria-hidden="true">?</div>
                    <p class="quote-text">{original_text}</p>
                    <footer class="quote-source">{original_source}</footer>
                </section>
            </div>
        </article>
    """


def build_html(cards: list[dict]) -> str:
    lexicon = build_lexicon(cards)
    cards_markup = "".join(build_card(card, lexicon) for card in cards)
    total_cards = len(cards)
    epub_href = html.escape("docs/The Oracle Speaks - David Andrews.epub", quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Oracle Speaks - Collector's Edition</title>
    <meta name="description" content="A redesigned collectible-style archive of Warren Buffett quotes with bilingual flip cards, search, filters, and pagination.">
    <meta name="keywords" content="Warren Buffett, quotes, investing, editorial cards, flip cards, Oracle of Omaha">
    <meta name="author" content="The Oracle Speaks">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="The Oracle Speaks - Collector's Edition">
    <meta property="og:description" content="Editorial quote archive with tactile flip cards and warm-beige collectible styling.">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="The Oracle Speaks - Collector's Edition">
    <meta name="twitter:description" content="Browse Warren Buffett quotes in a redesigned editorial flip-card experience.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #f4ede2;
            --bg-soft: #fbf6ee;
            --paper: rgba(255, 251, 245, 0.86);
            --paper-strong: rgba(255, 250, 243, 0.96);
            --ink: #2f241b;
            --ink-soft: #625346;
            --line: rgba(113, 90, 66, 0.18);
            --line-strong: rgba(113, 90, 66, 0.34);
            --accent: #916c4c;
            --accent-deep: #5f4127;
            --accent-soft: #d9c0a1;
            --shadow: 0 20px 50px rgba(73, 51, 31, 0.12);
            --shadow-soft: 0 10px 24px rgba(73, 51, 31, 0.08);
            --radius-xl: 28px;
            --radius-lg: 22px;
            --radius-md: 16px;
            --max-width: 1440px;
        }}

        * {{
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            margin: 0;
            min-height: 100vh;
            color: var(--ink);
            font-family: "Manrope", sans-serif;
            background:
                radial-gradient(circle at top left, rgba(255, 255, 255, 0.72), transparent 28%),
                radial-gradient(circle at 85% 15%, rgba(210, 177, 144, 0.24), transparent 22%),
                linear-gradient(180deg, #efe6d9 0%, #f6efe5 28%, #f4ede2 100%);
            position: relative;
            overflow-x: hidden;
        }}

        body::before,
        body::after {{
            content: "";
            position: fixed;
            inset: auto;
            pointer-events: none;
            z-index: -1;
            filter: blur(10px);
        }}

        body::before {{
            width: 24rem;
            height: 24rem;
            top: -7rem;
            right: -4rem;
            background: radial-gradient(circle, rgba(168, 130, 93, 0.18), transparent 70%);
        }}

        body::after {{
            width: 30rem;
            height: 30rem;
            bottom: -12rem;
            left: -6rem;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.4), transparent 62%);
        }}

        a {{
            color: inherit;
        }}

        button,
        input {{
            font: inherit;
        }}

        .page-shell {{
            width: min(calc(100% - 32px), var(--max-width));
            margin: 0 auto;
            padding: 24px 0 72px;
        }}

        .hero {{
            position: relative;
            overflow: hidden;
            padding: 28px;
            border: 1px solid var(--line);
            border-radius: 32px;
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.82), rgba(250, 242, 231, 0.86)),
                repeating-linear-gradient(
                    90deg,
                    rgba(120, 92, 67, 0.018) 0,
                    rgba(120, 92, 67, 0.018) 1px,
                    transparent 1px,
                    transparent 10px
                );
            box-shadow: var(--shadow);
        }}

        .hero::before {{
            content: "";
            position: absolute;
            inset: 18px;
            border: 1px solid rgba(145, 108, 76, 0.12);
            border-radius: 24px;
            pointer-events: none;
        }}

        .hero-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1.45fr) minmax(280px, 0.85fr);
            gap: 28px;
            align-items: stretch;
        }}

        .eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 18px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.24em;
            text-transform: uppercase;
            color: var(--accent-deep);
        }}

        .eyebrow::before {{
            content: "";
            width: 38px;
            height: 1px;
            background: currentColor;
        }}

        .hero h1 {{
            margin: 0;
            max-width: 10ch;
            font-family: "Newsreader", serif;
            font-size: clamp(3.4rem, 8vw, 7rem);
            line-height: 0.92;
            letter-spacing: -0.055em;
            font-weight: 600;
        }}

        .hero-copy {{
            margin: 20px 0 0;
            max-width: 60ch;
            font-size: clamp(1rem, 1vw + 0.85rem, 1.15rem);
            line-height: 1.8;
            color: var(--ink-soft);
        }}

        .hero-actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 26px;
        }}

        .hero-link {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 48px;
            padding: 0 18px;
            border-radius: 999px;
            border: 1px solid var(--line-strong);
            background: rgba(255, 251, 246, 0.84);
            color: var(--ink);
            text-decoration: none;
            transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
        }}

        .hero-link--primary {{
            background: var(--accent-deep);
            color: #fff9f0;
            border-color: transparent;
        }}

        .hero-link--download {{
            gap: 10px;
        }}

        .hero-link--download svg {{
            width: 16px;
            height: 16px;
            flex: 0 0 auto;
        }}

        .hero-link:hover,
        .hero-link:focus-visible {{
            transform: translateY(-2px);
        }}

        .hero-link:focus-visible,
        .tag:focus-visible,
        .quote-card:focus-visible,
        .page-btn:focus-visible,
        .search-input:focus-visible {{
            outline: none;
            box-shadow: 0 0 0 3px rgba(145, 108, 76, 0.18), 0 0 0 1px rgba(95, 65, 39, 0.6);
        }}

        .hero-panel {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 18px;
        }}

        .portrait-card,
        .stats-card {{
            padding: 18px;
            border-radius: 24px;
            border: 1px solid var(--line);
            background: var(--paper);
            box-shadow: var(--shadow-soft);
            backdrop-filter: blur(10px);
        }}

        .portrait-card {{
            display: grid;
            grid-template-columns: 96px minmax(0, 1fr);
            gap: 16px;
            align-items: center;
        }}

        .portrait-frame {{
            aspect-ratio: 1;
            border-radius: 22px;
            overflow: hidden;
            background: linear-gradient(135deg, rgba(145, 108, 76, 0.2), rgba(255, 255, 255, 0.72));
            border: 1px solid rgba(145, 108, 76, 0.14);
        }}

        .portrait-frame img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .portrait-meta h2,
        .portrait-meta p {{
            margin: 0;
        }}

        .portrait-meta h2 {{
            font-family: "Newsreader", serif;
            font-size: 2rem;
            font-weight: 500;
            letter-spacing: -0.03em;
        }}

        .portrait-meta p {{
            margin-top: 6px;
            line-height: 1.7;
            color: var(--ink-soft);
        }}

        .stats-card {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
        }}

        .stat {{
            padding: 14px;
            border-radius: 18px;
            background: rgba(255, 252, 247, 0.82);
            border: 1px solid rgba(145, 108, 76, 0.12);
        }}

        .stat strong {{
            display: block;
            font-family: "Newsreader", serif;
            font-size: clamp(1.8rem, 4vw, 2.5rem);
            line-height: 1;
            font-weight: 600;
        }}

        .stat span {{
            display: block;
            margin-top: 8px;
            color: var(--ink-soft);
            font-size: 0.92rem;
            line-height: 1.5;
        }}

        .toolbar {{
            position: sticky;
            top: 14px;
            z-index: 20;
            margin-top: 26px;
            padding: 16px;
            border-radius: 24px;
            border: 1px solid var(--line);
            background: rgba(251, 246, 238, 0.78);
            box-shadow: var(--shadow-soft);
            backdrop-filter: blur(18px);
        }}

        .toolbar-grid {{
            display: grid;
            grid-template-columns: minmax(260px, 1.3fr) minmax(0, 1fr) auto;
            gap: 14px;
            align-items: center;
        }}

        .search-wrap {{
            position: relative;
        }}

        .search-wrap svg {{
            position: absolute;
            top: 50%;
            left: 18px;
            width: 18px;
            height: 18px;
            transform: translateY(-50%);
            color: rgba(95, 65, 39, 0.68);
            pointer-events: none;
        }}

        .search-input {{
            width: 100%;
            min-height: 54px;
            padding: 0 18px 0 48px;
            border-radius: 999px;
            border: 1px solid rgba(113, 90, 66, 0.18);
            background: rgba(255, 252, 247, 0.96);
            color: var(--ink);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
        }}

        .search-input::placeholder {{
            color: rgba(98, 83, 70, 0.78);
        }}

        .tag-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .tag {{
            min-height: 42px;
            padding: 0 16px;
            border-radius: 999px;
            border: 1px solid rgba(113, 90, 66, 0.14);
            background: rgba(255, 251, 246, 0.7);
            color: var(--ink-soft);
            cursor: pointer;
            transition: transform 180ms ease, border-color 180ms ease, background 180ms ease, color 180ms ease;
        }}

        .tag:hover,
        .tag.active {{
            color: #fff9f0;
            border-color: transparent;
            background: linear-gradient(135deg, #7a5638, #9b7657);
            transform: translateY(-1px);
        }}

        .results-meta {{
            text-align: right;
            color: var(--ink-soft);
            line-height: 1.6;
            font-size: 0.95rem;
            white-space: nowrap;
        }}

        .results-meta strong {{
            display: block;
            color: var(--ink);
            font-size: 1rem;
        }}

        .section-head {{
            display: flex;
            justify-content: space-between;
            align-items: end;
            gap: 20px;
            margin: 32px 0 18px;
        }}

        .section-head h3,
        .section-head p {{
            margin: 0;
        }}

        .section-head h3 {{
            font-family: "Newsreader", serif;
            font-size: clamp(1.9rem, 3vw, 2.5rem);
            letter-spacing: -0.04em;
            font-weight: 500;
        }}

        .section-head p {{
            max-width: 52ch;
            color: var(--ink-soft);
            line-height: 1.7;
        }}

        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 20px;
            perspective: 1600px;
        }}

        .quote-card {{
            position: relative;
            height: 520px;
            border: 0;
            padding: 0;
            background: transparent;
            cursor: pointer;
            perspective: 1600px;
            text-align: left;
        }}

        .quote-card__inner {{
            position: relative;
            height: 100%;
            height: 100%;
            transition:
                filter 250ms ease,
                transform 460ms cubic-bezier(0.22, 0.7, 0.2, 1);
            border-radius: var(--radius-xl);
            transform-origin: center center;
        }}

        .quote-card:hover .quote-card__inner {{
            filter: drop-shadow(0 26px 40px rgba(68, 47, 29, 0.1));
        }}


        .quote-face {{
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            height: 100%;
            padding: 22px;
            border-radius: var(--radius-xl);
            border: 1px solid rgba(113, 90, 66, 0.16);
            overflow: hidden;
            transition:
                opacity 320ms ease,
                transform 460ms cubic-bezier(0.22, 0.7, 0.2, 1),
                visibility 320ms ease,
                clip-path 460ms cubic-bezier(0.22, 0.7, 0.2, 1);
            will-change: opacity, transform, clip-path;
        }}

        .quote-face::after {{
            content: "";
            position: absolute;
            inset: -10%;
            background: linear-gradient(
                105deg,
                transparent 20%,
                rgba(255, 255, 255, 0.18) 40%,
                rgba(255, 255, 255, 0.52) 50%,
                rgba(255, 255, 255, 0.12) 60%,
                transparent 78%
            );
            opacity: 0;
            transform: translateX(-120%) skewX(-12deg);
            pointer-events: none;
        }}

        .quote-face::before {{
            content: "";
            position: absolute;
            inset: 10px;
            border-radius: calc(var(--radius-xl) - 10px);
            border: 1px solid rgba(113, 90, 66, 0.08);
            pointer-events: none;
        }}

        .quote-face--front {
            background:
                radial-gradient(circle at top right, rgba(217, 192, 161, 0.2), transparent 32%),
                linear-gradient(180deg, rgba(255, 253, 249, 0.96), rgba(249, 242, 232, 0.92));
            box-shadow: var(--shadow-soft);
            opacity: 1;
            visibility: visible;
            transform: none;
            clip-path: inset(0 0 0 0 round 28px);
        }

        .quote-face--single {
            clip-path: inset(0 0 0 0 round 28px);
        }}


        .quote-face__topline {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
            position: relative;
            z-index: 1;
        }}

        .quote-index,
        .quote-badge {{
            display: inline-flex;
            align-items: center;
            min-height: 28px;
            padding: 0 10px;
            border-radius: 999px;
            border: 1px solid rgba(113, 90, 66, 0.14);
            font-size: 0.72rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }}

        .quote-index {{
            color: var(--accent-deep);
            background: rgba(255, 252, 247, 0.7);
        }}

        .quote-badge {{
            color: var(--ink-soft);
            background: rgba(255, 250, 244, 0.55);
        }}

        .quote-mark {{
            font-family: "Newsreader", serif;
            font-size: 5rem;
            line-height: 0.8;
            color: rgba(145, 108, 76, 0.18);
            margin-bottom: 10px;
        }}

        .quote-text {{
            position: relative;
            z-index: 1;
            margin: 0;
            font-family: "Newsreader", serif;
            font-size: 1.38rem;
            line-height: 1.6;
            letter-spacing: -0.01em;
            color: var(--ink);
            flex: 1;
            min-height: 0;
            overflow-y: auto;
            padding-right: 8px;
            scrollbar-width: thin;
            scrollbar-color: rgba(145, 108, 76, 0.45) transparent;
        }}


        .quote-text::-webkit-scrollbar {{
            width: 6px;
        }}

        .quote-text::-webkit-scrollbar-track {{
            background: transparent;
        }}

        .quote-text::-webkit-scrollbar-thumb {{
            background: rgba(145, 108, 76, 0.35);
            border-radius: 999px;
        }}

        .quote-text::-webkit-scrollbar-thumb:hover {{
            background: rgba(145, 108, 76, 0.55);
        }}

        .quote-source {{
            position: relative;
            z-index: 1;
            margin-top: 18px;
            padding-top: 14px;
            border-top: 1px solid rgba(113, 90, 66, 0.12);
            color: var(--ink-soft);
            line-height: 1.7;
            font-size: 0.92rem;
        }}

        .search-highlight {{
            padding: 0 0.2em;
            border-radius: 0.2em;
            color: var(--accent-deep);
            background: linear-gradient(180deg, rgba(230, 205, 165, 0), rgba(230, 205, 165, 0.9));
        }}

        .empty-state {{
            display: none;
            padding: 60px 24px;
            border: 1px dashed rgba(113, 90, 66, 0.25);
            border-radius: 28px;
            background: rgba(255, 251, 246, 0.56);
            text-align: center;
            color: var(--ink-soft);
        }}

        .empty-state h4,
        .empty-state p {{
            margin: 0;
        }}

        .empty-state h4 {{
            font-family: "Newsreader", serif;
            font-size: 2rem;
            font-weight: 500;
            color: var(--ink);
        }}

        .empty-state p {{
            margin-top: 12px;
            line-height: 1.8;
        }}

        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 28px;
        }}

        .page-btn {{
            min-width: 42px;
            height: 42px;
            padding: 0 14px;
            border: 1px solid rgba(113, 90, 66, 0.16);
            border-radius: 999px;
            background: rgba(255, 252, 247, 0.82);
            color: var(--ink);
            cursor: pointer;
            transition: transform 180ms ease, background 180ms ease, border-color 180ms ease, color 180ms ease;
        }}

        .page-btn:hover:not([disabled]),
        .page-btn.active {{
            background: var(--accent-deep);
            color: #fff9f0;
            border-color: transparent;
            transform: translateY(-1px);
        }}

        .page-btn[disabled] {{
            cursor: not-allowed;
            opacity: 0.45;
        }}

        .page-info {{
            color: var(--ink-soft);
            line-height: 1.6;
            margin-left: 6px;
        }}

        .page-dots {{
            color: var(--ink-soft);
            padding: 0 2px;
        }}

        .footer-note {{
            margin-top: 26px;
            color: var(--ink-soft);
            text-align: center;
            line-height: 1.7;
            font-size: 0.94rem;
        }}

        @media (max-width: 1180px) {{
            .hero-grid {{
                grid-template-columns: 1fr;
            }}

            .toolbar-grid {{
                grid-template-columns: 1fr;
            }}

            .results-meta {{
                text-align: left;
                white-space: normal;
            }}

            .cards-grid {{
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }}
        }}

        @media (max-width: 900px) {{
            .page-shell {{
                width: min(calc(100% - 24px), var(--max-width));
                padding-top: 14px;
            }}

            .hero,
            .toolbar {{
                border-radius: 24px;
            }}

            .stats-card {{
                grid-template-columns: 1fr;
            }}

            .cards-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
        }}

        @media (max-width: 640px) {{
            .hero {{
                padding: 20px;
            }}

            .portrait-card {{
                grid-template-columns: 1fr;
            }}

            .portrait-frame {{
                max-width: 124px;
            }}

            .section-head {{
                align-items: start;
                flex-direction: column;
            }}

            .cards-grid {{
                grid-template-columns: 1fr;
                gap: 16px;
            }}

            .quote-card {{
                height: 440px;
            }}

            .quote-text {{
                font-size: 1.24rem;
            }}

        }}

        @media (prefers-reduced-motion: reduce) {{
            html {{
                scroll-behavior: auto;
            }}

            *,
            *::before,
            *::after {{
                animation: none !important;
                transition: none !important;
            }}


            .quote-card__inner {{
                transition: none !important;
                transform: none !important;
            }}

            .quote-face::after {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <main class="page-shell">
        <section class="hero">
            <div class="hero-grid">
                <div>
                    <span class="eyebrow">Collector's Edition</span>
                    <h1>The Oracle Speaks</h1>
                    <p class="hero-copy">
                        A warmer, more editorial reading surface for Warren Buffett's quotes.
                        Each card now focuses on the original English text, and the overall page feels
                        more like a curated archive than a raw grid.
                    </p>
                    <div class="hero-actions">
                        <a class="hero-link hero-link--primary" href="#quote-archive">Enter the archive</a>
                        <a class="hero-link hero-link--download" href="{epub_href}" download>
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                                <path d="M12 3V15"></path>
                                <path d="M7 10L12 15L17 10"></path>
                                <path d="M5 19H19"></path>
                            </svg>
                            Download EPUB
                        </a>
                        <a class="hero-link" href="#filter-bar">Search and filter</a>
                    </div>
                </div>
                <div class="hero-panel">
                    <article class="portrait-card">
                        <div class="portrait-frame">
                            <img src="theoraclesays.png" alt="Portrait of Warren Buffett">
                        </div>
                        <div class="portrait-meta">
                            <h2>Warren Buffett</h2>
                            <p>
                                A tactile quote library centered on Buffett's original English text.
                                Designed for browsing, collecting, and slow reading.
                            </p>
                        </div>
                    </article>
                    <section class="stats-card" aria-label="Archive stats">
                        <div class="stat">
                            <strong>{total_cards}</strong>
                            <span>Total quote cards in this archive.</span>
                        </div>
                        <div class="stat">
                            <strong>4</strong>
                            <span>Themes to skim quickly through the collection.</span>
                        </div>
                        <div class="stat">
                            <strong>12</strong>
                            <span>Cards per page for a calmer, gallery-like reading pace.</span>
                        </div>
                    </section>
                </div>
            </div>
        </section>

        <section class="toolbar" id="filter-bar">
            <div class="toolbar-grid">
                <label class="search-wrap" aria-label="Search quotes">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                        <circle cx="11" cy="11" r="7"></circle>
                        <path d="M20 20L16.65 16.65"></path>
                    </svg>
                    <input class="search-input" id="search-input" type="text" placeholder="Search Chinese, English, or source...">
                </label>
                <div class="tag-list" role="tablist" aria-label="Quote filters">
                    <button class="tag active" type="button" data-filter="all">All</button>
                    <button class="tag" type="button" data-filter="investing">Investing</button>
                    <button class="tag" type="button" data-filter="business">Business</button>
                    <button class="tag" type="button" data-filter="wealth">Wealth</button>
                    <button class="tag" type="button" data-filter="life">Life</button>
                </div>
                <div class="results-meta">
                    <strong id="result-count">{total_cards} cards</strong>
                    <span id="result-summary">Showing the full archive.</span>
                </div>
            </div>
        </section>

        <section class="section-head" id="quote-archive">
            <div>
                <h3>Archive Cabinet</h3>
                <p>
                    The new layout adds stronger spacing, clearer hierarchy, and a more premium paper-card feel
                    while keeping the reading experience focused and uncluttered.
                </p>
            </div>
        </section>

        <section class="cards-grid" id="cards-grid">
{cards_markup}
        </section>

        <section class="empty-state" id="empty-state">
            <h4>No matching cards</h4>
            <p>Try another keyword or switch back to a broader theme filter.</p>
        </section>

        <nav class="pagination" id="pagination" aria-label="Pagination"></nav>

        <p class="footer-note">
            Redesign file generated from the same quote data source. Original source file is preserved unchanged.
        </p>
    </main>

    <script>
        const CARDS_PER_PAGE = 12;
        const allCards = Array.from(document.querySelectorAll('.quote-card'));
        const cardsGrid = document.getElementById('cards-grid');
        const emptyState = document.getElementById('empty-state');
        const pagination = document.getElementById('pagination');
        const searchInput = document.getElementById('search-input');
        const tags = Array.from(document.querySelectorAll('.tag'));
        const resultCount = document.getElementById('result-count');
        const resultSummary = document.getElementById('result-summary');

        let activeFilter = 'all';
        let currentPage = 1;
        let filteredCards = [...allCards];

        const filterGroups = {{
            investing: ['invest', 'stock', 'market', 'capital', 'price', 'pitch', 'deal', 'share', 'portfolio', 'moat', 'valuation', 'investment'],
            business: ['business', 'company', 'manager', 'management', 'owner', 'industry', 'brand', 'competition', 'enterprise'],
            wealth: ['wealth', 'money', 'rich', 'fortune', 'capital', 'profit', 'return', 'cash', 'dollar'],
            life: ['life', 'people', 'character', 'habit', 'temperament', 'success', 'happiness', 'mistake', 'reputation', 'human']
        }};

        function escapeRegExp(text) {{
            return text.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
        }}

        function normalizeText(text) {{
            return (text || '').toLowerCase();
        }}

        function getCardPayload(card) {{
            return JSON.parse(card.dataset.card);
        }}

        function setOriginalContent(card) {{
            const payload = getCardPayload(card);
            card.querySelector('.quote-text').innerHTML = payload.original_text;
            card.querySelector('.quote-face--front .quote-source').innerHTML = payload.original_source;
        }}

        function clearHighlights(card) {{
            setOriginalContent(card);
        }}

        function highlightText(content, keyword) {{
            if (!keyword) return content;
            const safe = escapeRegExp(keyword);
            return content.replace(new RegExp(`(${{safe}})`, 'gi'), '<span class="search-highlight">$1</span>');
        }}

        function applyHighlights(card, keyword) {{
            const payload = getCardPayload(card);
            card.querySelector('.quote-text').innerHTML = highlightText(payload.original_text, keyword);
            card.querySelector('.quote-face--front .quote-source').innerHTML = highlightText(payload.original_source, keyword);
        }}

        function matchesTheme(card, theme) {{
            if (theme === 'all') return true;
            const payload = getCardPayload(card);
            const haystack = normalizeText([
                payload.original_text,
                payload.original_source
            ].join(' '));
            return filterGroups[theme].some(keyword => haystack.includes(keyword));
        }}

        function matchesSearch(card, query) {{
            if (!query) return true;
            const payload = getCardPayload(card);
            const haystack = normalizeText([
                payload.original_text,
                payload.original_source
            ].join(' '));
            return haystack.includes(query);
        }}

        function getPageItems() {{
            const start = (currentPage - 1) * CARDS_PER_PAGE;
            return filteredCards.slice(start, start + CARDS_PER_PAGE);
        }}

        function renderCards() {{
            allCards.forEach(card => {{
                card.hidden = true;
            }});
            const pageItems = getPageItems();
            pageItems.forEach(card => {{
                card.hidden = false;
            }});
            cardsGrid.style.display = filteredCards.length ? 'grid' : 'none';
            emptyState.style.display = filteredCards.length ? 'none' : 'block';
        }}

        function renderPagination() {{
            const totalPages = Math.ceil(filteredCards.length / CARDS_PER_PAGE);
            if (totalPages <= 1) {{
                pagination.innerHTML = '';
                return;
            }}

            let html = `<button class="page-btn" data-page="prev" ${{currentPage === 1 ? 'disabled' : ''}}>Prev</button>`;
            for (let page = 1; page <= totalPages; page++) {{
                if (
                    page === 1 ||
                    page === totalPages ||
                    (page >= currentPage - 1 && page <= currentPage + 1)
                ) {{
                    html += `<button class="page-btn ${{page === currentPage ? 'active' : ''}}" data-page="${{page}}">${{page}}</button>`;
                }} else if (page === currentPage - 2 || page === currentPage + 2) {{
                    html += `<span class="page-dots">...</span>`;
                }}
            }}
            html += `<button class="page-btn" data-page="next" ${{currentPage === totalPages ? 'disabled' : ''}}>Next</button>`;
            html += `<span class="page-info">Page ${{currentPage}} of ${{totalPages}}</span>`;
            pagination.innerHTML = html;

            Array.from(pagination.querySelectorAll('.page-btn')).forEach(button => {{
                button.addEventListener('click', () => {{
                    const target = button.dataset.page;
                    if (target === 'prev' && currentPage > 1) currentPage -= 1;
                    else if (target === 'next' && currentPage < totalPages) currentPage += 1;
                    else if (!isNaN(Number(target))) currentPage = Number(target);
                    renderCards();
                    renderPagination();
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }});
            }});
        }}

        function renderSummary(searchQuery) {{
            resultCount.textContent = `${{filteredCards.length}} cards`;
            const filterLabel = activeFilter === 'all' ? 'all themes' : activeFilter;
            resultSummary.textContent = searchQuery
                ? `Filtered by "${{searchQuery}}" in ${{filterLabel}}.`
                : `Showing ${{filterLabel}}.`;
        }}

        function applyFilters() {{
            const searchQuery = normalizeText(searchInput.value.trim());

            allCards.forEach(card => {{
                clearHighlights(card);
            }});

            filteredCards = allCards.filter(card => matchesTheme(card, activeFilter) && matchesSearch(card, searchQuery));
            if (searchQuery) {{
                filteredCards.forEach(card => applyHighlights(card, searchQuery));
            }}

            currentPage = 1;
            renderCards();
            renderPagination();
            renderSummary(searchInput.value.trim());
        }}

        tags.forEach(tag => {{
            tag.addEventListener('click', () => {{
                tags.forEach(item => item.classList.remove('active'));
                tag.classList.add('active');
                activeFilter = tag.dataset.filter;
                applyFilters();
            }});
        }});

        searchInput.addEventListener('input', applyFilters);

        renderCards();
        renderPagination();
        renderSummary('');
    </script>
</body>
</html>
"""


def main() -> None:
    cards = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    OUTPUT_HTML.write_text(build_html(cards), encoding="utf-8")
    print(f"Generated {OUTPUT_HTML} with {len(cards)} cards.")


if __name__ == "__main__":
    main()
