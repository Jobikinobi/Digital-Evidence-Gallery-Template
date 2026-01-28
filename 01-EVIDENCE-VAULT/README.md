# Evidence Vault - Preserved Originals

**This folder contains your preserved evidence archive with metadata and checksums.**

---

## 🔐 What's in This Folder

After running `python3 scripts/1_build_vault.py`, this folder will contain:

```
01-EVIDENCE-VAULT/
├── photos/                    Original photos (unchanged)
├── documents/                 Original PDFs (unchanged)
├── videos/                    Original videos (unchanged)
├── metadata/
│   ├── photos_exif.csv        Complete EXIF data for all photos
│   ├── documents_metadata.csv PDF properties (future)
│   └── checksums.txt          SHA-256 hashes for integrity
└── VAULT_MANIFEST.txt         Complete inventory
```

---

## 🎯 Purpose

This vault serves as:
- 🔒 **Long-term archive** of original evidence
- 📋 **Metadata repository** (EXIF, PDF properties)
- ✅ **Integrity verification** (checksums)
- ⚖️ **Legal compliance** (chain of custody)

---

## ⚠️ CRITICAL RULES

### DO NOT:
❌ Modify any files in this folder
❌ Delete files from this folder
❌ Rename files in this folder
❌ Add files manually (use scripts only)

### Purpose:
This folder is a **forensically sound archive**. Files must remain unchanged to maintain integrity.

---

## 📊 What Gets Generated

### Metadata Files

**photos_exif.csv**:
```csv
FileName,DateTimeOriginal,Make,Model,ISO,FNumber,ShutterSpeed,FocalLength
IMG_001.JPG,2023:08:15 14:32:00,Canon,EOS R5,400,2.8,1/500,85mm
IMG_002.JPG,2023:08:15 14:35:12,Canon,EOS R5,400,2.8,1/500,85mm
```

**checksums.txt**:
```
abc123def456...  IMG_001.JPG
789ghi012jkl...  IMG_002.JPG
345mno678pqr...  report.pdf
```

**VAULT_MANIFEST.txt**:
```
EVIDENCE VAULT MANIFEST
========================
Created: 2026-01-26 10:00:00
Total Files: 38
Total Size: 287 MB

PHOTOS: 23 files
  - IMG_001.JPG (8.2 MB) [SHA-256: abc123...]
  ...
```

---

## ✅ Integrity Verification

### Check Checksums
```bash
# Verify files unchanged
cd metadata/
shasum -a 256 -c checksums.txt

# Expected output: "OK" for each file
# If any show "FAILED", integrity compromised
```

### Review Manifest
```bash
cat VAULT_MANIFEST.txt
# Shows complete inventory with checksums
```

---

## 🔄 Next Stage

Once vault is created, proceed to:

```bash
cd ..  # Return to project root
python3 scripts/2_optimize_for_web.py
```

This creates web-optimized versions in `02-WEB-OPTIMIZED/`

---

*Evidence Vault - Preserved originals with forensic integrity*
