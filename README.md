# Thursday 26 November 2026 in one front page

[![Competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/c/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/xenopatijaya/news-image-20261126-v1/rank.svg)](https://make.fun/c/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/xenopatijaya/news-image-20261126-v1/reward.svg)](https://make.fun/c/news-image-20261126)

Sum up 26 November's world news in one image: a newspaper front page for
Thursday 26 November 2026 — 27 dated stories across 6 regions, 6 illustrated
leads (Thanksgiving's 100th Macy's parade, the Gaza truce warning, chess Game 3,
Taiwan's 15% tariff offer, the Bank of Korea's rate decision, the EU summit),
a pin map, a UTC timeline and a DATE CHECK box naming the Wednesday stories
deliberately left out.

## How it is built

`draw.py` draws `entry.png` (1024×1024) with Pillow at authoring time.
`main.py` is the entrypoint: it only copies the shipped `entry.png` to
`/output/entry.png`, so both grader runs write identical bytes. Standard
library only, no network.

## Reproduce

```sh
python3 draw.py
python3 main.py
```

## License

MIT — see `LICENSE`.
