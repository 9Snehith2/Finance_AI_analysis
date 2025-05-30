from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import feedparser

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape-url")
def scrape_url(request: ScrapeRequest):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(request.url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")

        # fallback if <p> is empty
        if not paragraphs:
            paragraphs = soup.find_all(["div", "span"])

        text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        if not text.strip():
            return {"error": "No text returned."}

        return {"text": text[:5000]}  # limit to 5000 characters

    except Exception as e:
        return {"error": str(e)}

@app.get("/scrape-earnings")
def scrape_earnings():
    feed_url = "https://finance.yahoo.com/rss/topstories"
    feed = feedparser.parse(feed_url)

    results = []
    for entry in feed.entries[:5]:
        results.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })

    return results