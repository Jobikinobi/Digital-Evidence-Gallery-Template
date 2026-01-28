# Quick Start - 5 Minutes to Your First Gallery

**Time**: 5 minutes
**Result**: Professional evidence gallery website

---

## ⚡ Ultra-Quick Start

```bash
# 1. Clone template (30 seconds)
git clone https://github.com/Jobikinobi/Digital-Evidence-Gallery-Template.git my-case
cd my-case

# 2. Add evidence (1 minute)
cp /your/photos/*.JPG 00-SOURCE-EVIDENCE/photos/
cp /your/documents/*.pdf 00-SOURCE-EVIDENCE/documents/

# 3. Process (2-3 minutes)
python3 scripts/run_all.py

# 4. View (30 seconds)
cd 03-WEBSITE-OUTPUT && python3 -m http.server 8000
# Open: http://localhost:8000/index.html
```

**Done! Professional gallery with complete metadata.** 🎉

---

## 📋 Prerequisites (One-Time Setup)

```bash
# Install dependencies
pip3 install Pillow PyMuPDF
brew install exiftool  # macOS

# Or see full installation guide in README.md
```

---

## 🎯 What You Get

After 5 minutes, you'll have:
- ✅ Evidence vault with checksums
- ✅ Web-optimized files (85% smaller)
- ✅ Responsive gallery website
- ✅ Complete EXIF metadata displayed
- ✅ Mobile-friendly design
- ✅ Professional appearance

---

## 🔄 The 4-Stage Process

The `run_all.py` script does this automatically:

**Stage 1: Vault** (2 min)
- Extracts metadata
- Generates checksums
- Creates preserved archive

**Stage 2: Optimize** (3 min)
- Compresses photos (50% resolution)
- Creates thumbnails
- Renders PDF pages (150 DPI)

**Stage 3: Website** (1 min)
- Builds responsive gallery
- Implements lazy loading
- Applies brand colors

**Total**: ~6 minutes (plus your time adding evidence)

---

##  ⚠️ One Important Rule

**ALWAYS COPY, NEVER MOVE**

```bash
# ✅ CORRECT:
cp -r /original/evidence/*.JPG 00-SOURCE-EVIDENCE/photos/

# ❌ WRONG:
mv /original/evidence/*.JPG 00-SOURCE-EVIDENCE/photos/
```

Keep originals in secure location!

---

## 📱 Mobile Testing

```bash
# Open in browser
open http://localhost:8000/index.html

# Press F12 (DevTools)
# Press Ctrl+Shift+M (Device Toolbar)
# Select iPhone or iPad
# Test responsive layout
```

---

## 🚀 Next Steps

### Customize
- Change colors: Edit `scripts/3_generate_website.py`
- Adjust quality: Edit `scripts/2_optimize_for_web.py`
- See: `docs/workflows/ADVANCED_USAGE.md`

### Learn More
- Complete guide: `docs/workflows/COMPLETE_WORKFLOW.md`
- Protocols: `docs/protocols/`
- Examples: `docs/examples/`

---

**That's it! Start processing evidence now.** 🎯
