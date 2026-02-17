<p align="center">
  <h1 align="center">🧠 Folder Intelligence</h1>
  <p align="center"><strong>The Complete File System Optimization Pipeline</strong></p>
  <p align="center">Audit → Declutter → Rename → Deduplicate → Document — in one toolkit.</p>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black"></a>
  <img src="https://img.shields.io/badge/AI_Model-None_Required-brightgreen" alt="No AI Model Required">
  <img src="https://img.shields.io/badge/dedupe-SHA--256-blueviolet" alt="SHA-256 Deduplication">
</p>

---

> **"Other tools organize files. We build self-documenting, enterprise-grade archives."**

---

## ⚡ How It Works

**Before:**
```
D:/Company_Archive/
├── Scan0001.pdf
├── budget_final_FINAL_v3.xlsx
├── IMG_20231015.jpg
├── meeting notes oct.docx
├── Scan0001 (1).pdf          ← duplicate
├── NDA_acme_signed.pdf
├── random.txt
├── invoice_sept.pdf
├── Q3_report_draft.pptx
├── old_budget.xlsx
└── receipt_lunch.jpg

0 directories, 11 files
```

**After:**
```
D:/Company_Archive/
├── README.md                                    ← auto-generated index
├── Contracts/
│   ├── README.md
│   └── 2023-10-15_Contract_Acme_Corp_NDA.pdf
├── Financial/
│   ├── README.md
│   ├── 2023-09-01_Invoice_September.pdf
│   ├── 2023-10-01_Report_Q3_Draft.pptx
│   └── 2023-01-01_Financial_Budget_v3.xlsx
├── Images/
│   ├── README.md
│   ├── 2023-10-15_Photo_Office.jpg
│   └── 2023-09-15_Receipt_Lunch.jpg
└── Correspondence/
    ├── README.md
    └── 2023-10-01_Correspondence_Meeting_Notes.docx

4 directories, 11 files (1 duplicate removed, 11 READMEs generated)
```

> ✅ Every folder has a `README.md` — your file system is now a **browsable wiki**.

---

## 🏆 Why Folder Intelligence?

Most file organizers do **one thing**. We do **five**.

| Feature | Folder Intelligence | Local-File-Organizer | classifier | rmlint |
|---|:---:|:---:|:---:|:---:|
| Smart Categorization | ✅ | ✅ | ✅ | ❌ |
| Content-Aware Renaming | ✅ (Regex + PDF) | ✅ (LLM) | ❌ | ❌ |
| Forensic Deduplication | ✅ SHA-256 | ❌ (Roadmap) | ❌ | ✅ |
| Auto-Documentation | ✅ Per-folder READMEs | ❌ | ❌ | ❌ |
| Enterprise SOP | ✅ ISO 8601, Governance | ❌ | ❌ | ❌ |
| Requires AI Model | ❌ **None** | ⚠️ 3GB Llama | ❌ | ❌ |
| Full Pipeline | ✅ 5-stage | Partial | Partial | Partial |

> **Key Insight:** We are the **only** tool that combines all five stages into one pipeline AND ships with enterprise governance documentation.

---

## 🛠 The 5-Stage Pipeline

```mermaid
graph LR
    A["📥 Raw Chaos"] --> B["🔍 Stage 1: Audit"]
    B --> C["📂 Stage 2: Declutter"]
    C --> D["✏️ Stage 3: Rename"]
    D --> E["🕵️ Stage 4: Dedupe"]
    E --> F["📖 Stage 5: Document"]
    F --> G["✨ Pristine Archive"]

    style A fill:#ff6b6b,color:#fff
    style G fill:#51cf66,color:#fff
    style B fill:#339af0,color:#fff
    style C fill:#339af0,color:#fff
    style D fill:#339af0,color:#fff
    style E fill:#339af0,color:#fff
    style F fill:#339af0,color:#fff
```

| Stage | Tool | What It Does |
|---|---|---|
| **1. Audit** | `universal_intelligence.py` | Recursively maps your file system, generates `README.md` indexes |
| **2. Declutter** | `universal_declutter.py` | Moves loose files into logical category folders |
| **3. Rename** | `universal_namer.py` | Reads PDF content to extract dates/entities, applies `YYYY-MM-DD_Type_Entity` standard |
| **4. Dedupe** | `universal_dedupe.py` | SHA-256 hash comparison — finds exact duplicates regardless of filename |
| **5. Document** | `universal_intelligence.py` | Regenerates READMEs to reflect the final, clean state |

---

## 🚀 Quick Start

### 1. Install
```bash
git clone https://github.com/SGajjar24/folder-intelligence.git
cd folder-intelligence
pip install -r requirements.txt   # Only dependency: PyMuPDF
```

### 2. Configure
Edit `config.py` to define your domain:
```python
KEYWORDS = {
    "Invoice": ["invoice", "receipt", "bill"],
    "Contract": ["agreement", "nda", "sow"],
}
ENTITIES = {
    "Globex_Corp": ["globex", "globex inc"],
    "Client_Acme": ["acme corp", "acme"],
}
```

### 3. Run (Safe Mode First)
```bash
# Stage 1: See what you have (generates READMEs, changes nothing else)
python universal_intelligence.py --target "/path/to/messy/folder"

# Stage 2-3: Preview proposed changes (Dry Run — no files modified)
python universal_declutter.py --target "/path/to/messy/folder"
python universal_namer.py --target "/path/to/messy/folder"

# Stage 4: Find duplicates (Dry Run — no files deleted)
python universal_dedupe.py --target "/path/to/messy/folder"
```

### 4. Execute
```bash
# When you're satisfied with the proposals:
python universal_declutter.py --target "/path/to/messy/folder" --execute
python universal_namer.py --target "/path/to/messy/folder" --execute
python universal_dedupe.py --target "/path/to/messy/folder" --delete
```

> 📖 **Need more help?** See the complete [`USER_MANUAL.md`](USER_MANUAL.md) for detailed step-by-step instructions with examples, configuration tips, and FAQ.

---

## 🏗 Tech Stack

| Component | Technology | Why |
|---|---|---|
| **Core** | Python 3.9+ | Cross-platform, no compilation |
| **PDF Analysis** | PyMuPDF (`fitz`) | 10x faster than alternatives, no Java dependency |
| **Hashing** | SHA-256 (`hashlib`) | Collision-resistant, industry standard |
| **File Ops** | `pathlib` + `shutil` | Native OS integration |
| **AI Model** | **None Required** | Zero setup, instant execution |

---

## 📜 Enterprise SOP (Standard Operating Procedures)

This project ships with formal governance documentation:

| Rule | Description |
|---|---|
| **Zero-Clutter Policy** | No folder shall contain >10 loose files |
| **ISO 8601 Naming** | `YYYY-MM-DD` is the only acceptable date format |
| **Hash-Based Truth** | Never delete based on name alone — verify SHA-256 |
| **Self-Documentation** | Every directory must contain a `README.md` |
| **3-Click Rule** | Any file reachable within 3 clicks from root |

See [`SOP.md`](SOP.md) for full enterprise use cases (M&A, Legal Discovery, DAM Audit).

---

## ✍️ Author

**Swetang Gajjar**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Swetang_Gajjar-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/gajjarswetang/)
[![Email](https://img.shields.io/badge/Email-gajjarswetang%40gmail.com-red?style=flat&logo=gmail)](mailto:gajjarswetang@gmail.com)

---

## 🔮 Future Scope

This project is actively evolving. Here's what has been shipped and what's on the horizon:

**✅ Shipped:**
- Content-aware PDF renaming (Regex + PyMuPDF)
- SHA-256 forensic deduplication
- Auto-generated per-folder README documentation
- Enterprise SOP and governance framework
- Configurable keyword/entity engine
- Dry-run mode for all operations

**🔜 Future Enhancements (Under Exploration):**
- GUI dashboard for non-technical users
- OCR support for scanned image documents
- Undo/rollback system with rename logging
- Watch mode (auto-organize new files in real-time)
- Docker container for server-side deployment
- Plugin architecture for custom classification rules
- Multi-language content analysis
- Cloud storage integration (S3, GCS, Azure Blob)

> 💡 **Interested in contributing or enhancing this project?** I'm actively working on the future scope and would love to hear your thoughts — feel free to [open an issue](../../issues) or reach out via [LinkedIn](https://www.linkedin.com/in/gajjarswetang/) or [Email](mailto:gajjarswetang@gmail.com).

---

## 📂 Project Structure
```
folder-intelligence/
├── config.py                  # Central configuration (keywords, entities, rules)
├── universal_intelligence.py  # Stage 1 & 5: Audit & Document
├── universal_declutter.py     # Stage 2: Categorize & Move
├── universal_namer.py         # Stage 3: Content-Aware Rename
├── universal_dedupe.py        # Stage 4: Hash-Based Deduplication
├── SKILL.md                   # AI Agent capability definition
├── SOP.md                     # Enterprise Standard Operating Procedures
├── USER_MANUAL.md             # Step-by-step usage guide
├── CONTRIBUTING.md            # Contribution guidelines
├── CODE_OF_CONDUCT.md         # Community standards
├── LICENSE                    # MIT License
├── requirements.txt           # Dependencies (PyMuPDF only)
└── README.md                  # You are here
```

---

## 🤝 Contributing

We welcome contributions! Check the [Future Scope](#-future-scope) for open items.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the MIT License — see [`LICENSE`](LICENSE) for details.

---

<p align="center">
  <strong>⭐ If this tool saved you time, give it a star!</strong><br>
  <em>Built with precision. Ships with governance. Runs without AI models.</em><br><br>
  <sub>Developed by <a href="https://www.linkedin.com/in/gajjarswetang/">Swetang Gajjar</a></sub>
</p>
