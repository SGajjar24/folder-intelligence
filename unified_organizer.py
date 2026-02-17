
import os
import shutil
import re
import argparse
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract

# --- Configuration ---
TARGET_DIR = r"C:\Users\sam\Desktop\02_Personal_Finance\KARANNAGAR CASE"

# 1. Definitive Category Map (Priority Order)
CATEGORIES = {
    "01_Legal_Proceedings": [
        "court", "order", "judgement", "petition", "affidavit", "vakilatnama", "summon", "notice",
        "દસ્તાવેજ", "રજીસ્ટર", "નોટીસ", "કેસ", "civil", "advocate", "high court"
    ],
    "02_Land_Records": [
        "7/12", "૮-અ", "હુકમ", "7-12", "village form", "pani patrak", "mutation", "ferfar", "khedut",
        "૭/૧૨", "form no", "revenue", "mamlatdar", "collector"
    ],
    "03_Sale_Deeds": [
        "sale deed", "banakhat", "vechan", "dastavej", "index 2", "registered", "વેચાણ", "ખરીદ"
    ],
    "04_Maps_and_Technicals": [
        "map", "naksha", "plan", "survey", "sketch", "site plan", "measurement", "નકશા", "drawings", "t.p."
    ],
    "05_Correspondence_RTI": [
        "rti", "letter", "application", "reply", "inward", "outward", "post", "mail", "અરજી", "જવાબ"
    ],
    "06_Evidence_Media": [
        ".mp3", ".mp4", ".wav", ".m4a", ".mov", ".avi", "recording", "call", "transcript"
    ],
    "99_Unsorted": []
}

# --- OCR Setup ---
OCR_AVAILABLE = False
try:
    potentials = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.getenv('LOCALAPPDATA', ''), r'Programs\Tesseract-OCR\tesseract.exe')
    ]
    for p in potentials:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            OCR_AVAILABLE = True
            break
            
    local_tessdata = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tessdata")
    TESSDATA_CONFIG = f'--tessdata-dir {local_tessdata}' if os.path.exists(local_tessdata) else ""
except:
    pass

# --- Helper Functions ---

def get_file_content(filepath):
    """Extracts text from PDF/Image using PyMuPDF or Tesseract."""
    text = ""
    ext = filepath.suffix.lower()
    
    try:
        # Media Handling (Filename only)
        if ext in [".mp3", ".mp4", ".wav", ".m4a"]:
            return filepath.name.lower()

        # PDF Handling
        if ext == ".pdf":
            doc = fitz.open(filepath)
            # Try text layer
            for page in doc:
                text += page.get_text()
                if len(text) > 200: break
            
            # If text layer empty, OCR first page
            if len(text.strip()) < 50 and OCR_AVAILABLE:
                page = doc.load_page(0)
                pix = page.get_pixmap(dpi=200)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                text = pytesseract.image_to_string(img, lang='eng+guj', config=TESSDATA_CONFIG)
        
        # Image Handling
        elif ext in [".jpg", ".png", ".jpeg"] and OCR_AVAILABLE:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img, lang='eng+guj', config=TESSDATA_CONFIG)
            
    except Exception as e:
        print(f"  [Read Error] {filepath.name}: {e}")
        
    return (text + " " + filepath.name).lower()

def clean_date_from_filename(filename):
    """Removes existing date prefix if present."""
    # Matches YYYY-MM-DD_ or YYYY-MM-DD- etc.
    return re.sub(r'^\d{4}-\d{2}-\d{2}[_ -]', '', filename)

def find_best_date(text, filepath):
    """Tier 1-3 Date Finding Logic."""
    # A. Check for date in text using Regex (Tier 1 & 2)
    patterns = [
        r'\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b', # YYYY-MM-DD
        r'\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})\b', # DD-MM-YYYY
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            g1, g2, g3 = m.groups()
            try:
                if len(g1) == 4: y, m, d = g1, g2, g3
                else: d, m, y = g1, g2, g3
                
                dt = datetime(int(y), int(m), int(d))
                if 1900 < dt.year < 2100:
                    return dt.strftime("%Y-%m-%d"), "Content"
            except: pass

    # B. Tier 3: System Date (Modified Time)
    ts = filepath.stat().st_mtime
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d"), "System"

def determine_category(text):
    """Scores text against categories."""
    best_cat = "99_Unsorted"
    max_score = 0
    
    # Check media extensions first
    if any(ext in text for ext in CATEGORIES["06_Evidence_Media"]):
         return "06_Evidence_Media"

    for cat, keywords in CATEGORIES.items():
        if cat == "99_Unsorted" or cat == "06_Evidence_Media": continue
        score = sum(1 for k in keywords if k in text)
        if score > max_score:
            max_score = score
            best_cat = cat
            
    return best_cat

def unified_organize(dry_run=False):
    root = Path(TARGET_DIR)
    moves = []
    
    print(f"Scanning {root}...")
    
    # 1. Collect all files (flattening)
    all_files = []
    for r, d, f in os.walk(root):
        for file in f:
            if file.lower() == "readme.md": continue
            all_files.append(Path(r) / file)
            
    print(f"Found {len(all_files)} files. Processing...")
    
    # 2. Process Each File
    for i, filepath in enumerate(all_files):
        print(f"[{i+1}/{len(all_files)}] Processing: {filepath.name}")
        
        # A. Analyze Content
        text = get_file_content(filepath)
        
        # B. Find Date
        date_str, source = find_best_date(text, filepath)
        
        # C. Determine Category
        category = determine_category(text)
        
        # D. Construct New Name/Path
        clean_name = clean_date_from_filename(filepath.name)
        
        # Add tag if System Date was used for a document that *should* have a date
        tag = ""
        is_doc = filepath.suffix.lower() in [".pdf", ".docx"]
        if source == "System" and is_doc:
             tag = "_SYSTEMDATE_"
             
        new_filename = f"{date_str}{tag}_{clean_name}"
        
        # Avoid double-tagging if script runs multiple times
        if "_SYSTEMDATE__SYSTEMDATE_" in new_filename:
            new_filename = new_filename.replace("_SYSTEMDATE__SYSTEMDATE_", "_SYSTEMDATE_")
            
        target_path = root / category / new_filename
        
        # Record Move
        if filepath != target_path:
            moves.append((filepath, target_path, category))
            print(f"  -> Plan: {category} | {new_filename}")

    # 3. Execute Moves
    print(f"\n--- Execution Summary ({len(moves)} moves) ---")
    if dry_run:
        print("[Dry Run] No changes made.")
    else:
        for src, dst, cat in moves:
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
            except Exception as e:
                print(f"Error moving {src.name}: {e}")
                
        # 4. Cleanup Empty Folders
        print("\nCleaning up empty folders...")
        for r, d, f in os.walk(root, topdown=False):
            p = Path(r)
            if p == root: continue
            if not any(p.iterdir()):
                try:
                    p.rmdir() 
                    print(f"Deleted empty: {p.relative_to(root)}")
                except: pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution")
    args = parser.parse_args()
    
    unified_organize(dry_run=args.dry_run)
