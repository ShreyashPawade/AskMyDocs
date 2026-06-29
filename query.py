from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Connect to Chroma
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    "knowledge_base"
)

# Ask question
question = input("Question: ")

# Convert question to vector
query_embedding = model.encode(question)

# Search
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=3,
    include=["documents", "distances"]
)

print("\nTOP RESULTS:\n")

for i, doc in enumerate(results["documents"][0]):
    print(f"\nResult {i+1}")
    print("Distance:", results["distances"][0][i])
    print(doc[:300])