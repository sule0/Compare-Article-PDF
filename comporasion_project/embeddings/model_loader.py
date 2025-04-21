# embeddings/model_loader.py
from sentence_transformers import SentenceTransformer

def load_model():
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Hızlı ve yeterince güçlü
    return model
