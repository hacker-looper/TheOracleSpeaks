# The Oracle Speaks

[English](README.md) | [中文](README-ZH.md)

A curated Warren Buffett quote website built from structured quote data, with editorial warm-beige styling, category filters, search, and paginated reading.

![Project screenshot](docs/image.png)

## Current Experience

- Warren Buffett quote cards
- Warm editorial card layout
- Category badges: `Investing`, `Business`, `Wealth`, `Life`
- Search by quote text or source
- Category filtering
- Pagination with 12 cards per page
- Amazon purchase link for the book
- Responsive layout for desktop and mobile

## Main Files

```text
TheOracleSpeaks/
├── README.md
├── redbook_cards.json
├── redbook_cards.html
├── redbook_cards_warmbeige.html
├── redbook_cards_flip_warmbeige.html
├── redbook_cards_flip_warmbeige_redesign.html
├── generate_html.py
├── generate_html_warmbeige.py
├── generate_html_flip.py
├── generate_html_flip_warmbeige.py
├── generate_html_flip_warmbeige_redesign.py
├── generate_html_mobile_swipe.py
├── generate_apple_design.py
├── parse_quotes.py
├── start-server.ps1
├── theoraclesays.png
├── docs/
│   └── image.png
└── temp/
```

## Recommended Entry Page

Open:

```text
redbook_cards_flip_warmbeige_redesign.html
```

This is the most up-to-date redesigned reading surface in the repository.

## Quick Start

### 1. Open the redesigned page directly

```powershell
start .\redbook_cards_flip_warmbeige_redesign.html
```

### 2. Or run a local server

```powershell
.\start-server.ps1
```

Then visit:

```text
http://localhost:8000/redbook_cards_flip_warmbeige_redesign.html
```

## Data Format

Each quote in `redbook_cards.json` contains:

```json
{
  "id": 1,
  "text": "Chinese translation",
  "source": "Chinese source",
  "original_text": "English quote",
  "original_source": "English source"
}
```

## Workflow

### 1. Parse quote content

`parse_quotes.py` extracts quote/source pairs from EPUB-derived XHTML content in `temp/`.

### 2. Build structured data

Processed quote data is saved to:

```text
redbook_cards.json
```

### 3. Generate HTML variants

Available generators include:

- `generate_html.py`
- `generate_html_warmbeige.py`
- `generate_html_flip.py`
- `generate_html_flip_warmbeige.py`
- `generate_html_flip_warmbeige_redesign.py`
- `generate_html_mobile_swipe.py`
- `generate_apple_design.py`

## Notes

- The redesigned page currently focuses on English quote display.
- The local EPUB source file is no longer kept in the repository.
- The hero CTA links users to Amazon instead of downloading a local ebook file.

## Tech Stack

- HTML5
- CSS3
- JavaScript
- Python
- PowerShell

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
