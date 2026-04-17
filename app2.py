import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
 
load_dotenv()
 
app = Flask(__name__)
 
# 🔹 Gemini Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)
# Use the newer, supported Gemini 3 model
model = genai.GenerativeModel("gemini-3-flash-preview")
 
# 🔹 Step 1: Search PubMed
def search_pubmed(query):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 3,
        "retmode": "json",
        "api_key": os.getenv("PUBMED_API_KEY")
    }
 
    res = requests.get(url, params=params)
    data = res.json()
    
    return data["esearchresult"]["idlist"]
 
# 🔹 Step 2: Fetch Abstracts
def fetch_abstracts(ids):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
 
    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml",
        "rettype": "abstract",
        "api_key": os.getenv("PUBMED_API_KEY")
    }
 
    res = requests.get(url, params=params)
    return res.text
 
# 🔹 Step 3: Ask Gemini
def ask_gemini(question, context):
    prompt = f"""
Answer the question using the research context below.
 
Give:
1. Clear Answer
2. Key Findings (bullet points)
3. Sources (PubMed links)
 
Question:
{question}
 
Context:
{context}
"""
    
    response = model.generate_content(prompt)
    return response.text
 
# 🔹 API Endpoint
@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_query = request.json.get("query")
 
        ids = search_pubmed(user_query)
        if not ids:
            return jsonify({"answer": "No relevant research found.", "sources": []})
        abstracts = fetch_abstracts(ids)
        answer = ask_gemini(user_query, abstracts)
 
        links = [f"https://pubmed.ncbi.nlm.nih.gov/{id}" for id in ids]
 
        return jsonify({
            "answer": answer,
            "sources": links
        })
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# 🔹 Run server
if __name__ == "__main__":
    app.run(debug=True)
 