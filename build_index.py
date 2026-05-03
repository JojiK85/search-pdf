"""
build_index.py
==============
Run this script ONCE on your computer whenever you add new PDFs.
It reads every PDF and saves an index.json file.

Then upload BOTH your PDFs + index.json to your GitHub repo.

HOW TO RUN:
    pip install pypdf
    python build_index.py                        # scans current folder
    python build_index.py C:\\Users\\you\\pdfs     # scans a specific folder
"""

import os, sys, glob, json
from pathlib import Path
from pypdf import PdfReader

folder = sys.argv[1] if len(sys.argv) > 1 else "."
folder = os.path.abspath(folder)

pdf_files = sorted(glob.glob(os.path.join(folder, "*.pdf")))

if not pdf_files:
    print(f"No PDF files found in: {folder}")
    sys.exit(1)

print(f"Found {len(pdf_files)} PDFs. Building index...\n")
index = []

for i, path in enumerate(pdf_files, 1):
    name = Path(path).name
    print(f"  [{i}/{len(pdf_files)}] Reading: {name}", end="", flush=True)
    try:
        reader = PdfReader(path)
        all_text = ""
        for page in reader.pages:
            all_text += (page.extract_text() or "") + " "
        index.append({
            "file": name,
            "text": all_text.strip()
        })
        print(f"  ✅  ({len(reader.pages)} pages)")
    except Exception as e:
        print(f"  ⚠  Skipped ({e})")

out = os.path.join(folder, "index.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False)

size_kb = round(os.path.getsize(out) / 1024)
print(f"\n✅  Done! Saved index.json ({size_kb} KB)")
print(f"📤  Now upload index.json + your PDFs + index.html to GitHub")
