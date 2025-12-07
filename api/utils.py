# api/utils.py
import cv2
import pytesseract
import re
import numpy as np

def preprocess_simple(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def extract_id_from_image(image_stream):
    """
    Takes an Image File (from HTTP request), reads it, and finds the CA ID.
    """
    # 1. Convert HTTP Upload -> OpenCV Image
    # We use numpy to read the raw bytes without saving to disk (Faster!)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"error": "Invalid image file"}

    # 2. Resize
    scale = 1000 / img.shape[1]
    img = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))

    # 3. Process
    processed_img = preprocess_simple(img)

    # 4. OCR
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_img, config=custom_config, lang='eng')
    
    # 5. Extract (Your Pattern Logic)
    clean_text = re.sub(r'[^A-Z0-9\n]', ' ', text.upper())
    
    result = {"dl_number": None, "confidence": "none"}

    # Strict Pattern
    match_strict = re.search(r'\b([A-Z][0-9]{7})\b', clean_text)
    # Repair Pattern
    match_lax = re.search(r'\b([A-Z0-9][0-9]{7})\b', clean_text)

    if match_strict:
        result["dl_number"] = match_strict.group(1)
        result["confidence"] = "high"
    elif match_lax:
        # Simple Repair Logic
        raw = match_lax.group(1)
        repairs = {'8': 'B', '1': 'I', 'L': 'I', '0': 'D', '5': 'S', '6': 'G', '2': 'Z'}
        if raw[0] in repairs:
            result["dl_number"] = repairs[raw[0]] + raw[1:]
            result["confidence"] = "repaired"
        else:
            result["dl_number"] = raw
            result["confidence"] = "low"
            
    return result