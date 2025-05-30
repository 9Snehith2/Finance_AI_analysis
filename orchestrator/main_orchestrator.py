from fastapi import FastAPI, Body
import requests

app = FastAPI()

@app.post("/analyze")
def analyze(data: dict = Body(...)):
    url = data.get("url")
    raw_text = data.get("text")

    if not url and not raw_text:
        return {"error": "Either 'url' or 'text' must be provided."}

    try:
        # Step 1: Get article text
        if url:
            scrape_resp = requests.post("http://127.0.0.1:8001/scrape-url", json={"url": url})
            scraped = scrape_resp.json()
            if "error" in scraped or not scraped.get("text"):
                return {"error": f"Scraping failed: {scraped.get('error', 'No text returned')}"}
            article_text = scraped["text"]
        else:
            article_text = raw_text

        # Step 2: Summarize article
        summary_resp = requests.post("http://127.0.0.1:8002/generate-summary", json={
            "query": "Summarize the article in simple financial language.",
            "context_chunks": [article_text]
        })
        summary_data = summary_resp.json()
        news_summary = summary_data.get("response", "").strip()

        # Step 3: Retrieve contextual documents
        retriever_resp = requests.get("http://127.0.0.1:8003/search-docs", params={"query": news_summary})
        retriever_json = retriever_resp.json()

        # Handle new retriever format: {"query": "...", "results": [...]}
        if isinstance(retriever_json, dict) and "results" in retriever_json:
            context_chunks = [doc.get("content", "") for doc in retriever_json["results"]]
        elif isinstance(retriever_json, list):
            context_chunks = [doc.get("content", "") for doc in retriever_json]
        else:
            return {"error": f"Unexpected response from retriever: {retriever_json}"}

        # Step 4: Make decision
        decision_resp = requests.post("http://127.0.0.1:8004/make-decision", json={
            "earnings_summary": news_summary,
            "news_summary": news_summary,
            "context": "\n\n".join(context_chunks)
        })
        decision_data = decision_resp.json()

        return {
            "source": "url" if url else "text",
            "scraped_text": article_text[:500] + "...",
            "summary": news_summary,
            "context_docs": context_chunks,
            "decision": decision_data.get("decision", "No decision returned.")
        }

    except Exception as e:
        return {"error": str(e)}
