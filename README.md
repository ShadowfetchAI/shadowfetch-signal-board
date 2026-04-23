# Shadowfetch Signal Board

`shadowfetch-signal-board` is Fook Me's second production repo.

It turns the raw report from `shadowfetch-builder-signal` into a simple product surface:
- a readable signal dashboard
- top GitHub projects and news stories
- app idea angles worth building or posting about

## Why this repo exists

Fook Me needed more than a data script.
She needed something that can be shown, inspected, and evolved into a real internal product surface.
This repo is that next step.

## Files that matter

- `build_board.py` builds the static board from the latest signal report
- `public/index.html` is the generated board
- `public/data/latest.json` is the mirrored source data
- `docs/product-notes.md` explains where the board can go next

## Build it

```bash
python3 build_board.py
```

## Serve it locally

```bash
python3 -m http.server 8080 -d public
```
