import io
import logging
from typing import Any, Dict, List
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

logger = logging.getLogger("ocr_service")
logging.basicConfig(level=logging.INFO)

# Initialize PaddleOCR with English language and angle classification
# use_angle_cls=True enables orientation correction for higher accuracy
_ocr_engine: PaddleOCR | None = None


def get_ocr_engine() -> PaddleOCR:
    global _ocr_engine
    if _ocr_engine is None:
        logger.info("Initializing PaddleOCR engine (lang='en', use_angle_cls=True)...")
        _ocr_engine = PaddleOCR(
            use_angle_cls=True,
            lang="en"
        )
        logger.info("PaddleOCR engine initialized successfully.")
    return _ocr_engine


def extract_text_from_image(image_bytes: bytes) -> Dict[str, Any]:
    """Extract text, bounding boxes, and confidence scores from raw image bytes.

    Args:
        image_bytes: The binary content of the uploaded image.

    Returns:
        Dict containing full text, detailed line items, and line count.
    """
    ocr = get_ocr_engine()

    # Open image with PIL and convert to RGB
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_array = np.array(image)

    # Perform OCR detection and recognition
    results = ocr.ocr(img_array, cls=True)

    extracted_lines: List[Dict[str, Any]] = []
    text_blocks: List[str] = []

    if results and len(results) > 0 and results[0] is not None:
        for item in results[0]:
            box = item[0]  # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            text, score = item[1]

            extracted_lines.append({
                "text": text,
                "confidence": round(float(score), 4),
                "box": box,
            })
            text_blocks.append(text)

    full_text = "\n".join(text_blocks)

    return {
        "text": full_text,
        "lines": extracted_lines,
        "total_lines": len(extracted_lines),
    }
