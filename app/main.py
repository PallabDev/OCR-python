from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.ocr_service import extract_text_from_image, get_ocr_engine

logger = logging.getLogger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up / initialize PaddleOCR model on startup
    logger.info("Pre-warming PaddleOCR engine...")
    get_ocr_engine()
    yield


app = FastAPI(
    title="PaddleOCR FastAPI Service",
    description="High-accuracy text recognition API using PaddleOCR and FastAPI.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for cross-origin web client calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import os
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
FAVICON_PATH = os.path.join(PUBLIC_DIR, "favicon.ico")
HTML_FILE_PATH = os.path.join(os.path.dirname(__file__), "index.html")

# Mount public directory if exists
if os.path.exists(PUBLIC_DIR):
    app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Serves the favicon."""
    if os.path.exists(FAVICON_PATH):
        return FileResponse(FAVICON_PATH)
    raise HTTPException(status_code=404, detail="Favicon not found")


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    """Serves the interactive PaddleOCR web frontend."""
    return FileResponse(HTML_FILE_PATH)


@app.get("/health")
def health_check():
    """Service health and info endpoint."""
    return {
        "status": "online",
        "service": "PaddleOCR API",
        "language": "en",
        "endpoints": {
            "GET /": "Interactive Web UI",
            "POST /ocr": "Upload an image file as multipart/form-data with key 'file'"
        },
    }


@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    """Accepts an uploaded image file and returns extracted text."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    try:
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        result = extract_text_from_image(image_bytes)

        return {
            "success": True,
            "filename": file.filename,
            "text": result["text"],
            "lines": result["lines"],
            "total_lines": result["total_lines"],
        }
    except Exception as e:
        logger.error(f"Error processing image {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(e)}"
        )
