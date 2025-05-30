from fastapi import FastAPI, Body
import requests

app = FastAPI()

@app.post("/summarize-url")
def summarize_url(data: dict = Body(...)):
    url = data.get("url")
    if not url:
        return {"error": "URL is required"}

    try:
        # 1. Call the scraping agent
        scrape_response = requests.post(
            "http://127.0.0.1:8000/scrape-url",
            json={"url": url}
        )
        scrape_data = scrape_response.json()
        print("SCRAPER RESPONSE:", scrape_data)

        # 2. Validate and extract scraped text
        if not scrape_data.get("text"):
            # If scraping failed, fallback to mock text (optional)
            # scraped_text = "TSMC reported a 4% beat on Q2 earnings. Revenue increased due to strong demand in AI chips. Samsung missed estimates by 2% due to consumer electronics slowdown."
            return {"error": f"Scraping failed: {scrape_data.get('error', 'No text returned.')}"}
        else:
            scraped_text = scrape_data["text"]

        # 3. Call the summarizer agent (LLaMA via Ollama)
        summary_response = requests.post(
            "http://127.0.0.1:8000/generate-summary",
            json={
                "query": "Summarize this article in simple financial language.",
                "context_chunks": [scraped_text]
            }
        )
        summary_data = summary_response.json()

        return {"summary": summary_data.get("response", "No summary returned.")}
    
    except Exception as e:
        return {"error": str(e)}
