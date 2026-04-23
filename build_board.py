#!/usr/bin/env python3
import datetime as dt
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE_REPORT = pathlib.Path('/home/rtx5060ti/production/shadowfetch-builder-signal/reports/latest.json')
OUT_JSON = ROOT / 'public' / 'data' / 'latest.json'
OUT_HTML = ROOT / 'public' / 'index.html'


def load_report() -> dict:
    if not SOURCE_REPORT.exists():
        return {
            'summary': {'generated_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'top_repo': '', 'top_news': '', 'repo_count': 0, 'news_count': 0},
            'repos': [],
            'news': [],
            'ideas': [],
        }
    return json.loads(SOURCE_REPORT.read_text())


def card(title: str, body: str, meta: list[str]) -> str:
    meta_html = ''.join(f'<li>{html.escape(item)}</li>' for item in meta if item)
    return f'''<article class="card"><h3>{html.escape(title)}</h3><p>{html.escape(body)}</p><ul>{meta_html}</ul></article>'''


def render(report: dict) -> str:
    summary = report.get('summary', {})
    repos = report.get('repos', [])[:6]
    news = report.get('news', [])[:6]
    ideas = report.get('ideas', [])[:6]
    repo_cards = '\n'.join(
        card(
            repo.get('name', 'Unknown repo'),
            repo.get('description') or 'No description provided.',
            [f"Language: {repo.get('language', 'Unknown')}", f"Stars: {repo.get('stars', 0)}", f"Score: {repo.get('score', 0)}", repo.get('url', '')],
        )
        for repo in repos
    ) or '<p class="empty">No repo signal yet.</p>'
    news_cards = '\n'.join(
        card(
            item.get('title', 'Unknown story'),
            'High-signal discussion worth scanning for product reactions and founder commentary.',
            [f"Points: {item.get('points', 0)}", f"Comments: {item.get('comments', 0)}", item.get('url', '')],
        )
        for item in news
    ) or '<p class="empty">No news signal yet.</p>'
    idea_cards = '\n'.join(
        card(
            idea.get('name', 'Untitled idea'),
            idea.get('thesis', ''),
            [f"Why now: {idea.get('why_now', '')}"],
        )
        for idea in ideas
    ) or '<p class="empty">No idea angles yet.</p>'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Shadowfetch Signal Board</title>
  <style>
    :root {{
      --bg: #0a1118;
      --panel: rgba(15, 25, 36, 0.9);
      --soft: #8db0c7;
      --text: #eff7ff;
      --accent: #8ff0c5;
      --accent-2: #f9ba61;
      --line: rgba(143, 240, 197, 0.18);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: ui-rounded, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: radial-gradient(circle at top, #18324f 0%, var(--bg) 58%); color: var(--text); }}
    .shell {{ max-width: 1180px; margin: 0 auto; padding: 36px 22px 64px; }}
    .hero {{ display: grid; gap: 18px; padding: 28px; border: 1px solid var(--line); background: linear-gradient(140deg, rgba(17, 32, 49, 0.96), rgba(10, 17, 24, 0.96)); border-radius: 28px; box-shadow: 0 20px 60px rgba(0,0,0,0.28); }}
    .eyebrow {{ color: var(--accent); letter-spacing: 0.16em; text-transform: uppercase; font-size: 12px; font-weight: 700; }}
    h1 {{ margin: 0; font-size: clamp(34px, 6vw, 62px); line-height: 0.96; max-width: 9ch; }}
    .lede {{ max-width: 72ch; color: #d7e8f6; font-size: 17px; line-height: 1.6; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-top: 10px; }}
    .stat {{ padding: 16px 18px; border-radius: 18px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); }}
    .stat span {{ display:block; color: var(--soft); font-size: 13px; margin-bottom: 8px; }}
    .stat strong {{ font-size: 20px; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 28px; }}
    .section-title {{ margin: 36px 0 0; font-size: 13px; letter-spacing: 0.16em; color: var(--accent-2); text-transform: uppercase; }}
    .card {{ border-radius: 22px; background: var(--panel); border: 1px solid rgba(255,255,255,0.05); padding: 18px; min-height: 220px; }}
    .card h3 {{ margin: 0 0 10px; font-size: 22px; line-height: 1.15; }}
    .card p {{ color: #d1dfeb; line-height: 1.55; }}
    .card ul {{ padding-left: 18px; color: var(--soft); line-height: 1.5; }}
    .empty {{ color: var(--soft); }}
    .footer {{ margin-top: 40px; color: var(--soft); font-size: 13px; }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="eyebrow">Shadowfetch production board</div>
      <h1>Builder signal, organized.</h1>
      <p class="lede">Fook Me's live board for tracking GitHub momentum, Hacker News discussion, and app-idea angles worth turning into product or content.</p>
      <div class="stats">
        <div class="stat"><span>Generated</span><strong>{html.escape(summary.get('generated_at', ''))}</strong></div>
        <div class="stat"><span>Top repo</span><strong>{html.escape(summary.get('top_repo', 'None yet'))}</strong></div>
        <div class="stat"><span>Top news</span><strong>{html.escape(summary.get('top_news', 'None yet'))}</strong></div>
        <div class="stat"><span>Coverage</span><strong>{summary.get('repo_count', 0)} repos / {summary.get('news_count', 0)} stories</strong></div>
      </div>
    </section>
    <p class="section-title">GitHub signal</p>
    <section class="grid">{repo_cards}</section>
    <p class="section-title">News signal</p>
    <section class="grid">{news_cards}</section>
    <p class="section-title">Product angles</p>
    <section class="grid">{idea_cards}</section>
    <p class="footer">Built automatically from <code>shadowfetch-builder-signal</code>. Open this file directly or serve the <code>public</code> directory.</p>
  </main>
</body>
</html>
'''


def main() -> int:
    report = load_report()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2) + '\n')
    OUT_HTML.write_text(render(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
