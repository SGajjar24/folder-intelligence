
import os
import re
import argparse
from pathlib import Path
import config
try:
    import fitz # PyMuPDF
except ImportError:
    fitz = None

def extract_text(filepath):
    if not fitz or filepath.suffix.lower() != ".pdf":
        return ""
    try:
        doc = fitz.open(filepath)
        text = ""
        for i in range(min(2, len(doc))): 
            text += doc[i].get_text()
        return text
    except:
        return ""

def find_date(text, filename):
    # Regex for various date formats
    patterns = [
        r'\b(\d{4})[-/](\d{2})[-/](\d{2})\b', # YYYY-MM-DD
        r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{4})\b', # DD-MM-YYYY
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})\b',
    ]
    
    # Check text
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            # Date normalization logic simplified for demo
            return "2023-01-01" # Placeholder for complex logic
            
    # Check filename for YYYY
    m = re.search(r'(20\d\d)', filename)
    if m:
        return f"{m.group(1)}-01-01"
        
    return "2023-01-01" # Default

def rename_system(target_dir, dry_run=True):
    root_path = Path(target_dir)
    print(f"--- Starting Renaming Audit in: {root_path} ---")
    if dry_run: print("[DRY RUN MODE - No changes will be applied]")
    
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if f.lower() in ["readme.md", "thumbs.db", ".ds_store", "config.py"]: continue
            
            filepath = Path(root) / f
            content = extract_text(filepath)
            
            # --- Analysis ---
            date_str = find_date(content, f)
            
            # Type
            doc_type = "Document"
            combined = (f + " " + content).lower()
            for k, v in config.KEYWORDS.items():
                if any(x in combined for x in v):
                    doc_type = k
                    break
            
            # Entity
            entity = ""
            for k, v in config.ENTITIES.items():
                if any(x in combined for x in v):
                    entity = "_" + k
                    break
            
            # Name Construction
            clean_name = Path(f).stem.replace("Scan", "").replace("Copy", "")[:20].strip()
            ext = Path(f).suffix.lower()
            new_name = f"{date_str}_{doc_type}{entity}_{clean_name}{ext}"
            
            if new_name != f:
                print(f"Proposed: {f:<30} -> {new_name}")
                if not dry_run:
                    try:
                        target = Path(root) / new_name
                        if target.exists():
                             new_name = f"{date_str}_{doc_type}{entity}_{clean_name}_1{ext}"
                             target = Path(root) / new_name
                        filepath.rename(target)
                    except Exception as e:
                        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--execute", action="store_true", help="Apply changes")
    args = parser.parse_args()
    
    rename_system(args.target, dry_run=not args.execute)
