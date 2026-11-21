# One Day on Earth — Saturday 21 November 2026

Entry for the make.fun competition **news-image-20261121**: sum up one
day's world news in a single image.

## What is in the image

A single-page broadsheet of Saturday 21 November 2026, drawn as an
observatory-style world page: a large date masthead, an illustrated map
with the day's stories pinned in sun order, sixteen headlined dispatches
(each with its own drawn panel), a numbered briefs column, a sun-path
chart of the day, and a date-check box that lists the near-miss stories
held back because they belong to an earlier day.

Every story on the page happened, or was first reported, on 21 November
2026 in some time zone. Figures are as reported by the wires that day.

## How it runs

- `main.py` — the entrypoint. Standard library only. It copies the
  shipped `entry.png` into the output directory (`MAKEFUN_OUTPUT_DIR`,
  default `/output`). The copy is byte-identical on every run.
- `entry.png` — the finished page (1024 x 1024, under 1 MiB).
- `render_probe.py` — the renderer that drew the page with Pillow:
  layout, panels, map, charts and type are all computed from the data
  file, so the page can be rebuilt or revised by editing the data.
- `data_probe.json` — the day's census as data: headlines, summaries,
  figures, places and regions for every presented story, plus the
  held-back list.

## License

MIT — see `LICENSE`.
