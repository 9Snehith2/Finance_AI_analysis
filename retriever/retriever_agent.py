# agents/retriever_agent.py

from fastapi import FastAPI, Query
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

app = FastAPI()

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load and embed documents from the directory
doc_dir = "data_ingestion/sample_docs"
documents = []
doc_texts = []

# Read all .txt files from the directory
for filename in os.listdir(doc_dir):
    file_path = os.path.join(doc_dir, filename)
    if filename.endswith(".txt") and os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            documents.append((filename, text))
            doc_texts.append(text)

# Create FAISS index
if doc_texts:
    embeddings = model.encode(doc_texts)
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
else:
    index = None

@app.get("/search-docs")
def search_docs(query: str = Query(...), top_k: int = 3):
    if not index or len(documents) == 0:
        return {"error": "No documents available for search."}

    # Encode the search query
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            filename, content = documents[idx]
            results.append({
                "file": filename,
                "content": content
            })

    return {"query": query, "results": results}
