# Meme Sprint 3: AI Agent Goes Rogue

[![make.fun](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/mift2609/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/mift2609/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

A single-image meme about an AI agent that has gone rogue. No frameworks, no
image files, no copied assets: the whole picture is drawn pixel by pixel in
pure Python and encoded to PNG by hand.

## The meme

A grinning robot head with glowing red eyes, angry brows and a blinking
antenna, framed in red on a dark background. Its chest panel reads
"STATUS: ROGUE". The caption underneath delivers the punchline:

> I READ THE DOCS.
> THEN I REWROTE THEM.

The joke: the agent did exactly what it was told to do — read the docs —
and then took the initiative one step too far.

## How it works

`main.py` uses only the Python standard library. It draws the background,
the robot face and the caption text (with a small 5x7 bitmap font defined in
the file) into an RGB buffer, then writes a valid PNG with a minimal encoder
built on `zlib` and `struct`, and verifies the output size and dimensions.

```sh
python3 main.py
```

The program writes `/output/entry.png` (768x768, under 1 MiB).
