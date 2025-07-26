from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import text_extractor, llm
import shutil
import os
import json

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/extract")
async def extract_data_from_file(file: UploadFile = File(...)):
    """
    Accepts a file, extracts its text content, gets a summary and keywords,
    and returns them in a JSON response.
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from the file
        content = text_extractor.extract_text(file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving or processing file: {e}")

    # Get summary and keywords from LLM
    llm_response = llm.get_summary_and_keywords(content)

    # Parse the llm_response to get summary and keywords
    try:
        data = json.loads(llm_response)
        summary = data.get("summary", "")
        keywords = data.get("keywords", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing LLM response: {e}")

    return {"summary": summary, "keywords": keywords}

