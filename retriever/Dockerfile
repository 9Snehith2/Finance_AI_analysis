FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8003

CMD ["uvicorn", "retriever_agent:app", "--host", "0.0.0.0", "--port", "8003"]
