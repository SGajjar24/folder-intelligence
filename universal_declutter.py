
import os
import shutil
from pathlib import Path
import config
import argparse

def declutter_system(target_dir, dry_run=True):
    root_path = Path(target_dir)
    print(f"--- Starting Declutter Audit in: {root_path} ---")
    if dry_run: print("[DRY RUN MODE - No changes will be applied]")
    
    for item in root_path.iterdir():
        if item.is_file() and item.name not in ["README.md", "config.py", ".DS_Store"]:
            # Categorize
            category = "Uncategorized"
            fname_lower = item.name.lower()
            
            # Check Config Keywords
            for cat, keywords in config.KEYWORDS.items():
                if any(k in fname_lower for k in keywords):
                    category = cat
                    break
            
            # Check Extensions if no keyword match
            if category == "Uncategorized":
                for cat, exts in config.FILE_EXTENSIONS.items():
                    if item.suffix.lower() in exts:
                        category = cat
                        break
            
            target_folder = root_path / category
            print(f"Propsoed Move: {item.name} -> {category}/")
            
            if not dry_run:
                target_folder.mkdir(exist_ok=True)
                try:
                    shutil.move(item, target_folder / item.name)
                except Exception as e:
                    print(f"Error moving {item.name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--execute", action="store_true", help="Apply changes")
    args = parser.parse_args()
    
    declutter_system(args.target, dry_run=not args.execute)
