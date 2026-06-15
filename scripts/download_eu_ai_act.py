import httpx

url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689"
resp = httpx.get(url, timeout=60, follow_redirects=True)
resp.raise_for_status()
with open("data/eu-ai-act-raw.html", "w", encoding="utf-8") as f:
    f.write(resp.text)
print(f"Downloaded {len(resp.text):,} chars")
