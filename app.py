from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from utils import  enhance_query
from pubmed import search_pubmed, fetch_abstracts
from chroma_store import store_documents, retrieve_chunks
from llm import generate_answer

load_dotenv()

app = Flask(__name__)


@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_query = request.json.get("query")

        if not user_query:
            return jsonify({"error": "Query required"}), 400

        enhanced_query = enhance_query(user_query)


        # Step 1: Search PubMed
        ids = search_pubmed(enhanced_query)

        if not ids:
            return jsonify({"error": "No articles found"}), 404

        # Step 2: Fetch abstracts
        abstracts = fetch_abstracts(ids)

        # Step 6: Store in vector DB
        collection=store_documents(abstracts)

        # Step 7: Retrieve relevant chunks
        chunks = retrieve_chunks(collection, enhanced_query)

        for i, c in enumerate(chunks):
            print(f"\nChunk {i+1}:\n",c[:200])

        # Step 8: Generate answer
        answer = generate_answer(user_query, chunks)

        links = [f"https://pubmed.ncbi.nlm.nih.gov/{id}" for id in ids]

        return jsonify({
            "answer": answer,
            "sources": links
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
