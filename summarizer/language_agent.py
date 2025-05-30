from fastapi import FastAPI, Body
import requests

app = FastAPI()

@app.post("/generate-summary")
def generate_summary(
    query: str = Body(..., embed=True),
    context_chunks: list[str] = Body(..., embed=True)
):
    full_context = "\n".join(context_chunks)

    prompt = f"""You are a financial assistant. Based on the context below, answer in a clear, professional tone.

Context:
{full_context}

Question: {query}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama2",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
        )

        if response.status_code == 200:
            response_json = response.json()
            return {
                "prompt_sent": prompt,
                "response": response_json.get("message", {}).get("content", "").strip()
            }
        else:
            return {"error": f"LLM returned non-200: {response.status_code}", "details": response.text}

    except Exception as e:
        return {"error": str(e)}
