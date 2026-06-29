from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os
import pickle
from document_registry import (remove_document,get_document)

# -----------------
# Configration
# -----------------




CHUNK_SIZE = 500
OVERLAP = 100



# -----------------
# Models
# -----------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


client = chromadb.PersistentClient(
    path="./chroma_db"
)



collection = client.get_or_create_collection(
    name="knowledge_base"
)


# -----------------
# Index one pdf
# -----------------


def index_pdf(pdf_path):
    
    filename=os.path.basename(pdf_path)
    
    if get_document(filename) is not None:
        return{
            "pages": 0,
            "chunks": 0,
            "filename": filename,
            "message": "Document already exists."
            
            
            
            
        }
    
    print(f"Indexing{filename }")
    
    reader = PdfReader(pdf_path)
    
    chunks=[]
    metadata=[]
    
    ## Curent collection size
    
    start_chunk_id=collection.count()
    
    # chunk pdf
    for page_num,page in enumerate(reader.pages):
        
        extracted = page.extract_text()
        
        if not extracted:
            continue
        
        start=0
        
        while start <len(extracted):
            
            end= start+CHUNK_SIZE
            
            chunk= extracted[start:end]
            
            chunk_id=(start_chunk_id+len(chunks))
            
            chunks.append(chunk)
            metadata.append (
                {
                    "chunk_id": chunk_id,
                    "source": filename,
                    "page":page_num +1
                    
                    
                }
            )
            
            start += (CHUNK_SIZE-OVERLAP)
            
        
    print("Chunks Generated: ",len(chunks))    
    
    ## embeddings
    
    print("Reached embeddings")

    
    embeddings= embedding_model.encode(chunks)
    
    print("Embeddings done")

    
    ## store in chroma
    for i in range(len(chunks)):
        try:
            collection.add(
            
                ids=[str(metadata[i]["chunk_id"])],
                
                embeddings=[embeddings[i].tolist()],
                
                documents=[chunks[i]],
                
                metadatas=[metadata[i]]
                
                
                
                
                
            )
        except Exception as e:
            print("Chroma Error:",e)
                
            
        print("Finished Chroma")
        print("Finished Chroma")

        

    
    print( "Collection Size:",  collection.count())
            
    
    ## upload BM25
    
    if os.path.exists("bm25_index.pkl"):
        with open("bm25_index.pkl","rb") as f:
            data = pickle.load(f)
            
            all_chunks=data["chunks"]
            all_metadata=data["metadata"]
            
    
    else:
        all_chunks=[]
        all_metadata=[]
        
    
    all_chunks.extend(chunks)
    all_metadata.extend(metadata)
    
    with open( "bm25_index.pkl", "wb") as f:
        
        pickle.dump(
            {
                "chunks": all_chunks,
                "metadata": all_metadata
            },
            f
        )
        
    
    print("BM25 Updated")
    
    ## return stats
    
    from document_registry import register_document
    
    register_document(
        
        filename,
        len(reader.pages),
        len(chunks)
    )
    
    return{
        
        "pages": len(reader.pages),
        "chunks": len(chunks),
        "filename": filename
        
        
        
        
        
        
        
    }
    

def delete_document(filename):
    
    
    ##. delete croma
    
    collection.delete(
        where={
            "source":filename
        }
    )
    with open("bm25_index.pkl","rb") as f:
        data = pickle.load(f)
        
    
    
    
    chunks=data["chunks"]
    metadata=data["metadata"]
        
        
    
    new_chunks=[]
    new_metadata=[]
    
    deleted_chunks=0
    
    for chunk,meta in zip(data["chunks"],data["metadata"]):
        
        if meta["source"]== filename:
            
            deleted_chunks+=1
            
        else:
            
            new_chunks.append(chunk)
            new_metadata.append(meta)
            
            
    with open("bm25_index.pkl","wb")as f:
        pickle.dump(
            {
                "chunks":new_chunks,
                "metadata": new_metadata
            },
            f
        )             
        
            
    
    if deleted_chunks==0:
        return False,0
    
    remove_document(filename)
    
    
    return True,deleted_chunks


def rebuild_database():

    global collection

    print("Deleting old database...")

    try:

        client.delete_collection(
            "knowledge_base"
        )

    except:

        pass

    collection = client.get_or_create_collection(
        "knowledge_base"
    )

    if os.path.exists(
        "bm25_index.pkl"
    ):

        os.remove(
            "bm25_index.pkl"
        )

    from document_registry import save_registry

    save_registry([])

    docs_folder = "docs"

    for file in os.listdir(
        docs_folder
    ):

        if file.endswith(".pdf"):

            print(
                f"Rebuilding {file}"
            )

            index_pdf(

                os.path.join(
                    docs_folder,
                    file
                )

            )

    print()

    print("Database Rebuilt Successfully!")
                
    
        
                
    
        
            
            
            
            
        
    
    

    
    
    
