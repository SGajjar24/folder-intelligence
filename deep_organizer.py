
import os
import shutil
import argparse
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract
import config

# --- OCR Setup ---
OCR_AVAILABLE = False
try:
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
        print(f"Tesseract found: {tess_path}")
    else:
        print("Warning: Tesseract not found.")

except Exception as e:
    print(f"OCR Setup Error: {e}")

# --- Keyword Extensions for Karannagar ---
# Adding specific Hindi/Gujarati terms
EXTENDED_KEYWORDS = config.KEYWORDS.copy()

# Initialize specific categories if not present
for cat in ["Land_Records", "Sale_Deeds", "Maps"]:
    if cat not in EXTENDED_KEYWORDS:
        EXTENDED_KEYWORDS[cat] = []

EXTENDED_KEYWORDS["Land_Records"].extend([
    "7/12", "૮-અ", "હુકમ", "7-12", "village form", "pani patrak", "mutation", "ferfar", "khedut"
])
EXTENDED_KEYWORDS["Legal"].extend([
    "court", "order", "judgement", "petition", "affidavit", "vakilatnama", "summon", "notice",
    "દસ્તાવેજ", "રજીસ્ટર", "નોટીસ", "કેસ"
])
EXTENDED_KEYWORDS["Sale_Deeds"].extend([
    "sale deed", "banakhat", "vechan", "dastavej", "index 2", "registered"
])
EXTENDED_KEYWORDS["Maps"].extend([
    "map", "naksha", "plan", "survey", "sketch", "site plan", "નકશા"
])


def ocr_scan(filepath):
    text = ""
    try:
        if filepath.suffix.lower() == ".pdf":
            doc = fitz.open(filepath)
            # Check text layer first
            for page in doc:
                text += page.get_text()
                if len(text) > 500: break # Enough text found
            
            # If little text, try OCR on first page
            if len(text.strip()) < 50 and OCR_AVAILABLE:
                page = doc.load_page(0)
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                text = pytesseract.image_to_string(img, lang='eng+guj', config=tessdata_config)
                
        elif filepath.suffix.lower() in [".jpg", ".png", ".jpeg"]:
            if OCR_AVAILABLE:
                img = Image.open(filepath)
                text = pytesseract.image_to_string(img, lang='eng+guj', config=tessdata_config)
                
    except Exception as e:
        print(f"Error scanning {filepath.name}: {e}")
        
    return text.lower()

def categorize_content(text):
    scores = {category: 0 for category in EXTENDED_KEYWORDS}
    
    for category, keywords in EXTENDED_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                scores[category] += 1
                
    # Get best match
    best_category = max(scores, key=scores.get)
    if scores[best_category] > 0:
        return best_category
    return None

def deep_organize(target_dir, dry_run=False):
    root = Path(target_dir)
    # Folders to scan
    scan_folders = ["Unsorted_Documents", "Uncategorized", "Unsorted"]
    
    moves = []
    
    for folder_name in scan_folders:
        folder_path = root / folder_name
        if not folder_path.exists(): continue
        
        print(f"Scanning {folder_name}...")
        
        for file in folder_path.glob("*"):
            if file.is_dir() or file.name.lower() == "readme.md": continue
            
            print(f"  > Analyzing: {file.name}")
            text = ocr_scan(file)
            category = categorize_content(text)
            
            if category:
                dest = root / category
                moves.append((file, dest / file.name, category))
                print(f"    -> Identified as: {category}")
            else:
                print(f"    -> Could not identify.")

    print(f"\n--- Summary of Moves ({len(moves)}) ---")
    for src, dst, cat in moves:
        print(f"[{cat}] {src.name} -> {dst.parent.name}/")
        
        if not dry_run:
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
            except Exception as e:
                print(f"Error moving {src.name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Simulate moves")
    args = parser.parse_args()
    
    # Reload config to get base dir if needed, or hardcode for safety given prior issues
    target = r"C:\Users\sam\Desktop\02_Personal_Finance\KARANNAGAR CASE"
    deep_organize(target, dry_run=args.dry_run)
