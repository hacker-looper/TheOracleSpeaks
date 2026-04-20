# The Oracle Speaks - Warren Buffett's Quote Website

[English](README.md) | [中文](README_ZH.md)

A beautiful Warren Buffett quotes display website that converts EPUB content to JSON format and then generates the website, featuring curated investment/business/wealth/life wisdom quotes with bilingual Chinese-English support and interactive card flip effects.
![alt text](docs/image.png)
@see http://xooper.cn/web/theoraclespeaks/index.html

## Features

- 📚 **Curated Quotes** - Collection of Buffett's classic investment wisdom
- 🌐 **Bilingual Support** - Each quote includes Chinese translation and English original text
- 🎴 **Card Flip Effect** - Double-click cards to view English original text
- 🎨 **Beautiful Design** - Warm beige color scheme design system
- 🔍 **Search Function** - Search quotes by content
- 📄 **Pagination** - Display 20 quotes per page
- 📱 **Responsive Design** - Support for desktop and mobile devices

## Project Structure

```
TheOracleSpeaks/
├── README_ZH.md                    # Project documentation (Chinese)
├── README.md                       # Project documentation (English)
├── redbook_cards.json              # Quote data
├── redbook_cards.html              # Generated HTML file
├── redbook_cards_flip_warmbeige.html  # Warm beige flip effect HTML
├── redbook_cards_warmbeige.html    # Warm beige HTML
├── parse_quotes.py                 # EPUB quote parsing script
├── generate_html.py                # Main HTML generation script
├── generate_apple_design.py        # Apple style HTML generator
├── generate_html_flip.py           # Flip effect HTML generator
├── generate_html_flip_warmbeige.py # Warm beige flip effect HTML generator
├── generate_html_warmbeige.py      # Warm beige HTML generator
├── generate_html_mobile_swipe.py   # Mobile swipe effect HTML generator
├── start-server.ps1                # Local server startup script
├── theoraclesays.png               # Project icon/LOGO
├── docs/                           # Documentation directory
│   ├── The Oracle Speaks - David Andrews.epub  # Original EPUB book
│   └── image.png                   # Project screenshot
└── temp/                           # Temporary files directory
```

## Quick Start

### 1. Generate HTML File

```powershell / cmd
python generate_html_flip_warmbeige.py
```

### 2. Start Local Server

```powershell
# Start server using PowerShell
.\start-server.ps1
```

Server will start at `http://localhost:8000/`

### 3. Access Website

Open `http://localhost:8000/redbook_cards_flip_warmbeige.html` in your browser

## Usage Guide

### View English Original Text
- Double-click any quote card to flip and view English original text
- Double-click again to return to Chinese version

### Search Quotes
- Enter keywords in the search box at the top of the page
- Supports searching Chinese translations, English original text, and source information

### Pagination Navigation
- Use "Previous" and "Next" buttons at the bottom to browse
- 20 quotes displayed per page

## Data Format

Each quote contains the following fields:

```json
{
    "id": 1,
    "text": "Chinese translation content",
    "source": "——Source information",
    "original_text": "English original text",
    "original_source": "—English source"
}
```

## Data Processing Workflow

The project uses the `parse_quotes.py` script to extract and process quote data from the EPUB ebook. The main workflow is as follows:

### 1. Extract Quotes (extract_quotes)
- Reads XHTML files from the `temp/OEBPS/xhtml` directory (extracted from EPUB)
- Uses BeautifulSoup to parse HTML and find quote paragraph tags (`quote`, `quotec`, `quote-in`)
- Extracts quote text and corresponding source information
- Returns a list of original quotes

### 2. Translate Text (translate_text)
- Uses the `translators` library for translation
- Prioritizes Baidu translation API, automatically falls back to Google translation on failure
- Supports retry mechanism (default 3 attempts) with exponential backoff delay
- Preserves original text and logs errors if translation fails

### 3. Generate Card Data (generate_redbook_cards)
- Iterates through the extracted quote list
- Translates both the text and source of each quote to Chinese
- Constructs card data structure with bilingual support
- Adds delays to avoid API rate limiting

### 4. Save Data (save_cards)
- Saves processed card data in JSON format
- Output file: `redbook_cards.json`
- Uses UTF-8 encoding to ensure proper Chinese character handling

### 5. HTML Generation Scripts
- `generate_html.py` - Basic HTML generator
- `generate_apple_design.py` - Apple style design HTML generator
- `generate_html_flip.py` - Flip effect HTML generator
- `generate_html_flip_warmbeige.py` - Warm beige flip effect HTML generator
- `generate_html_warmbeige.py` - Warm beige HTML generator
- `generate_html_mobile_swipe.py` - Mobile swipe effect HTML generator

### Dependencies
- `BeautifulSoup` - HTML parsing
- `translators` - Multi-engine translation support
- `json` - Data serialization
- `time` - Delay control

## Design Specifications

The project uses a warm beige color scheme design system to create an elegant and comfortable reading experience:

- **Color Scheme**:
  - Page background: #f8f5f0 (warm beige)
  - Card front: #ffffff (pure white)
  - Card back: #f4f0ea (light beige)
  - Primary text: #5a4a3f (dark brown)
  - Secondary text: #8a7866 (medium brown)
  - Border decoration: #e6ddd0, #d4c8b8 (light brown)

- **Typography**: Georgia and Times New Roman serif fonts for a classic reading experience

- **Card Design**:
  - Rounded corners (12px)
  - Subtle shadow effects
  - Top gradient decorative bar
  - 3D flip animation effect

- **Interaction Feedback**:
  - Double-click card to flip and view English original text
  - Smooth 0.8s transition animation
  - Hover effects enhance visual feedback

## Tech Stack

- **HTML5** - Page structure
- **CSS3** - Styles and animation effects
- **JavaScript** - Interaction logic (flip, search, pagination)
- **Python** - HTML generation scripts
- **PowerShell** - Local server

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## License

This project content is sourced from "The Oracle Speaks - David Andrews" for learning and reference purposes only.

## Contributing

Issues and improvement suggestions are welcome!
