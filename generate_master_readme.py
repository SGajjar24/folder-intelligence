
import os
from pathlib import Path
from datetime import datetime

target_dir = r"C:\Users\sam\Desktop\02_Personal_Finance\KARANNAGAR CASE"

header = """# 📂 Karannagar Land Case - Master Index

**Location:** `Karannagar, Kadi, Mehsana`  
**Generated:** {date}

This repository contains legal proceedings, land records, and evidence regarding the land disputes in Karannagar.

## 🏗 Directory Structure
"""

def generate_index():
    base = Path(target_dir)
    structure_md = []
    file_index_md = []
    
    file_index_md.append("\n## 📑 Detailed File Index\n")
    file_index_md.append("| Category | File Name | Type |")
    file_index_md.append("|---|---|---|")
    
    # Walk for structure
    for root, dirs, files in os.walk(base):
        level = root.replace(str(base), '').count(os.sep)
        indent = ' ' * 4 * (level)
        rel_path = root.replace(str(base), '')
        if rel_path.startswith(os.sep): rel_path = rel_path[1:]
        folder_name = os.path.basename(root)
        
        if folder_name in [".git", "__pycache__"] or folder_name == base.name:
            continue
            
        structure_md.append(f"{indent}- **📂 {folder_name}/**")
        
        # Add files to structure (optional, maybe too verbose, let's keep structure high level)
        # Add files to Table
        sub_files = [f for f in files if f.lower() not in ["readme.md", "desktop.ini"]]
        for f in sub_files:
            cat = rel_path if rel_path else "Root"
            file_index_md.append(f"| {cat} | [{f}](./{rel_path.replace(os.sep, '/')}/{f}) | {Path(f).suffix} |")

    with open(base / "README.md", "w", encoding="utf-8") as f:
        f.write(header.format(date=datetime.now().strftime("%Y-%m-%d")))
        f.write("\n".join(structure_md))
        f.write("\n")
        f.write("\n".join(file_index_md))
        
    print(f"Master README generated at {base / 'README.md'}")

if __name__ == "__main__":
    generate_index()
