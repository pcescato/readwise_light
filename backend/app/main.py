from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session
from . import crud, models, text_extractor, llm
from .db import engine, create_db_and_tables
import shutil
import os
import json
from typing import List

app = FastAPI()

def get_db():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Create a directory to store uploaded files
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the file
    try:
        content = text_extractor.extract_text(file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Get summary and keywords from LLM
    llm_response = llm.get_summary_and_keywords(content)

    # Parse the llm_response to get summary and keywords
    try:
        # Find the start of the JSON block
        json_start_index = llm_response.find("```json")
        if json_start_index == -1:
            raise ValueError("JSON block not found in the LLM response")

        summary = llm_response[:json_start_index].strip()
        json_str = llm_response[json_start_index + 7:].strip().strip("`")
        keywords = json.loads(json_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing LLM response: {e}")


    # Create document object
    doc = models.Document(
        filename=file.filename,
        content=content,
        summary=summary,
    )
    doc.set_keywords(keywords)
    db_doc = crud.create_document(db, doc)

    return db_doc

@app.get("/documents/", response_model=List[models.Document])
def get_documents(db: Session = Depends(get_db)):
    return crud.get_all_documents(db)

@app.get("/documents/{doc_id}", response_model=models.Document)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@app.get("/download/{doc_id}")
def download_file(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = os.path.join("uploads", doc.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=doc.filename)

@app.get("/search/")
def search_documents(query: str, db: Session = Depends(get_db)):
    # A simple search implementation
    docs = crud.get_all_documents(db)
    results = []
    for doc in docs:
        if query.lower() in doc.content.lower() or any(query.lower() in k.lower() for k in doc.get_keywords()):
            results.append(doc)
    return results

@app.get("/")
def read_root():
    return {"Hello": "World"}
