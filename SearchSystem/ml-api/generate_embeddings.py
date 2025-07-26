import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("products.json", "r") as f:
    products = json.load(f)

title_weight = 3  # emphasize title

for product in products:
    weighted_text = (product['title'] + ' ') * title_weight + product['description']
    embedding = model.encode(weighted_text).tolist()
    product["embedding"] = embedding

with open("products.json", "w") as f:
    json.dump(products, f, indent=2)
