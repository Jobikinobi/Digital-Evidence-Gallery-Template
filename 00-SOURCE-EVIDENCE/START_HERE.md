# START HERE - Add Your Evidence

**This is where you add your raw evidence files.**

---

## 📥 How to Add Evidence

### Step 1: Copy Photos
```bash
cp -r /path/to/photos/*.JPG photos/
cp -r /path/to/photos/*.PNG photos/
```

**Supported**: JPEG, JPG, PNG, HEIC
**What to include**: Crime scene photos, surveillance images, evidence photos

### Step 2: Copy Documents
```bash
cp -r /path/to/documents/*.pdf documents/
```

**Supported**: PDF
**What to include**: Reports, statements, forms, diagrams

### Step 3: Copy Videos (Future Support)
```bash
cp -r /path/to/videos/*.MP4 videos/
```

**Note**: Video processing coming in v1.1.0. For now, just copy them for archival.

---

## ⚠️ CRITICAL RULES

### ALWAYS:
✅ **COPY files** (use `cp`, not `mv`)
✅ **Keep originals** in secure location
✅ **Preserve timestamps** (use `cp -p` or `cp -r`)
✅ **Verify file counts** after copying

### NEVER:
❌ **Move files** from original location
❌ **Delete originals** after copying
❌ **Modify files** before processing
❌ **Rename files** (keep original names)

---

## 📋 After Adding Evidence

Once you've copied all your evidence here:

```bash
# Return to project root
cd ..

# Run Stage 1: Build Vault
python3 scripts/1_build_vault.py

# This will:
#   ✅ Extract metadata (EXIF, PDF properties)
#   ✅ Generate checksums (SHA-256)
#   ✅ Create preserved archive in 01-EVIDENCE-VAULT/
#   ✅ Generate vault manifest
```

---

## 🔍 Verify Your Evidence

### Check File Counts
```bash
echo "Photos: $(ls photos/ | wc -l)"
echo "Documents: $(ls documents/*.pdf | wc -l)"
echo "Videos: $(ls videos/ | wc -l)"
```

### Check File Sizes
```bash
du -sh photos/
du -sh documents/
du -sh videos/
```

### Verify EXIF Data (Photos)
```bash
# Check if photos have EXIF
exiftool photos/*.JPG | grep -i "Date/Time Original"

# If no output, photos may lack EXIF (screenshots, edited images)
# This is OK - system will show "Unknown" for missing data
```

---

## 📂 Expected Folder Structure

After adding evidence, you should have:

```
00-SOURCE-EVIDENCE/
├── photos/
│   ├── IMG_001.JPG
│   ├── IMG_002.JPG
│   └── ... (your photos)
│
├── documents/
│   ├── report.pdf
│   ├── statement.pdf
│   └── ... (your PDFs)
│
└── videos/
    ├── bodycam.MP4
    └── ... (your videos - future support)
```

---

## ✅ Checklist Before Processing

- [ ] All evidence files copied to appropriate folders
- [ ] Original files preserved in secure location
- [ ] File counts verified (matches expected)
- [ ] File sizes reasonable (no corrupted files)
- [ ] File extensions correct (.JPG, .pdf, .MP4)
- [ ] Ready to run Stage 1: Build Vault

---

## 🚀 Next Step

Once your evidence is here, run:

```bash
cd ..  # Return to project root
python3 scripts/1_build_vault.py
```

This creates your evidence vault with checksums and metadata!

---

*Add your evidence here, then run Stage 1 to begin processing*
