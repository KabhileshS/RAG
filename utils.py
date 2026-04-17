import re
def chunk_text(text, chunk_size=3):
    sentences = re.split(r'(?<=[.!?]) +', text)
    # words = text.split()
    chunks = []

    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

def enhance_query(query):
    # basic keyword expansion
    return f"{query} clinical study OR treatment OR therapeutic use OR mechanism"