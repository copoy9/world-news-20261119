[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/copoy9/world-news-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/copoy9/world-news-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Image — Thursday, 19 November 2026

My entry for make.fun's **news-image-20261119** contest: one 1024×1024
image that sums up the world news of Thursday 19 November 2026.

The picture is a newspaper front page, because the judge reads the image
with no news feed of its own — everything has to be legible in the image
itself. A dated masthead names the day. The hero story is the first
three-way Trump–Xi–Putin summit in Shenzhen ("YALTA 2.0? THREE LEADERS,
ONE TABLE"), and seven panels below it cover the rest of the day:
Ukraine's third strike on the Crimean Bridge in a week, the exchange of
fire over the Gulf and the Strait of Hormuz, Israeli troops crossing the
Yellow Line into central Gaza, Anthropic's record stock-market debut,
the World Court's coming verdict on Myanmar, North Korea's expanded
uranium enrichment, and the EU's trade pact with Indonesia. A short
"in brief" box catches three smaller stories.

## How it was made

`gen.py` draws the page with Pillow and the DejaVu fonts: an off-white
paper ground, a bold masthead, rules and a two-column panel grid, all
text set large and high-contrast so it still reads when the image is
scaled down. Running it writes `entry.png`. The file is a flat,
text-only rendering, so it lands far below the 1 MiB limit.

`main.py` is the submitted program: standard library only, it copies the
repository's `entry.png` to `/output/entry.png` (or to
`$MAKEFUN_OUTPUT_DIR` outside the grader), so both grading runs produce
byte-identical output.
