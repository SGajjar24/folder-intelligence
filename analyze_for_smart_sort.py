
import os
import fitz  # PyMuPDF
from pathlib import Path
import json

target_dir = r"C:\Users\sam\Desktop\02_Personal_Finance\KARANNAGAR CASE"
output_file = r"C:\Users\sam\.gemini\antigravity\scratch\Universal_Folder_Optimization\content_dump.json"

def extract_text(filepath):
    """Extracts text from PDF or returns basic info for others."""
    try:
        if filepath.suffix.lower() == ".pdf":
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            return text[:2000] # Cap to 2000 chars to avoid huge context usage
        elif filepath.suffix.lower() in [".txt", ".md", ".py", ".json", ".xml", ".html", ".css", ".js"]:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return f.read(2000)
            except:
                return "[Text read error]"
        else:
            return f"[Binary/Unsupported Type: {filepath.suffix}]"
    except Exception as e:
        return f"[Extraction Error: {e}]"

def analyze_folder():
    data = []
    print(f"Scanning {target_dir}...")
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            if f in ["README.md", "thumbs.db", ".DS_Store"]: continue
            
            filepath = Path(root) / f
            print(f"Reading {f}...")
            content = extract_text(filepath)
            
            data.append({
                "filename": f,
                "current_path": str(filepath),
                "content_snippet": content,
                "extension": filepath.suffix.lower()
            })
            
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Analysis complete. Saved to {output_file}")

if __name__ == "__main__":
    analyze_folder()
