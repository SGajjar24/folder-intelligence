import os
import shutil
import re
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract

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

class UniversalOrganizer:
    def __init__(self, target_dir, config_path, dry_run=True):
        self.target_dir = Path(target_dir).resolve()
        self.dry_run = dry_run
        self.stats = {"scanned": 0, "moved": 0, "errors": 0}
        
        # Load Config
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.categories = self.config.get("categories", {})
        self.blocked_dirs = [Path(p).resolve() for p in self.config.get("blocked_dirs", [])]

    def validate_safety(self):
        """Ensures we aren't running on a system directory."""
        if not self.target_dir.exists():
            print(f"Error: Directory not found: {self.target_dir}")
            sys.exit(1)

        # Check against blocked dirs
        for blocked in self.blocked_dirs:
            # Check if target is blocked or a parent of blocked (to avoid C:\Users accident)
            # Actually, we want to prevent running ON C:\Users, but C:\Users\Sam\Desktop is fine.
            if self.target_dir == blocked or blocked in self.target_dir.parents:
                 # If target is PARENT of blocked (e.g. running on C:\), that's bad.
                 # If target IS blocked (e.g. running on C:\Windows), that's bad.
                 # If blocked is parent (e.g. C:\Users is parent of C:\Users\Sam...), that's usually OK unless strictly blocked.
                 pass

        # Strict check: Don't run on C:\ directly or C:\Windows
        if str(self.target_dir).lower() in [str(p).lower() for p in self.blocked_dirs]:
            print(f"SAFETY ERROR: Usage on {self.target_dir} is blocked by configuration.")
            sys.exit(1)
            
        print(f"Target: {self.target_dir}")
        print(f"Mode: {'DRY RUN (Safe)' if self.dry_run else 'LIVE EXECUTION'}")
        
    def get_file_content(self, filepath):
        """Extracts text from PDF/Image."""
        text = ""
        ext = filepath.suffix.lower()
        try:
            if ext in [".mp3", ".mp4", ".wav", ".m4a"]:
                return filepath.name.lower()
            if ext == ".pdf":
                doc = fitz.open(filepath)
                for page in doc:
                    text += page.get_text()
                    if len(text) > 200: break
                if len(text.strip()) < 50 and OCR_AVAILABLE:
                    page = doc.load_page(0)
                    pix = page.get_pixmap(dpi=200)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    text = pytesseract.image_to_string(img, lang='eng+guj', config=TESSDATA_CONFIG)
            elif ext in [".jpg", ".png", ".jpeg"] and OCR_AVAILABLE:
                img = Image.open(filepath)
                text = pytesseract.image_to_string(img, lang='eng+guj', config=TESSDATA_CONFIG)
        except Exception as e:
            pass # Silent fail on read
        return (text + " " + filepath.name).lower()

    def find_best_date(self, text, filepath):
        patterns = [r'\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b', r'\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})\b']
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
        ts = filepath.stat().st_mtime
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d"), "System"

    def determine_category(self, text):
        best_cat = "99_Unsorted"
        max_score = 0
        
        # Check specific media category first if exists
        media_cat = next((c for c in self.categories if "Media" in c), None)
        if media_cat and any(ext in text for ext in self.categories[media_cat]):
             return media_cat

        for cat, keywords in self.categories.items():
            if cat == "99_Unsorted" or (media_cat and cat == media_cat): continue
            score = sum(1 for k in keywords if k in text)
            if score > max_score:
                max_score = score
                best_cat = cat
        return best_cat

    def clean_name(self, filename):
        return re.sub(r'^\d{4}-\d{2}-\d{2}[_ -]', '', filename)

    def run(self):
        self.validate_safety()
        
        # Confirmation for live run
        if not self.dry_run:
            confirm = input(f"WARNING: You are about to organize contents of {self.target_dir}. Continue? (y/n): ")
            if confirm.lower() != 'y':
                print("Aborted.")
                sys.exit(0)

        moves = []
        all_files = []
        
        # Collect files
        for r, d, f in os.walk(self.target_dir):
            for file in f:
                if file.lower() in ["readme.md", "thumbs.db", ".ds_store"]: continue
                all_files.append(Path(r) / file)

        print(f"Processing {len(all_files)} files...")

        for i, filepath in enumerate(all_files):
            self.stats["scanned"] += 1
            if i % 5 == 0: print(f"  Scanned {i}/{len(all_files)}...", end="\r")
            
            text = self.get_file_content(filepath)
            date_str, source = self.find_best_date(text, filepath)
            category = self.determine_category(text)
            
            clean_name = self.clean_name(filepath.name)
            tag = ""
            if source == "System" and filepath.suffix.lower() in [".pdf", ".docx"]:
                tag = "_SYSTEMDATE_"
                
            new_name = f"{date_str}{tag}_{clean_name}"
            # Clean duplicate tags
            new_name = new_name.replace("_SYSTEMDATE__SYSTEMDATE_", "_SYSTEMDATE_")
            
            target_path = self.target_dir / category / new_name

            if filepath != target_path:
                moves.append((filepath, target_path, category))
        
        print(f"\nAnalysis Complete. Found {len(moves)} necessary moves.")
        
        for src, dst, cat in moves:
            if self.dry_run:
                print(f"[DRY RUN] Move: {src.name} -> {cat}/{dst.name}")
            else:
                try:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    # Handle Name Collision
                    if dst.exists() and src != dst:
                        stem = dst.stem
                        suffix = dst.suffix
                        counter = 1
                        while dst.exists():
                            dst = dst.parent / f"{stem}_{counter}{suffix}"
                            counter += 1
                            
                    shutil.move(str(src), str(dst))
                    self.stats["moved"] += 1
                    print(f"[OK] Moved: {dst.name}")
                except Exception as e:
                    print(f"[ERROR] Failed {src.name}: {e}")
                    self.stats["errors"] += 1

        # Clean Empty
        if not self.dry_run:
            for r, d, f in os.walk(self.target_dir, topdown=False):
                p = Path(r)
                if p == self.target_dir: continue
                if not any(p.iterdir()):
                    try: p.rmdir()
                    except: pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Folder Organizer (OCR & Smart Sort)")
    parser.add_argument("target", help="Directory to organize")
    parser.add_argument("--config", default="default_config.json", help="Path to categories.json")
    parser.add_argument("--execute", action="store_true", help="Perform actual moves (default is Dry Run)")
    
    args = parser.parse_args()
    
    organizer = UniversalOrganizer(args.target, args.config, dry_run=not args.execute)
    organizer.run()
