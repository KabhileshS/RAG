import chromadb
from sentence_transformers import SentenceTransformer
from utils import chunk_text
import uuid
import os
import google.generativeai as genai

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

# def get_embedding(text):
#     response = genai.embed_content(
#         model="embedding-001",
#         content=text
#     )
#     return response["embeddings"]



# Create DB

# collection = client.get_or_create_collection(name="medical_docs")


def store_documents(text):
    # collection.delete()  # clear old data
    # collection.delete(where={})  # clear old data

    collection = client.create_collection(name=f"medical_{uuid.uuid4()}")

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        # embedding=get_embedding(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{i}"]
        )
    
    return collection


def retrieve_chunks(collection , query, k=5):
    query_embedding = embedding_model.encode(query).tolist()
    # query_embedding=get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]


