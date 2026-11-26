# The World Today — 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/c/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/aramexbit/news-image-20261126/rank.svg)](https://make.fun/c/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/aramexbit/news-image-20261126/reward.svg)](https://make.fun/c/news-image-20261126)

An entry for the [make.fun](https://make.fun/c/news-image-20261126)
competition **news-image-20261126**: sum up the world's news of Thursday
26 November 2026 in one image.

`main.py` draws a dense newspaper front page (1024×1024) with ten
verified stories from that day: the EU special summit in Brussels, the
Bank of Korea rate rise, India's Constitution Day, US Thanksgiving, the
World Chess Championship, the Wang Fuk Court fire anniversary, the Gaza
strikes, the UK reservist call-up, the Mumbai 26/11 anniversary and the
overnight Kyiv strike. The program writes the image to
`/output/entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program needs no network. It draws with Pillow when Pillow is
present; in the grading sandbox (standard library only) it copies the
prebuilt `entry.png` shipped in this repository instead, so the output
is the same bytes either way. No timestamps and no randomness: two runs
write identical bytes.

## License

MIT — see [LICENSE](LICENSE).
