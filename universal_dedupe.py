
import os
import hashlib
from pathlib import Path
import argparse

def get_hash(filepath):
    try:
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None

def find_duplicates(target_dir, delete=False):
    root_path = Path(target_dir)
    print(f"--- Starting Deduplication Scan in: {root_path} ---")
    if not delete: print("[DRY RUN MODE - No files will be deleted]")
    
    hashes = {}
    duplicates = []
    
    count = 0
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if f in ["README.md", "config.py"]: continue
            
            filepath = Path(root) / f
            file_hash = get_hash(filepath)
            
            if file_hash:
                if file_hash in hashes:
                    original = hashes[file_hash]
                    duplicates.append((filepath, original))
                    print(f"Duplicate Found: {f} (Matches {original.name})")
                    
                    if delete:
                        try:
                            # Archive logic could be added here
                            filepath.unlink() 
                            print(f"   Deleted: {f}")
                        except Exception as e:
                            print(f"   Error deleting: {e}")
                else:
                    hashes[file_hash] = filepath
            count += 1
            if count % 100 == 0: print(f"Scanned {count} files...")

    print(f"Scan Complete. Found {len(duplicates)} duplicates.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--delete", action="store_true", help="Delete duplicates")
    args = parser.parse_args()
    
    find_duplicates(args.target, delete=args.delete)
