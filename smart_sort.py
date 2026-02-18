
import os
import shutil
import re
from pathlib import Path

# Config
target_dir = r"C:\Users\sam\Desktop\02_Personal_Finance\KARANNAGAR CASE"
dry_run = False

# Heuristics
RULES = [
    # Top Priority: Specific Legal Cases
    {"pattern": r"115/2022|Civil Suit|RCS|Regular Civil Suit", "folder": "Legal_Proceedings/Civil_Suit_115_2022"},
    {"pattern": r"High Court|SCA|Special Civil Application", "folder": "Legal_Proceedings/High_Court"},
    
    # Second Priority: Sale Deeds (Dastavej)
    {"pattern": r"Sale Deed|Dastavej|Banakaht|Vechan", "folder": "Land_Records/Sale_Deeds"},
    
    # Third Priority: Maps
    {"pattern": r"Map|Naksha|Trace", "folder": "Land_Records/Maps"},
    
    # Fourth Priority: RTI
    {"pattern": r"RTI|Information|Mahiti", "folder": "RTI_And_Correspondence"},
    
    # Fifth Priority: Survey Number Specifics (if not caught above)
    # We check for these specifically to group loose records
    {"pattern": r"2304", "folder": "Land_Records/Survey_2304"},
    {"pattern": r"2306", "folder": "Land_Records/Survey_2306"},
    {"pattern": r"2313", "folder": "Land_Records/Survey_2313"},
    {"pattern": r"2397", "folder": "Land_Records/Survey_2397"},
    {"pattern": r"1200", "folder": "Land_Records/Survey_1200"},
    
    # Sixth: Revenue Records Generic
    {"pattern": r"7_12|7_no_uttara|8_A|Hakam|Entry|Nondh", "folder": "Land_Records/Revenue_Entries"},
    
    # Seventh: Media
    {"ext": [".mp3", ".mp4", ".m4a", ".wav", ".jpg", ".jpeg", ".png"], "folder": "Evidence/Multimedia"},
    
    # Fallback
    {"pattern": r".*", "folder": "Unsorted_Documents"} 
]

def clean_filename(name):
    # Remove excessive underscores or 'Copy' prefixes from previous runs
    name = name.replace("Copy of ", "").replace("Scan", "")
    name = re.sub(r'[_]+', '_', name)
    return name

def organize():
    print(f"--- Smart Sort for: {target_dir} ---")
    base = Path(target_dir)
    
    for root, dirs, files in os.walk(base, topdown=False):
        for f in files:
            if f.lower() in ["readme.md", "thumbs.db", ".ds_store", "desktop.ini"]: continue
            
            src = Path(root) / f
            
            # Identify Destination
            dest_folder = "Unsorted_Documents"
            
            # Check rules
            matched = False
            # Check patterns
            for rule in RULES:
                if "pattern" in rule:
                    if re.search(rule["pattern"], f, re.IGNORECASE):
                        dest_folder = rule["folder"]
                        matched = True
                        break
                elif "ext" in rule:
                    if src.suffix.lower() in rule["ext"]:
                        dest_folder = rule["folder"]
                        matched = True
                        break
            
            # Logic: If it matched a broad "Survey" rule but matches a more specific file type, maybe we combine?
            # For now, simplistic hierarchical logic is better than chaos.
            
            # Construct Target
            target_folder_path = base / dest_folder
            target_file = target_folder_path / clean_filename(f)
            
            # Check if we are moving the file to itself (or same folder)
            if src.parent == target_folder_path:
                continue
                
            print(f"[MOVE] {f} -> {dest_folder}/")
            
            if not dry_run:
                target_folder_path.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(src, target_file)
                except Exception as e:
                    print(f"  Error moving: {e}")

    # Cleanup empty dirs
    for root, dirs, files in os.walk(base, topdown=False):
        for d in dirs:
            dir_path = Path(root) / d
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"Removed empty dir: {d}")
            except:
                pass

if __name__ == "__main__":
    organize()
