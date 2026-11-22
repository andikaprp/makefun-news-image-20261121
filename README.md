[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/andikaprp/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/andikaprp/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# One Day on Earth — Saturday 21 November 2026

Entry for the make.fun competition **news-image-20261121**: sum up one
day's world news in a single image.

## What is in the image

A single-page cream broadsheet of Saturday 21 November 2026. The page
presents **34 stories**: **15 headlined cards**, each with its own drawn
art panel (banner label and source tag on every panel), plus a numbered
**briefs band** of 19 further one-line stories, place-led and interleaved
across regions so no single country's local news clusters at the tail.

Alongside the cards sit an **abstract-blob map panel** — continent blobs
with 15 numbered dots marking where the headlined stories happened — and
a **DATE CHECK box** of verified Friday items (the Wall Street rout and
Anthropic's second down day among them, with their figures) that are
shown as Friday news, not passed off as Saturday's.

Every story on the page happened, or was first reported, on 21 November
2026 in some time zone. Every figure was checked against its primary
source before printing.

## How it runs

- `main.py` — the entrypoint. Standard library only. It copies the
  shipped `entry.png` into the output directory (`MAKEFUN_OUTPUT_DIR`,
  default `/output`). The copy is byte-identical on every run.
- `entry.png` — the finished page (1024 x 1024, under 1 MiB).
- `render_strong.py` — the renderer that drew the page with Pillow:
  layout, art panels, map panel and type are all computed from the data
  file, so the page can be rebuilt or revised by editing the data.
- `data_strong.json` — the day's census as data: headlines, summaries,
  figures, places and regions for every presented story, plus the
  held-back Friday list.

## License

MIT — see `LICENSE`.
