
import os
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
import sys

# Tesseract Configuration
OCR_AVAILABLE = False
try:
    import pytesseract
    from PIL import Image
    import io
    
    # Common Tesseract Paths on Windows
    potentials = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.getenv('LOCALAPPDATA', ''), r'Programs\Tesseract-OCR\tesseract.exe')
    ]
    
    tess_path = None
    for p in potentials:
        if os.path.exists(p):
            tess_path = p
            break
            
    # Local Tessdata Path
    local_tessdata = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tessdata")
    tessdata_config = f'--tessdata-dir {local_tessdata}' if os.path.exists(local_tessdata) else ""

    if tess_path:
        pytesseract.pytesseract.tesseract_cmd = tess_path
        OCR_AVAILABLE = True
        print(f"Tesseract found at: {tess_path}")
        if tessdata_config:
            print(f"Using local tessdata: {local_tessdata}")
    else:
        print("Warning: Tesseract.exe not found in standard paths. OCR will be disabled.")
        
except ImportError:
    print("Warning: pytesseract or Pillow not installed. OCR will be disabled.")


# Config
TARGET_DIR = r"C:\Users\sam\Desktop\02_Personal_Finance\KARANNAGAR CASE"
GUJARATI_NUMERALS = {
    '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4',
    '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9'
}

def normalize_gujarati_numerals(text):
    for g, e in GUJARATI_NUMERALS.items():
        text = text.replace(g, e)
    return text

def find_date_in_text(text):
    """
    Tier 1 & 2: Regex Extraction
    """
    if not text: return None
    text = normalize_gujarati_numerals(text)
    
    # Patterns
    patterns = [
        r'\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})\b',       # DD-MM-YYYY
        r'\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b',       # YYYY-MM-DD
        r'\b(\d{1,2})\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s(\d{4})\b' # DD Mon YYYY
    ]
    
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            g1, g2, g3 = match.groups()
            if len(g3) == 4: day, month, year = g1, g2, g3
            elif len(g1) == 4: year, month, day = g1, g2, g3
            else: continue
            
            try:
                # Basic validation
                month_map = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
                if month.lower()[:3] in month_map:
                    month = month_map[month.lower()[:3]]
                
                dt = datetime(int(year), int(month), int(day))
                if 1900 < dt.year < 2100:
                    return dt.strftime("%Y-%m-%d")
            except:
                continue
    return None

def get_system_date(filepath):
    """Tier 3: System Timestamp"""
    ts = filepath.stat().st_mtime
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

def deep_scan_file(filepath):
    filename = filepath.name
    if not filename.startswith("2023-01-01"):
        return None, None

    print(f"Analyzing: {filename}")

    # --- Tier 1: Digital Text ---
    text_content = ""
    try:
        if filepath.suffix.lower() == ".pdf":
            doc = fitz.open(filepath)
            for i in range(min(5, len(doc))):
                text_content += doc[i].get_text()
        else:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text_content = f.read(5000)
    except Exception as e:
        pass

    date_found = find_date_in_text(text_content)
    if date_found:
        return date_found, "Tier 1 (Regex)"

    # --- Tier 2: Tesseract OCR ---
    if OCR_AVAILABLE and filepath.suffix.lower() in [".pdf", ".jpg", ".png", ".jpeg"]:
        print("  ... Tier 1 failed. Attempting Tier 2 (Tesseract OCR)...")
        try:
            pil_images = []
            if filepath.suffix.lower() == ".pdf":
                doc = fitz.open(filepath)
                # Render first page as image (300 DPI for better OCR)
                page = doc.load_page(0)
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                pil_images.append(Image.open(io.BytesIO(img_data)))
            else:
                pil_images.append(Image.open(filepath))
            
            for img in pil_images:
                # Try Gujarati + English
                # Better to specify 'eng+guj'
                ocr_text = pytesseract.image_to_string(img, lang='eng+guj', config=tessdata_config)
                date_found = find_date_in_text(ocr_text)
                if date_found:
                     return date_found, "Tier 2 (Tesseract)"
                     
        except Exception as e:
            print(f"  OCR Failed: {e}")

    # --- Tier 3: System Metadata ---
    print("  ... Tier 2 failed. Using Tier 3 (System Date).")
    return get_system_date(filepath), "Tier 3 (System Fallback)"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Don't rename files")
    args = parser.parse_args()

    base = Path(TARGET_DIR)
    renames = []
    
    for root, dirs, files in os.walk(base):
        for f in files:
            if not f.startswith("2023-01-01"): continue
            
            filepath = Path(root) / f
            new_date, method = deep_scan_file(filepath)
            
            if new_date:
                parts = f.split("_", 1)
                if len(parts) < 2: continue
                
                rest_of_name = parts[1]
                tag = "SYSTEMDATE_" if "Tier 3" in method else ""
                
                new_name = f"{new_date}_{tag}{rest_of_name}"
                
                if new_name != f:
                    renames.append((filepath, root, new_name, method))

    print(f"\n--- Summary of Corrections ({len(renames)}) ---")
    for original_path, root, new_name, method in renames:
        print(f"[{method}] {original_path.name} -> {new_name}")
        
        if not args.dry_run:
            try:
                target = Path(root) / new_name
                original_path.rename(target)
            except Exception as e:
                print(f"Error renaming: {e}")

if __name__ == "__main__":
    main()
