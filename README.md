# FastAPI + PaddleOCR Service

High-accuracy OCR REST API powered by **FastAPI** and **PaddleOCR**, containerized with **Docker** and managed via **uv**.

---

## 🚀 How to Run

### 1. Build & Start with Docker Compose
Run the following command in the project directory:
```bash
docker compose up -d --build
```

### 2. Check Logs
```bash
docker compose logs -f
```

### 3. Stop the Service
```bash
docker compose down
```

---

## 📡 API Endpoints

### 1. Health Check
- **Endpoint**: `GET /`
- **Response**:
```json
{
  "status": "online",
  "service": "PaddleOCR API",
  "language": "en"
}
```

### 2. Extract Text (OCR)
- **Endpoint**: `POST /ocr`
- **Payload**: `multipart/form-data` with form field `file` containing the image.

#### Example using `cURL`:
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.png"
```

#### Example Response:
```json
{
  "success": true,
  "filename": "sample.png",
  "text": "Hello World\nFastAPI and PaddleOCR",
  "lines": [
    {
      "text": "Hello World",
      "confidence": 0.9982,
      "box": [[10, 20], [150, 20], [150, 60], [10, 60]]
    },
    {
      "text": "FastAPI and PaddleOCR",
      "confidence": 0.9945,
      "box": [[10, 70], [300, 70], [300, 110], [10, 110]]
    }
  ],
  "total_lines": 2
}
```

---

## 📖 Interactive API Docs
Once running, you can visit interactive Swagger documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
