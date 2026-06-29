import pickle
from rank_bm25 import BM25Okapi
import nltk
import chromadb
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

import os

nltk.download("stopwords")

from nltk.corpus import stopwords

STOP_WORDS = set(
    stopwords.words("english")
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    "knowledge_base"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

reranker=CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def chroma_search(
    question,
    k
):

    query_embedding = (
        embedding_model.encode(
            question
        )
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=k,
        include=[
            "metadatas",
            "distances"
        ]
    )

    return results

def reciprocal_rank_fusion(
    bm25_ids,
    chroma_ids
):

    scores = {}

    # BM25 contribution
    for rank, chunk_id in enumerate(bm25_ids):

        scores[chunk_id] = (
            scores.get(chunk_id, 0)
            + 1/(rank+1)
        )

    # Chroma contribution
    for rank, chunk_id in enumerate(chroma_ids):

        scores[chunk_id] = (
            scores.get(chunk_id, 0)
            + 1/(rank+1)
        )

    return sorted(
        scores.items(), ## conver dict into tuple [(78,2),]
       
        key=lambda x: x[1], ## x[0]=chubk_id, x[1]=score rank based on score
        reverse=True
    )

def preprocess(text):

    words = text.lower().split()

    return [
        w.strip(".,?!()")
        for w in words
        if w not in STOP_WORDS
    ]
    

chunks = []
metadata = []
bm25 = None

def load_bm25():

    global chunks
    global metadata
    global bm25
    
    if not os.path.exists("bm25_index.pkl"):
        print("BM25 index not found.")
        chunks=[]
        metadata=[]
        bm25=None
        
        return
        
        
        
        
        

    with open(
        "bm25_index.pkl",
        "rb"
    ) as f:

        data = pickle.load(f)

    chunks = data["chunks"]
    metadata = data["metadata"]

    tokenized_chunks = [

        preprocess(chunk)

        for chunk in chunks

    ]

    bm25 = BM25Okapi(
        tokenized_chunks
    )
    

def reload_bm25():

    load_bm25()

    print(
        "BM25 Reloaded Successfully!"
    )



load_bm25()      


def bm25_search(question, k):

    query_tokens = preprocess(question)

    scores = bm25.get_scores(query_tokens)

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:k]




    

def hybrid_search(question,k=20):
    
    ## BM25
    
    bm25_results=bm25_search(question,k)
    bm25_ids=[]
    
    for idx,score in bm25_results:
        bm25_ids.append(idx)
        
    
    ## Chroma
    chroma_results=chroma_search(question,k)
    chroma_ids=[]
    
    for meta in chroma_results["metadatas"][0]:
        chroma_ids.append(
            meta["chunk_id"]
        )    
        
        
    
    ## fusion
    
    fused= reciprocal_rank_fusion(bm25_ids,chroma_ids)  
    
    pairs=[]
    candidate_ids=[]
    
    for chunk_id,_ in fused[:k]:
        pairs.append(
            (question,
                     chunks[chunk_id])
            
        )
        candidate_ids.append(chunk_id)
        
    
    scores= reranker.predict(pairs)
    
    reranked=list(zip(candidate_ids,scores))
    
    top_scores=sorted(scores,reverse=True)[:3]
    confidence=(sum(top_scores)/len(top_scores))
    
    print(
    f"Retriever Confidence: "
    f"{confidence:.2f}"
    )
    
    if confidence<1:
        return("",[],float(confidence))

    
    reranked=sorted(reranked,key=lambda x:x[1], reverse=True)    
    
    
      
    
    ## recover text
    THRESHOLD=2.0
    context_chunks=[]
    sources=[]
    
    for chunk_id,score in reranked:
        if score<THRESHOLD:
            continue
        
        context_chunks.append(chunks[chunk_id])
        sources.append(metadata[chunk_id])
        
        if len(context_chunks)==5:
            break
        
    
    
    context="\n\n".join(context_chunks)
    confidence=float(confidence)
    
    
    return (context,sources,confidence)   
    


# ------------------
# TEMPORARY TEST
# ------------------


if __name__ =="__main__":
    context,sources,confidence=hybrid_search("What is Strength of Figure?")

    print("CONTEXT\n")
    print(context[:800])

    print("\nSOURCES\n")

    for s in sources:
        print(s)
    


