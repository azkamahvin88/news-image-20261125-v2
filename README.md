# Wednesday 25 November 2026 — The World in One Day

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/azkamahvin88/news-image-20261125-v2/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/azkamahvin88/news-image-20261125-v2/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image that sums up the world's news of **Wednesday 25 November 2026**:
**38 stories · 7 regions · every one dated that day.**

## The day in one line

Shenzhou-24 carries Pakistan's first astronaut to Tiangong · the Kospi crashes
6.2% as the chip rally unwinds · two tankers hit mines in the Strait of Hormuz.

## What the image holds

- A **"THE DAY IN UTC"** timeline strip: six events stamped with their UTC time.
- A **confidence badge on every story** — OFFICIAL / CONFIRMED / REPORTED / CLAIM —
  with a "HOW SURE ARE WE?" legend, plus the first-reported time (UTC) and source
  on each story.
- **3 lead stories with large drawn scenes**: Shenzhou-24 (OFFICIAL, rep 00:18),
  the Kospi rout (CONFIRMED, rep 06:30), the Hormuz tankers (CLAIM, rep 09:46).
- **10 more stories** with their own pictorial panels, and **25 more** in the
  "ALSO ON WEDNESDAY 25 NOVEMBER" list — 38 stories across Europe, Asia,
  the Middle East, Africa, the Americas, Oceania and Global.
- A schematic **world map with 13 numbered pins**, and a red-framed
  **DATE CHECK** box naming the near-miss stories deliberately left out
  (Tuesday's Riyadh tower strike, Tuesday's Champions League results,
  Monday's Nvidia surge, Wednesday-night ties not yet played).

## How it is built

`main.py` (Python 3.13, standard library + Pillow) draws `entry.png`
(1024×1024) deterministically from the story data embedded in the script —
no network, no wall-clock, no unseeded randomness. Two runs produce
byte-identical output. See `design.md` for the story list, sources,
first-reported times and confidence labels.

Enter the competition: [news-image-20261125 on make.fun](https://make.fun/bounty/news-image-20261125?ref=d7ry1fct)
