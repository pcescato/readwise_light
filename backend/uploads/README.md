# Readwise Light

This project is a lightweight version of Readwise, allowing users to upload documents and receive summaries and keyword extractions.

## Features

-   Upload files (`.txt`, `.rtf`, `.docx`, `.odt`, `.md`).
-   Text extraction from various file formats.
-   Summarization and keyword extraction using an LLM.
-   View and download original files.
-   Keyword-based search.

## Tech Stack

-   **Frontend**: React with TailwindCSS
-   **Backend**: FastAPI (Python)
-   **Database**: AlloyDB (PostgreSQL-compatible)
-   **Deployment**: Docker

## Setup

1.  Clone the repository.
2.  Install backend dependencies: `pip install -r requirements.txt`
3.  Install frontend dependencies: `cd frontend && npm install`
4.  Set up your `.env` file based on `.env.sample`.
5.  Run the backend: `uvicorn app.main:app --reload`
6.  Run the frontend: `cd frontend && npm start`

## API

(Documentation to be added)
