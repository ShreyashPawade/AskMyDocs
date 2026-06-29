import pickle
import os

REGISTRY_FILE= "document_registry.pkl"


def load_registry():
    
    if not os.path.exists(REGISTRY_FILE):
        return[]
    
    with open(REGISTRY_FILE,"rb") as f:
        return pickle.load(f)
    

def save_registry(registry):
    
    with open(REGISTRY_FILE,"wb") as f:
        pickle.dump(registry,f)
        

def register_document(
    filename,
    pages,
    chunks
):
    registry=load_registry()
    
    for doc in registry:
        if doc["filename"] == filename:
            return
    
    registry.append(
        {
            "filename":filename,
            "pages":pages,
            "chunks": chunks
        }
    )  
    
    save_registry(registry)
    

def get_documents():
    return load_registry()   


def get_document(filename):
    
    registry=load_registry()
    
    for doc in registry:
        if doc["filename"]== filename:
            return doc
        
    
    return None

def remove_document(filename):
    registry=load_registry()
    
    new_registry=[
        doc
        for doc in registry
        if doc["filename"]!=filename
    ]
    
    save_registry(new_registry)
               