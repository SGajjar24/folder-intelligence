
# Universal Folder Optimization Configuration

# 1. Target Directory (Can be overridden by CLI args)
DEFAULT_TARGET_DIR = r"./sample_data"

# 2. File Type Categorization (Extension -> Category)
FILE_EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt"],
    "Spreadsheets": [".xlsx", ".xls", ".csv", ".ods"],
    "Presentations": [".pptx", ".ppt", ".key"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".json", ".xml", ".yaml"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mov", ".avi", ".mkv"]
}

# 3. Content Analysis Keywords (Filename/Content -> Document Type)
# Format: "Standarized_Type": ["keyword1", "keyword2", ...]
KEYWORDS = {
    "Invoice": ["invoice", "bill", "receipt", "payment"],
    "Contract": ["contract", "agreement", "nda", "sow", "proposal"],
    "Identification": ["passport", "license", "id card", "ssn", "visa"],
    "Financial": ["bank statement", "tax", "return", "audit", "balance sheet"],
    "Report": ["report", "analysis", "summary", "audit"],
    "Correspondence": ["letter", "email", "memo"],
    "HR": ["resume", "cv", "offer letter", "payroll", "salary"],
    "Legal": ["affidavit", "court", "summon", "notary", "deed"],
    "Technical": ["spec", "requirement", "architecture", "diagram", "manual"],
}

# 4. Entity Recognition (Filename/Content -> Entity Tag)
# Customize for your organization
ENTITIES = {
    "Internal": ["internal", "confidential", "proprietary"],
    "Client_A": ["client a", "acme corp", "acme"],
    "Vendor_X": ["vendor x", "supplier y"],
    "HR_Dept": ["human resources", "hr", "people ops"],
    "Finance_Dept": ["finance", "accounting", "cfo"],
}

# 5. Rules
MAX_LOOSE_FILES = 10  # Files allowed in root before sub-categorization trigger
README_HEADER = "# 📂 Project Index"
DATE_FORMAT = "%Y-%m-%d" # ISO 8601
