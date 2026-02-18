
import os
import shutil
import argparse
from pathlib import Path
import config

def deep_cleanup(target_dir, dry_run=False):
    target_path = Path(target_dir)
    print(f"Scanning {target_path} for empty folders...")
    
    # Walk bottom-up to handle nested empty folders
    for root, dirs, files in os.walk(target_path, topdown=False):
        current_path = Path(root)
        
        # Skip root and special folders
        if current_path == target_path: continue
        if ".git" in str(current_path) or "__pycache__" in str(current_path): continue
        
        # Check for visible files (ignoring README.md and system files)
        ignored = ["readme.md", "thumbs.db", ".ds_store", "desktop.ini"]
        visible_files = [f for f in files if f.lower() not in ignored]
        
        # Check for visible subdirectories
        # Since we walk bottom-up, if a subdir was empty, it might have been deleted already (in actual run)
        # In dry-run, we just check if it has entries.
        # But os.walk lists dirs present at start of iteration. 
        # We need to check if they still exist.
        visible_subdirs = [d for d in dirs if (current_path / d).exists()]
        
        if not visible_files and not visible_subdirs:
            print(f"[Delete Candidate] {current_path.relative_to(target_path)}")
            
            if not dry_run:
                try:
                    # Remove README if it exists
                    readme_path = current_path / "README.md"
                    if readme_path.exists():
                        os.remove(readme_path)
                    
                    # Remove directory
                    current_path.rmdir()
                    print(f"  -> Deleted: {current_path.name}")
                except Exception as e:
                    print(f"  -> Error deleting {current_path.name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help=" Simulate cleanup")
    args = parser.parse_args()
    
    target = r"C:\Users\sam\Desktop\02_Personal_Finance\KARANNAGAR CASE"
    deep_cleanup(target, dry_run=args.dry_run)
