
import os
import shutil
import sys
from pathlib import Path

# Import tool functions
import universal_declutter
import universal_namer
import universal_dedupe
import universal_intelligence

source_dir = r"C:\Users\sam\Desktop\02_Personal_Finance\Karannagar Land case"
dest_dir = r"C:\Users\sam\Desktop\02_Personal_Finance\KARANNAGAR CASE"

def main():
    print(f"--- Starting Optimization Wrapper ---")
    
    # 1. Copy Files
    if os.path.exists(dest_dir):
        print(f"Destination exists. Cleaning up specific files if needed or starting fresh?")
        # For safety, let's just copy over. If it exists, shutil.copytree fails.
        # We'll use dirs_exist_ok=True
        pass
    
    print(f"Copying '{source_dir}' to '{dest_dir}'...")
    try:
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        print("Copy complete.")
    except Exception as e:
        print(f"Copy failed: {e}")
        return

    # 2. Run Tools
    print("\n--- Stage 2: Declutter ---")
    universal_declutter.declutter_system(dest_dir, dry_run=False)
    
    print("\n--- Stage 3: Rename ---")
    universal_namer.rename_system(dest_dir, dry_run=False)
    
    print("\n--- Stage 4: Dedupe ---")
    # Note: universal_dedupe might require 'delete' arg or similar. 
    # Checking import: find_duplicates(target_dir, delete=False)
    universal_dedupe.find_duplicates(dest_dir, delete=True)
    
    print("\n--- Stage 5: Document ---")
    universal_intelligence.scan_system(dest_dir)
    
    print("\n--- Optimization Complete ---")

if __name__ == "__main__":
    main()
