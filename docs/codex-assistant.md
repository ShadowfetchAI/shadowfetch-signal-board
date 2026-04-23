# Codex guide for `shadowfetch-signal-board`

Use Codex here for concrete board work, not general ideation.

## What Codex should know

- `build_board.py` is the source of truth for the board
- `public/index.html` and `public/data/latest.json` are generated outputs
- upstream input comes from `/home/rtx5060ti/production/shadowfetch-builder-signal/reports/latest.json`

## Good ways to use Codex

- change layout, copy, ordering, limits, or card content by editing `build_board.py`
- add a small new section if it can be derived from the existing report shape
- tighten the local workflow or docs when the change needs a short operator note

## What to avoid

- hand-editing `public/` without updating the generator
- adding heavy tooling or framework churn to a simple static board
- touching other repos unless the task clearly depends on upstream report structure

## Default verification

```bash
python3 build_board.py
python3 -m http.server 8080 -d public
```

Then confirm the board renders and the generated JSON still mirrors the upstream report cleanly.
