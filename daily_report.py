#!/usr/bin/env python3
import os, datetime, pytz
from openai import OpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5")

utc_now = datetime.datetime.now(datetime.timezone.utc)
et = utc_now.astimezone(pytz.timezone("America/New_York"))
cest = utc_now.astimezone(pytz.timezone("Europe/Stockholm"))
date_header = f"{et:%a, %b %d, %Y} — {et:%H:%M} ET / {cest:%H:%M} CEST"

SYSTEM = """You are an analyst. Use primary sources (BLS, BEA, FOMC/ECB/BoE/BoJ, DOE/EIA, OPEC+, stats agencies) and reputable outlets. Be concise, bullet-led, include exact release times & timezones. End with a 5-bullet TL;DR and a 2-week calendar."""
USER = f"""
Give me a detailed, up-to-date analysis of the current state of world economics from an American perspective. Structure into four sections:
1) Today — key events, data releases, and immediate market reactions.
2) The coming week — scheduled economic reports, central bank meetings, political/geopolitical events to watch, and likely market implications.
3) The coming month — broader trends, risks, and opportunities.
4) Stocks to watch — U.S.-listed names (8–12) that are volatile and ~break-even YTD (±5%) with ≥30% upside to 12-mo consensus target.
Formatting rules (strict): start with this timestamp line: {date_header}. Use concise bullets with one-line takeaways; include U.S. market impacts and global feedbacks; end with a compact 2-week calendar. Add a clear “Not investment advice” note.
"""

client = OpenAI(api_key=OPENAI_API_KEY)
resp = client.chat.completions.create(
    model=MODEL,
    messages=[{"role":"system","content":SYSTEM},{"role":"user","content":USER}],
    temperature=0.4,
)
body = resp.choices[0].message.content

# Write a markdown file the workflow will post to GitHub Issue/Discussion
title = f"Daily Macro & Stocks — {et:%b %d}"
with open("report_title.txt","w") as f: f.write(title)
with open("report.md","w") as f:
    f.write(f"### {date_header}\n\n")
    f.write(body)
    f.write("\n\n_Not investment advice._\n")
print("Report generated.")
