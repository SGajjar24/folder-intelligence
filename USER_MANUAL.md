# 📖 Folder Intelligence: User Manual

## 👋 Welcome
Welcome to Folder Intelligence, your personal digital librarian. This guide will walk you through setting up and running the system to organize your files.

## 🛠 Prerequisites
1.  **Python**: Ensure Python 3.9 or higher is installed. [Download Here](https://www.python.org/downloads/)
2.  **Files**: Have a chaotic folder ready (e.g., "Downloads", "Old Desktop").

## ⚙️ Configuration (The Brain)
Open `config.py` in a text editor (Notepad, VS Code).
This file controls how the AI thinks.

### Important Settings to Change:
-   **ENTITIES**: Add names of your clients, vendors, or departments.
    ```python
    ENTITIES = {
        "Globex_Corp": ["globex corporation", "globex"],
        "Client_Acme": ["acme corp", "project x"],
    }
    ```
-   **KEYWORDS**: Add words that identify your document types.
    ```python
    KEYWORDS = {
        "Invoice": ["invoice", "receipt", "bill"],
        "Contract": ["agreement", "nda", "sign"],
    }
    ```

## 🚀 Step-by-Step Usage

### Step 1: The Audit (Safe Mode)
Run this command to see a "Health Check" of your folder. It won't change anything.
```bash
python universal_intelligence.py --target "D:/My_Files"
```
**Result:** Check the new `README.md` files generated inside your folders. They will show you what's there.

### Step 2: The Cleanup (Dry Run)
Identify loose files that need a home.
```bash
python universal_declutter.py --target "D:/My_Files"
```
**Result:** It will print "Proposed Move: invoice.pdf -> Financial/". If it looks good, run with `--execute`.

### Step 3:The Rename (The Magic)
This is where files get smart names.
```bash
python universal_namer.py --target "D:/My_Files"
```
**Result:** It will print "Proposed Rename: Scan001.pdf -> 2023-01-01_Invoice_Acme.pdf".
**Action:** Review the list carefully! If satisfied, run with `--execute`.

### Step 4: The Dedupe (The Deep Clean)
Remove exact copies.
```bash
python universal_dedupe.py --target "D:/My_Files" --delete
```
**Warning:** This permanently deletes duplicates. Ensure you have a backup first.

## ❓ FAQ

**Q: Will this delete my data?**
A: Only the `universal_dedupe.py` script deletes files, and only if they are *exact* mathematical duplicates (SHA-256 hash match).

**Q: Can I undo the renaming?**
A: Currently, there is no automatic undo. Use the "Dry Run" mode first to be safe.

**Q: What is a "Dry Run"?**
A: It means the script simulates the action and prints what *would* happen, without actually changing any files.
