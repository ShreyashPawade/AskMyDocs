from fastapi import FastAPI
from model import ChatRequest
from retriever import (hybrid_search,reload_bm25)
from fastapi import UploadFile, File
import os
import shutil
from document_registry import (get_documents,get_document)

from vector_store import (index_pdf,delete_document)

from fastapi import Request
from fastapi.responses import JSONResponse

import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

from  fastapi.responses import StreamingResponse

from llm import( rewrite_query, generate_answer,stream_answer)






UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


from llm import (
    rewrite_query,
    generate_answer
)

# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI(
    title="AskMyDocs API",
    version="1.0"
)



## GLobal exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    
    
    logger.exception("Unhandled Exception")

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc)
        }
    )





# -----------------------------------
# Temporary Conversation Memory
# (Will replace with session memory later)
# -----------------------------------

chat_sessions = {}


# -----------------------------------
# Home
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "AskMyDocs API is running!"
    }

# -----------------------------------
# Chat Endpoint
# -----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):
    
    session_id = request.session_id

    if session_id not in chat_sessions:

        chat_sessions[session_id] = []

    history = chat_sessions[session_id]


    question = request.question

    # -----------------------------
    # Rewrite Query
    # -----------------------------

    rewritten_question = rewrite_query(
        question,
        history
    )

    print("\nRewritten Query:")
    print(rewritten_question)

    # -----------------------------
    # Hybrid Retrieval
    # -----------------------------

    context, sources, confidence = hybrid_search(
        rewritten_question
    )

    print("\nRetriever Confidence:")
    print(confidence)

    # -----------------------------
    # Low Confidence
    # -----------------------------

    if confidence < 1:

        return {

            "answer":
            "I couldn't confidently find the answer in the uploaded documents.",

            "sources": [],

            "confidence": confidence
        }

    # -----------------------------
    # Generate Answer
    # -----------------------------

    answer = generate_answer(

        question,

        context,

        history
    )

    # -----------------------------
    # Update Conversation Memory
    # -----------------------------

    history.append(

        {

            "question": question,

            "answer": answer

        }

    )

    # Keep only last 10 turns

    if len(history) > 10:

        history.pop(0)

    # -----------------------------
    # Response
    # -----------------------------

    return {

        "answer": answer,

        "sources": sources,

        "confidence": confidence
    }
    
    


@app.post("/upload")
def upload_pdf(
    file: UploadFile = File(...)
):

    # -----------------------------
    # Check file type
    # -----------------------------

    if not file.filename.lower().endswith(".pdf"):

        return {

            "status": "error",

            "message": "Only PDF files are allowed."
        }

    # -----------------------------
    # Save uploaded file
    # -----------------------------

    save_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(
        save_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # -----------------------------
    # Index PDF
    # -----------------------------

    result = index_pdf(
        save_path
    )
    
    print("INDEX RESULT:", result)
    
    if result["chunks"]>0:
        reload_bm25()
        
    
    

    # -----------------------------
    # Success
    # -----------------------------

    return {

        "status": "success",

        "filename": file.filename,

        "pages": result["pages"],

        "chunks": result["chunks"],

        "message": "PDF indexed successfully."
    }  
    
    

@app.get("/documents")
def list_documents():
    return{
        "documents":
            get_documents()
    }
    

@app.delete("/documents/{filename}")
def delete_document_api(
    filename:str
):
    success,deleted_chunks= delete_document(filename)
    
    if not success:
        return{
            
            "status":"errror",
            "message":" Document not found."
            
        }
        
    reload_bm25()
    
    return{
        
        "status":"success",
        "filename": filename,
        "deleted_chunks": deleted_chunks,
        "message": " Document deleted",
        
    }    
    
    


@app.get("/documents/{filename}")   
def document_details(
    filename:str 
):
    document=get_document(filename)
    if document is None:
        return{
            
            "status": "error",
            "message":" Document not found"
        } 
        
    return document     
    
    

    
        
@app.post("/chat_stream")
def chat_stream(request: ChatRequest):

    session_id = request.session_id

    if session_id not in chat_sessions:

        chat_sessions[session_id] = []

    history = chat_sessions[session_id]

    question = request.question

    # -----------------------------
    # Rewrite Query
    # -----------------------------

    rewritten_question = rewrite_query(
        question,
        history
    )

    print("\nRewritten Query:")
    print(rewritten_question)

    # -----------------------------
    # Hybrid Retrieval
    # -----------------------------

    context, sources, confidence = hybrid_search(
        rewritten_question
    )

    print("\nRetriever Confidence:")
    print(confidence)

    if confidence < 1:

        return StreamingResponse(
            iter([
                "I couldn't confidently find the answer in the uploaded documents."
            ]),
            media_type="text/plain"
        )

    # -----------------------------
    # Stream Response
    # -----------------------------

    return StreamingResponse(

        stream_answer(
            question,
            context,
            history
        ),

        media_type="text/plain"
    )

@app.get("/health")
def health():
    return {
        "status": "online"
    }    