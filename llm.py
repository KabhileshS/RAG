import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")


def generate_answer(question, chunks):
    context = "\n\n".join(chunks)

    prompt = f"""
You are a medical assistant.
Answer using the context if relevant.
If context is incomplete, use general medical knowledge.
Use ONLY the context below.

Give:
1. Clear Answer
2. Key Findings
3. Summary

Question:
{question}

Context:
{context}
"""

    response = model.generate_content(prompt)
    return response.text


