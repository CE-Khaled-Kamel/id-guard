import cv2
import pytesseract
import re

def preprocess_simple(img):
    """
    The Simple Preprocessing you requested.
    Grayscale -> Otsu Thresholding.
    No CLAHE, No Denoising.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Binary Thresholding (Otsu)
    # Finds the best contrast automatically
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary

def extract_california_pattern_only(image_path):
    print(f"--- 🐻 Scanning California (Pattern Only): {image_path} ---")
    
    # 1. Read & Resize
    img = cv2.imread(image_path)
    if img is None: return {"error": "Image not found"}
    
    scale = 1000 / img.shape[1]
    img = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))
    
    # 2. Preprocess (Simple)
    processed_img = preprocess_simple(img)
    cv2.imwrite("debug_pattern.jpg", processed_img)

    # 3. Run OCR
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_img, config=custom_config, lang='eng')
    
    # Force Uppercase & Clean
    # We remove everything except A-Z and 0-9 to make pattern matching easier
    clean_text = re.sub(r'[^A-Z0-9\n]', ' ', text.upper())
    print(f"Text Seen:\n{clean_text[:50]}...\n")

    result = {
        "dl_number": None,
        "confidence": "none",
        "method": "failed"
    }

    # --- STRATEGY 1: Strict California Pattern ---
    # Exactly 1 Letter followed by 7 Digits (e.g., "B1234567")
    # \b ensures it's a distinct word
    strict_pattern = r'\b([A-Z][0-9]{7})\b'
    match_strict = re.search(strict_pattern, clean_text)

    # --- STRATEGY 2: Repair Pattern (The "Glitch" Fix) ---
    # Looks for 8 characters that are *mostly* numbers.
    # We use this if Tesseract read "B" as "8" or "D" as "0"
    lax_pattern = r'\b([A-Z0-9][0-9]{7})\b'
    match_lax = re.search(lax_pattern, clean_text)

    if match_strict:
        result["dl_number"] = match_strict.group(1)
        result["confidence"] = "high"
        result["method"] = "strict_pattern"
    
    elif match_lax:
        raw_val = match_lax.group(1)
        first_char = raw_val[0]
        
        # Repair Mapping: Map numbers/letters back to valid California prefixes
        repairs = {
            '8': 'B', '1': 'I', 'L': 'I', 
            '0': 'D', 'O': 'D', 
            '5': 'S', '6': 'G', '2': 'Z'
        }
        
        if first_char in repairs:
            repaired_val = repairs[first_char] + raw_val[1:]
            result["dl_number"] = repaired_val
            result["confidence"] = "repaired"
            result["method"] = "repair_pattern"
        else:
            # If we can't map the first char, return it raw
            result["dl_number"] = raw_val
            result["confidence"] = "low"
            result["method"] = "raw_lax_pattern"

    return result

if __name__ == "__main__":
    data = extract_california_pattern_only("test_dl.jpg")
    print(f"✅ RESULT: {data}")