import os
import re

DOCUMENTS_FOLDER = "documents"
CHUNK_SIZE = 400
OVERLAP = 50

def load_documents(folder):
    """Load all .txt files from the documents folder."""
    documents = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt") and filename != ".gitkeep":
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({"source": filename, "text": text})
            print(f"Loaded: {filename} ({len(text)} characters)")
    return documents

def clean_text(text):
    """Remove HTML tags, extra whitespace, and boilerplate."""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove HTML entities like &amp; &nbsp;
    text = re.sub(r"&[a-z]+;", " ", text)
    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    # Collapse multiple spaces and newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()

def chunk_text(text, source, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 50:  # skip tiny fragments
            chunks.append({"source": source, "text": chunk})
        start += chunk_size - overlap
    return chunks

def run_pipeline():
    docs = load_documents(DOCUMENTS_FOLDER)
    all_chunks = []

    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, doc["source"])
        all_chunks.extend(chunks)

    print(f"\n✅ Total chunks: {len(all_chunks)}")

    # Print 5 sample chunks to inspect
    print("\n--- 5 SAMPLE CHUNKS ---")
    import random
    for chunk in random.sample(all_chunks, min(5, len(all_chunks))):
        print(f"\n[Source: {chunk['source']}]")
        print(chunk["text"])
        print("-" * 40)

    return all_chunks

if __name__ == "__main__":
    run_pipeline()