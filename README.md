# SBI Branch Modernization @ IISc Campus

A standalone case-study page for **SBI Branch Modernization @ IISc**, a UX
research & service-design project that reimagines the SBI IISc branch as a
smart, efficient, walk-in experience (smart queue, assisted kiosks, app
dashboard, and a real-time status wall).

Single-file static site — vanilla HTML, CSS, JS (same approach as AI Idea Hub
and Civic Simbaa). A sticky top nav lists every chapter; each chapter is a board
section sliced straight from the source PDF. Theme matches the PDF: pale
lavender → blue gradient, Poppins display type, deep-indigo + SBI-cyan accents.

## Run locally

```bash
cd "SBI 2040"
python3 -m http.server 5230
# open http://localhost:5230
```

## Structure

```
SBI 2040/
├── index.html                      single-file case study + top nav
├── public/board/                   one image per chapter (sliced from the PDF)
│   ├── 01-overview.jpg … 11-roadmap.jpg
│   ├── 01-overview.webp … 11-roadmap.webp
│   ├── full.jpg                    full-board reference export
│   └── manifest.json
├── scripts/analyze_bands.py        find clean horizontal cut points
├── scripts/render_board.py         board → per-chapter section images
├── scripts/make_webp.py            JPG chapter images → WebP
├── Wipro Design Task SBI Bank.pdf  source board export (1 tall page)
└── README.md
```

## Chapters

Overview · Research · Insights · Prioritize · Field Study · Interviews ·
Personas · Solutions · Experience · After · Roadmap.

The source PDF is a single tall page (1920 × 22102 pt). Section boundaries are
expressed in board y-units and chosen to fall in the pale gaps between sections
so no heading is clipped (see `BANDS` in `scripts/render_board.py`).

## Re-rendering the chapter images

```bash
python3 scripts/analyze_bands.py            # inspect gaps/blocks (optional)
python3 scripts/render_board.py --width 2000
python3 scripts/make_webp.py
```

(Requires `PyMuPDF`, `Pillow`, `numpy`: `pip3 install --user PyMuPDF Pillow numpy`.)

## Notes

- **Theme:** pale lavender → blue gradient, deep indigo `#2c2480`, SBI cyan
  `#0aa0e0`, violet `#6b5cf0` — taken from the project's own visual language.
- **Typography:** Poppins (display) + Inter (body).
- **Nav:** compact numbered pills with in-place hover preview and mobile
  tap-centering; scroll-spy highlights the active chapter.
- Click any chapter image to open it full-size in a lightbox (Esc to close).
- The 144 MB source PDF renders to ~6 MB of chapter images (WebP), so the page
  stays lightweight for the portfolio.
