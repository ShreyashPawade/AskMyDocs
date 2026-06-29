from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os

# -----------------
# Load PDF
# -----------------


chunks = []
metadata = []

CHUNK_SIZE = 500
OVERLAP = 100

for filename in os.listdir("docs"):

    if not filename.endswith(".pdf"):
        continue

    pdf_path = os.path.join(
        "docs",
        filename
    )

    print(f"Processing {filename}")

    reader = PdfReader(pdf_path)

    for page_num, page in enumerate(reader.pages):

        extracted = page.extract_text()

        if not extracted:
            continue

        start = 0

        while start < len(extracted):

            end = start + CHUNK_SIZE

            chunk = extracted[start:end]
            
            chunk_id=len(chunks)

            chunks.append(chunk)
            

            metadata.append(
                {
                    "chunk_id": chunk_id,
                    "source": filename,
                    "page": page_num + 1
                }
            )

            start += (
                CHUNK_SIZE - OVERLAP
            )

print("Chunks:", len(chunks))
print(metadata[0])

print(metadata[-1])

# -----------------
# Embeddings
# -----------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(chunks)

# -----------------
# Chroma
# -----------------





client = chromadb.PersistentClient(
    path="./chroma_db"
)

try:
    client.delete_collection(
        "knowledge_base"
    )
except:
    pass

collection = client.get_or_create_collection(
    name="knowledge_base"
)

for i, chunk in enumerate(chunks):

    collection.add(
        ids=[str(i)],
        embeddings=[embeddings[i].tolist()],
        documents=[chunk],
        metadatas=[metadata[i]]
    )

print("Stored successfully!")
print(collection.count())
import pickle

with open("bm25_index.pkl", "wb") as f:
    pickle.dump(
        {
            "chunks": chunks,
            "metadata": metadata
        },
        f
    )

print("BM25 index saved!")