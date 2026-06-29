import os
from pypdf import PdfReader

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

            chunks.append(chunk)

            metadata.append(
                {
                    "source": filename,
                    "page": page_num + 1
                }
            )

            start += (
                CHUNK_SIZE - OVERLAP
            )

print("Chunks:", len(chunks))
print(metadata[0])
print(metadata[0])
print(metadata[-1])

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings= model.encode(chunks)
print(f"Number of embeddings: {len(embeddings)}")

print(f"Embedding dimension: {len(embeddings[0])}")

print("\nFirst 10 values:\n")

print(embeddings[0][:10])
    