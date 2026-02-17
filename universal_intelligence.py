
import os
import shutil
from datetime import datetime
from pathlib import Path
import config
import argparse

def get_file_metadata(filepath):
    """Extracts metadata for the file index."""
    stats = filepath.stat()
    size_mb = stats.st_size / (1024 * 1024)
    mod_time = datetime.fromtimestamp(stats.st_mtime).strftime(config.DATE_FORMAT)
    
    # Simple type check
    ext = filepath.suffix.lower()
    return f"{size_mb:.2f} MB", mod_time, ext

def generate_readme(folder_path):
    """Generates a standardized README.md for the given folder."""
    try:
        # Collect items
        items = list(folder_path.iterdir())
        files = [f for f in items if f.is_file() and f.name not in ["README.md", "Thumbs.db", ".DS_Store"]]
        subfolders = [d for d in items if d.is_dir() and d.name not in [".git", "__pycache__", "Archive"]]
        
        # Header
        lines = [
            config.README_HEADER,
            "",
            f"**Location:** `{folder_path.name}`",
            f"**Last Structure Audit:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 📂 Sub-Categories",
            "| Name | Description |",
            "|---|---|",
        ]

        # Subfolders Table
        if subfolders:
            for sub in sorted(subfolders, key=lambda x: x.name):
                lines.append(f"| [`{sub.name}`](./{sub.name}) | Sub-directory |")
        else:
            lines.append("| *None* | This is a leaf node. |")

        lines.extend([
            "",
            "## 📄 File Index",
            "| Date | File Name | Size | Type |",
            "|---|---|---|---|",
        ])

        # Files Table
        if files:
            for f in sorted(files, key=lambda x: x.name):
                size, date, ext = get_file_metadata(f)
                lines.append(f"| {date} | `{f.name}` | {size} | {ext} |")
        else:
            lines.append("| *None* | No loose files. | - | - |")

        # Write
        with open(folder_path / "README.md", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            
        return True
    except Exception as e:
        print(f"Error generating README for {folder_path}: {e}")
        return False

def scan_system(target_dir):
    """Recursively scans and documents the system."""
    target_path = Path(target_dir)
    print(f"Starting Universal Intelligence Scan on: {target_path}")
    
    count = 0
    for root, dirs, files in os.walk(target_path):
        current_path = Path(root)
        if ".git" in current_path.parts or "__pycache__" in current_path.parts:
            continue
            
        if generate_readme(current_path):
            print(f"   + Documented: {current_path.name}")
            count += 1
            
    print(f"--- Scan Complete. Generated {count} READMEs. ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Folder Intelligence Agent")
    parser.add_argument("--target", help="Target directory to document", required=False)
    args = parser.parse_args()
    
    target = args.target if args.target else config.DEFAULT_TARGET_DIR
    if os.path.exists(target):
        scan_system(target)
    else:
        print(f"Target directory not found: {target}")
