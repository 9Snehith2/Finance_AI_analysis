FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8002

CMD ["uvicorn", "language_agent:app", "--host", "0.0.0.0", "--port", "8002"]
