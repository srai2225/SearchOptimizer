from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware
import phonetics

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and product data
model = SentenceTransformer('all-MiniLM-L6-v2')

with open("products.json", "r") as f:
    products = json.load(f)

@app.post("/semantic-search")
async def semantic_search(request: Request):
    body = await request.json()
    query = body["query"].strip().lower()

    # Semantic embedding
    query_embedding = model.encode([query])
    product_embeddings = [p["embedding"] for p in products]
    semantic_similarities = cosine_similarity(query_embedding, product_embeddings)[0]

    # Phonetic encoding
    query_phonetic = phonetics.dmetaphone(query)[0] or ""
    phonetic_scores = []
    for p in products:
        title_phonetic = phonetics.dmetaphone(p["title"].lower())[0] or ""
        phonetic_scores.append(1.0 if query_phonetic == title_phonetic else 0.0)

    results = []
    for product, semantic_score, phonetic_score in zip(products, semantic_similarities, phonetic_scores):
        title_match_boost = 1.0 if query in product["title"].lower() else 0.0
        hybrid_score = 0.75 * semantic_score + 0.15 * title_match_boost + 0.10 * phonetic_score
        results.append({
            "title": product["title"],
            "description": product["description"],
            "score": float(hybrid_score)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
