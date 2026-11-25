[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Erwinsays12/makefun-news-image-20261125/rank.svg)](https://make.fun/c/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Erwinsays12/makefun-news-image-20261125/reward.svg)](https://make.fun/c/news-image-20261125)

# One image summing up 25 November world news

Entry for the [make.fun competition "Sum up 25 November's world news in one image"](https://make.fun/c/news-image-20261125).

`main.ts` copies `entry.png` to the output directory. The image is a one-page
newspaper front page for **Wednesday 25 November 2026**, drawn by `draw.py`
(Pillow) from the day's reported news:

- **Lead — Europe:** Ukraine confirms drone strikes on Russian ships at sea
  (Gulf of Finland cargo ship; warship sunk off Libya)
- **Middle East:** Houthi drone hits Riyadh's tallest tower, eleven wounded
- **United States:** Trump awards Rudy Giuliani the Medal of Freedom
- **Tech / China:** Huawei convicted in a US criminal trial over its Iran business
- **Business:** Nvidia shares jump 31.5% as Jensen Huang returns as CEO
- **Asia / India:** BJP and Shiromani Akali Dal reunite for the 2027 Punjab polls

Footer: Trump meets NATO chief Rutte; UN Day for the Elimination of Violence
against Women; England level the T20 series 1–1.

Run it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Regenerate the image with `python3 draw.py` (needs Pillow and DejaVu fonts).
