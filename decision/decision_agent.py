from fastapi import FastAPI, Body
import requests

app = FastAPI()

@app.post("/make-decision")
def make_decision(data: dict = Body(...)):
    earnings_summary = data.get("earnings_summary")
    news_summary = data.get("news_summary")
    context_info = data.get("context", "")

    if not earnings_summary and not news_summary:
        return {"error": "At least one of earnings_summary or news_summary is required."}

    # Construct prompt
    full_prompt = f"""
You are a financial analyst agent. Based on the earnings summary and news summary provided below,
you need to decide whether the company outlook is positive, negative, or neutral. 

Respond with one of the following decisions: INVEST, AVOID, or HOLD.

Earnings Summary:
{earnings_summary or "No earnings data provided."}

News Summary:
{news_summary or "No news data provided."}

Context:
{context_info or "No additional context."}

Give a brief rationale and your decision.
"""

    try:
        # Make request to local Ollama server
        summary_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",  # Use "llama2" or any model you have pulled
                "prompt": full_prompt,
                "stream": False
            }
        )
        summary_data = summary_response.json()
        decision_text = summary_data.get("response", "No decision returned.")

        return {
            "prompt_sent": full_prompt,
            "llm_raw_response": summary_data,
            "decision": decision_text
        }

    except Exception as e:
        return {"error": str(e)}

