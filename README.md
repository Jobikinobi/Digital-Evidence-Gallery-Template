# Digital Evidence Gallery Template

![Template](https://img.shields.io/badge/type-template-purple)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-ready--to--use-success)

**A ready-to-go starter kit for building forensic evidence galleries from scratch**

This is a **blank template repository** for the Digital Evidence Gallery Generator. Use this template to start a new evidence processing project with all the tools and workflows pre-configured.

---

## 🎯 What This Template Provides

This template gives you a **complete workflow** from raw evidence to professional web gallery:

```
Raw Evidence → Vault → Optimized → Web Gallery
    ↓            ↓         ↓            ↓
  Original    Preserved  Compressed   Beautiful
  Files       Archive    For Web      Website
```

### **4-Stage Workflow**

**Stage 1**: 📥 **SOURCE-EVIDENCE** - Drop your raw evidence files here
**Stage 2**: 🔐 **EVIDENCE-VAULT** - Build preserved original archive
**Stage 3**: ⚡ **WEB-OPTIMIZED** - Create compressed web-ready versions
**Stage 4**: 🌐 **WEBSITE-OUTPUT** - Generate final gallery website

---

## 📁 Folder Structure

```
Your-Evidence-Project/
│
├── 00-SOURCE-EVIDENCE/          📥 START HERE: Drop your evidence
│   ├── photos/                  Put JPEG, PNG images here
│   ├── videos/                  Put MP4, MOV videos here (future support)
│   └── documents/               Put PDF documents here
│
├── 01-EVIDENCE-VAULT/           🔐 Original preserved archive (checksums)
│   ├── photos/                  Original photos + metadata
│   ├── videos/                  Original videos + metadata
│   ├── documents/               Original documents + metadata
│   ├── metadata/                Extracted EXIF and PDF metadata
│   │   ├── photos_exif.csv
│   │   ├── documents_metadata.csv
│   │   └── checksums.txt
│   └── VAULT_MANIFEST.txt       Complete inventory with checksums
│
├── 02-WEB-OPTIMIZED/            ⚡ Web-ready compressed versions
│   ├── photos/                  Optimized JPEGs (50% resolution, Q75)
│   ├── thumbnails/              Small thumbnails (150x150, Q40)
│   ├── documents/               Optimized PDF pages (150 DPI, Q60)
│   └── OPTIMIZATION_LOG.txt     Processing details
│
├── 03-WEBSITE-OUTPUT/           🌐 Final gallery website
│   ├── index.html               Main gallery (lazy loading)
│   ├── images-data.json         Full images (on-demand)
│   ├── documents-data.json      Document pages (on-demand)
│   ├── thumbnails-data.json     Gallery thumbnails
│   └── README.md                User guide for website
│
├── scripts/                     🔧 Processing tools
│   ├── 1_build_vault.py         Extract metadata, create vault
│   ├── 2_optimize_for_web.py    Create web-optimized versions
│   ├── 3_generate_website.py    Build final gallery
│   └── run_all.py               Run complete pipeline
│
└── docs/                        📚 Instructions and guides
    ├── workflows/
    │   ├── COMPLETE_WORKFLOW.md      Full A-Z guide
    │   ├── QUICK_START.md            5-minute quick start
    │   └── ADVANCED_USAGE.md         Advanced features
    └── guides/
        ├── METADATA_GUIDE.md         Understanding metadata
        └── TROUBLESHOOTING.md        Common issues
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Use This Template

**Option A: GitHub (Recommended)**
```bash
# Click "Use this template" button on GitHub
# Or clone:
git clone https://github.com/Jobikinobi/Digital-Evidence-Gallery-Template.git my-evidence-project
cd my-evidence-project
```

**Option B: Download**
- Download ZIP from GitHub
- Extract to your project folder
- Rename folder to your case name

### Step 2: Add Your Evidence
```bash
# Copy your evidence files (NEVER move originals!)
cp -r /path/to/crime-scene-photos/*.JPG 00-SOURCE-EVIDENCE/photos/
cp -r /path/to/reports/*.pdf 00-SOURCE-EVIDENCE/documents/
```

### Step 3: Run the Pipeline
```bash
# Install dependencies (one-time)
pip3 install Pillow PyMuPDF
brew install exiftool

# Run complete workflow
python3 scripts/run_all.py

# This will automatically:
#   ✅ Build evidence vault with checksums
#   ✅ Create web-optimized versions
#   ✅ Generate responsive gallery website
```

### Step 4: View Your Gallery
```bash
cd 03-WEBSITE-OUTPUT/
python3 -m http.server 8000
# Open: http://localhost:8000/index.html
```

**Done! You have a professional evidence gallery with complete metadata preservation.**

---

## 📖 Complete Workflow Guide

### Stage 1: Build Evidence Vault

**Purpose**: Create preserved archive with metadata and checksums

```bash
python3 scripts/1_build_vault.py
```

**What It Does**:
1. ✅ Scans `00-SOURCE-EVIDENCE/` for all files
2. ✅ Extracts EXIF metadata from photos (exiftool)
3. ✅ Extracts PDF metadata from documents (PyMuPDF)
4. ✅ Generates SHA-256 checksums for integrity
5. ✅ Copies originals to `01-EVIDENCE-VAULT/` (preserved forever)
6. ✅ Creates `VAULT_MANIFEST.txt` with complete inventory

**Output Files**:
- `01-EVIDENCE-VAULT/photos/` - Original photos (unchanged)
- `01-EVIDENCE-VAULT/documents/` - Original PDFs (unchanged)
- `01-EVIDENCE-VAULT/metadata/photos_exif.csv` - Complete EXIF data
- `01-EVIDENCE-VAULT/metadata/documents_metadata.csv` - PDF properties
- `01-EVIDENCE-VAULT/metadata/checksums.txt` - SHA-256 hashes
- `01-EVIDENCE-VAULT/VAULT_MANIFEST.txt` - Full inventory

**Why This Matters**:
- 🔐 Original evidence preserved with checksums (forensic integrity)
- 📋 Complete metadata extracted (EXIF, PDF properties)
- ⚖️ Chain of custody documented
- 🗂️ Organized archive for long-term retention

---

### Stage 2: Create Web-Optimized Versions

**Purpose**: Generate compressed versions suitable for web display

```bash
python3 scripts/2_optimize_for_web.py
```

**What It Does**:
1. ✅ Reads originals from `01-EVIDENCE-VAULT/`
2. ✅ Resizes photos to 50% resolution (2000px → 1000px typical)
3. ✅ Compresses to JPEG quality 75 (visually lossless)
4. ✅ Creates thumbnails (150×150px, quality 40)
5. ✅ Renders PDF pages at 150 DPI (screen-optimized)
6. ✅ Applies smart page limiting (50-100 pages for large PDFs)
7. ✅ Saves to `02-WEB-OPTIMIZED/`

**Output Files**:
- `02-WEB-OPTIMIZED/photos/` - Compressed JPEGs (~80% smaller)
- `02-WEB-OPTIMIZED/thumbnails/` - Gallery thumbnails (~95% smaller)
- `02-WEB-OPTIMIZED/documents/` - Rendered PDF pages (150 DPI)
- `02-WEB-OPTIMIZED/OPTIMIZATION_LOG.txt` - Processing details

**File Size Comparison**:
```
Original Photo:     4000×3000px @ 8 MB
Optimized Photo:    2000×1500px @ 400 KB (95% smaller)
Thumbnail:          150×150px @ 8 KB (99.9% smaller)

Original PDF:       328 pages @ 83 MB
Optimized Pages:    50 pages @ 12 MB (85% smaller)
```

**Why This Matters**:
- ⚡ Fast website loading (compressed files)
- 💾 Manageable file sizes for web hosting
- 📱 Mobile-friendly (smaller data transfer)
- 🎨 Maintains visual quality for review

---

### Stage 3: Generate Gallery Website

**Purpose**: Build responsive web gallery with metadata display

```bash
python3 scripts/3_generate_website.py
```

**What It Does**:
1. ✅ Reads optimized files from `02-WEB-OPTIMIZED/`
2. ✅ Reads metadata from `01-EVIDENCE-VAULT/metadata/`
3. ✅ Creates responsive HTML gallery
4. ✅ Implements lazy loading (thumbnails embedded, full data on-demand)
5. ✅ Adds agency filtering (if multi-agency)
6. ✅ Includes keyboard navigation
7. ✅ Applies brand colors
8. ✅ Generates to `03-WEBSITE-OUTPUT/`

**Output Files**:
- `03-WEBSITE-OUTPUT/index.html` - Main gallery (3-10 MB with thumbnails)
- `03-WEBSITE-OUTPUT/images-data.json` - Full images (loaded on click)
- `03-WEBSITE-OUTPUT/documents-data.json` - Document pages (loaded on click)
- `03-WEBSITE-OUTPUT/thumbnails-data.json` - Gallery thumbnails
- `03-WEBSITE-OUTPUT/README.md` - User guide

**Features**:
- 📱 **Responsive Design** - Desktop, tablet, mobile optimized
- 🎨 **Brand Colors** - Customizable (#172144 default)
- 🔍 **Agency Filtering** - Toggle between agencies
- ⌨️ **Keyboard Navigation** - Arrow keys, Escape
- ⚡ **Lazy Loading** - 98% faster initial load
- 📊 **Complete Metadata** - EXIF, PDF properties displayed
- 📅 **Chronological Sorting** - Organized by original dates
- 🌐 **Self-Contained** - Works offline, no dependencies

**Why This Matters**:
- 🎯 Professional presentation for court/clients
- 🚀 Fast loading (1-3 seconds initial)
- 📱 Works on any device
- 🔒 Self-contained (no external dependencies)
- ⚖️ Legal-ready formatting

---

## 🔄 Complete Pipeline (One Command)

### Run All Stages Automatically

```bash
# Run complete pipeline
python3 scripts/run_all.py

# This executes:
#   Stage 1: Build vault (metadata + checksums)
#   Stage 2: Optimize for web (compression)
#   Stage 3: Generate website (gallery)
#
# Total time: 10-30 minutes (depending on evidence size)
```

**Console Output**:
```
================================================================================
DIGITAL EVIDENCE GALLERY - COMPLETE PIPELINE
================================================================================

Stage 1/3: Building Evidence Vault...
  ✅ Extracted EXIF from 23 photos
  ✅ Extracted metadata from 15 PDFs
  ✅ Generated checksums for all files
  ✅ Created vault manifest

Stage 2/3: Optimizing for Web...
  ✅ Optimized 23 photos (95% size reduction)
  ✅ Created 23 thumbnails
  ✅ Rendered 342 PDF pages (150 DPI)
  ✅ Smart page limiting applied

Stage 3/3: Generating Website...
  ✅ Created responsive gallery
  ✅ Implemented lazy loading
  ✅ Applied brand colors
  ✅ Generated documentation

================================================================================
✅ COMPLETE! Gallery ready at: 03-WEBSITE-OUTPUT/index.html
================================================================================

Next steps:
  1. Review: python3 -m http.server 8000 in 03-WEBSITE-OUTPUT/
  2. Test on mobile using browser DevTools
  3. Deliver to client or publish to web
```

---

## 🎯 Key Features

### Evidence Management
✅ **Original Preservation** - Vault maintains untouched originals with checksums
✅ **Complete Metadata** - EXIF and PDF properties fully extracted
✅ **Chain of Custody** - Processing logs and manifests created
✅ **Integrity Verification** - SHA-256 checksums for all files

### Web Gallery
✅ **Responsive Design** - Mobile, tablet, desktop optimized
✅ **Lazy Loading** - 3-10 MB initial load, data on-demand
✅ **Professional Branding** - Customizable colors
✅ **Agency Filtering** - Multi-agency support built-in
✅ **Keyboard Navigation** - Arrow keys, Escape shortcuts
✅ **Touch-Friendly** - Optimized for mobile/tablet

### Optimization
✅ **Image Compression** - 50% resolution, 95% size reduction
✅ **Document Optimization** - 150 DPI, readable on screens
✅ **Smart Page Limiting** - Adaptive limits for large PDFs
✅ **Thumbnail Generation** - Fast gallery display

---

## 📚 Documentation Included

### Workflows
1. **COMPLETE_WORKFLOW.md** - Step-by-step A-Z guide
2. **QUICK_START.md** - 5-minute getting started
3. **ADVANCED_USAGE.md** - Advanced features and customization

### Guides
1. **METADATA_GUIDE.md** - Understanding EXIF and PDF metadata
2. **TROUBLESHOOTING.md** - Common issues and solutions
3. **DEPLOYMENT_GUIDE.md** - Publishing your gallery

---

## 🔧 Prerequisites

### Required Software
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **exiftool** - [Download](https://exiftool.org/) or `brew install exiftool`
- **Modern browser** - Chrome, Firefox, Safari, or Edge

### Python Packages
```bash
pip3 install Pillow PyMuPDF
```

### Verify Installation
```bash
python3 --version   # Should show 3.10+
exiftool -ver       # Should show 12.0+
```

---

## 📖 Detailed Instructions

### Step-by-Step: First Time Setup

#### 1. Get This Template
```bash
# Option A: Use GitHub template
# Click "Use this template" button on GitHub

# Option B: Clone
git clone https://github.com/Jobikinobi/Digital-Evidence-Gallery-Template.git my-case-name
cd my-case-name

# Option C: Download ZIP
# Download and extract to your project folder
```

#### 2. Install Dependencies
```bash
# Install Python packages
pip3 install Pillow PyMuPDF

# Install exiftool (macOS)
brew install exiftool

# Install exiftool (Linux)
sudo apt-get install libimage-exiftool-perl

# Install exiftool (Windows)
# Download from https://exiftool.org/ and add to PATH
```

#### 3. Add Your Evidence
```bash
# Copy (NEVER move) your evidence files
cp -r /path/to/crime-scene-photos/*.JPG 00-SOURCE-EVIDENCE/photos/
cp -r /path/to/witness-videos/*.MP4 00-SOURCE-EVIDENCE/videos/
cp -r /path/to/reports/*.pdf 00-SOURCE-EVIDENCE/documents/

# Verify files copied
ls -R 00-SOURCE-EVIDENCE/
```

**CRITICAL**: Always COPY evidence, never MOVE. Keep originals in secure location.

#### 4. Run Complete Pipeline
```bash
# One command does everything
python3 scripts/run_all.py

# Or run stages individually:
python3 scripts/1_build_vault.py          # Stage 1: Vault + metadata
python3 scripts/2_optimize_for_web.py     # Stage 2: Web optimization
python3 scripts/3_generate_website.py     # Stage 3: Gallery website
```

#### 5. Review Output
```bash
# Start web server
cd 03-WEBSITE-OUTPUT/
python3 -m http.server 8000

# Open in browser
open http://localhost:8000/index.html

# Or just open the file directly
open 03-WEBSITE-OUTPUT/index.html
```

#### 6. Test on Mobile
- Open browser DevTools (F12)
- Toggle device toolbar (Ctrl+Shift+M / Cmd+Shift+M)
- Test iPhone, iPad, Android sizes
- Verify responsive layout works

#### 7. Deliver or Publish
```bash
# Option A: USB drive delivery
cp -r 03-WEBSITE-OUTPUT/* /Volumes/USB-Drive/Evidence-Gallery/

# Option B: Compress for email
7z a evidence-gallery.7z 03-WEBSITE-OUTPUT/

# Option C: Deploy to web server
scp -r 03-WEBSITE-OUTPUT/* user@server:/var/www/evidence/
```

---

## 🎨 Customization

### Change Brand Colors

Edit `scripts/3_generate_website.py`:
```python
# Find this line:
BRAND_COLOR = "#172144"

# Change to your color:
BRAND_COLOR = "#YourHexColor"
```

### Adjust Optimization Quality

Edit `scripts/2_optimize_for_web.py`:
```python
# Image optimization
IMAGE_RESIZE_PERCENT = 0.5    # 0.5 = 50% resolution
IMAGE_JPEG_QUALITY = 75       # 75 = high quality

# Document optimization
DOCUMENT_DPI = 150            # 150 = screen optimized
DOCUMENT_JPEG_QUALITY = 60    # 60 = balanced compression

# Page limits for large PDFs
MAX_PAGES_HUGE = 50           # Files > 20 MB
MAX_PAGES_LARGE = 75          # Files 5-20 MB
MAX_PAGES_SMALL = 100         # Files < 5 MB
```

### Agency Names

Edit `scripts/3_generate_website.py`:
```python
# The script auto-detects agencies from folder names
# To customize display names:
AGENCY_DISPLAY_NAMES = {
    "sheriff": "County Sheriff's Office",
    "citypd": "City Police Department",
    "eppd": "El Paso Police Department"
}
```

---

## 📊 What Gets Generated

### Evidence Vault (Stage 1 Output)
```
01-EVIDENCE-VAULT/
├── photos/ (23 files, originals preserved)
├── documents/ (15 files, originals preserved)
├── metadata/
│   ├── photos_exif.csv (complete EXIF data)
│   ├── documents_metadata.csv (PDF properties)
│   └── checksums.txt (SHA-256 for all files)
└── VAULT_MANIFEST.txt (complete inventory)

Checksums example:
  abc123...def original_photo_001.JPG
  456def...789 witness_statement.pdf
```

### Web-Optimized Files (Stage 2 Output)
```
02-WEB-OPTIMIZED/
├── photos/ (23 files @ ~400 KB each = ~9 MB total)
├── thumbnails/ (23 files @ ~8 KB each = ~180 KB total)
├── documents/ (342 pages @ ~100 KB each = ~34 MB total)
└── OPTIMIZATION_LOG.txt

Original Size:  287 MB
Optimized Size: 43 MB
Reduction:      85%
```

### Website Gallery (Stage 3 Output)
```
03-WEBSITE-OUTPUT/
├── index.html (4 MB - gallery with thumbnails)
├── images-data.json (9 MB - full images)
├── documents-data.json (34 MB - document pages)
├── thumbnails-data.json (4 MB - gallery data)
└── README.md (user guide)

Total:         51 MB (all files)
Initial Load:  4 MB (thumbnails only)
Lazy Loading:  92% on-demand
```

---

## 🎯 File Flow Diagram

```
┌────────────────────────────────────────────────────────┐
│  00-SOURCE-EVIDENCE/                                   │
│  (Raw evidence from camera, scanner, etc.)             │
│                                                         │
│  photos/       videos/       documents/                │
│  IMG_001.JPG   VIDEO.MP4     report.pdf               │
│  IMG_002.JPG   ...           statement.pdf            │
│  ...                         ...                       │
└───────────────────────┬────────────────────────────────┘
                        │
            [Stage 1: Build Vault]
            python3 scripts/1_build_vault.py
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  01-EVIDENCE-VAULT/                                    │
│  (Preserved originals + metadata + checksums)          │
│                                                         │
│  photos/ (originals)    metadata/                      │
│  documents/ (originals) ├─ photos_exif.csv            │
│  videos/ (originals)    ├─ documents_metadata.csv     │
│                         └─ checksums.txt               │
│  VAULT_MANIFEST.txt (complete inventory)              │
└───────────────────────┬────────────────────────────────┘
                        │
        [Stage 2: Optimize for Web]
        python3 scripts/2_optimize_for_web.py
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  02-WEB-OPTIMIZED/                                     │
│  (Compressed web-ready versions)                       │
│                                                         │
│  photos/ (50% resolution, JPEG Q75)                   │
│  thumbnails/ (150×150px, JPEG Q40)                    │
│  documents/ (150 DPI pages, JPEG Q60)                 │
│  OPTIMIZATION_LOG.txt                                  │
└───────────────────────┬────────────────────────────────┘
                        │
        [Stage 3: Generate Website]
        python3 scripts/3_generate_website.py
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  03-WEBSITE-OUTPUT/                                    │
│  (Final responsive gallery website)                    │
│                                                         │
│  index.html (lazy loading portal)                     │
│  images-data.json (full images)                       │
│  documents-data.json (pages)                          │
│  thumbnails-data.json (gallery)                       │
│  README.md (user guide)                               │
│                                                         │
│  ✅ Responsive (mobile/tablet/desktop)                 │
│  ✅ Lazy loading (fast)                                │
│  ✅ Complete metadata                                  │
│  ✅ Professional branding                              │
└────────────────────────────────────────────────────────┘
```

---

## 🎓 Understanding the Stages

### Why 4 Stages?

**Stage 0 (SOURCE-EVIDENCE)**:
- Purpose: Temporary holding area for raw evidence
- Status: Evidence as received, unprocessed
- Action: Copy evidence here from original location
- Next: Build vault from these files

**Stage 1 (EVIDENCE-VAULT)**:
- Purpose: Long-term archive with forensic integrity
- Status: Original files preserved, metadata extracted, checksums generated
- Action: Create preserved archive for retention
- Next: Create web-optimized versions for gallery

**Stage 2 (WEB-OPTIMIZED)**:
- Purpose: Compressed versions suitable for web display
- Status: Optimized for file size while maintaining quality
- Action: Generate compressed photos and rendered PDF pages
- Next: Build responsive web gallery

**Stage 3 (WEBSITE-OUTPUT)**:
- Purpose: Final deliverable - professional web gallery
- Status: Complete, ready to deliver or publish
- Action: Deploy to USB drive, web server, or email
- Next: Deliver to client, publish online, or archive

### What Goes Where?

| Stage | Original Files | Metadata | Checksums | Web-Ready | Website |
|-------|---------------|----------|-----------|-----------|---------|
| **SOURCE** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **VAULT** | ✅ Yes (preserved) | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **WEB-OPT** | ❌ No | ✅ Referenced | ❌ No | ✅ Yes | ❌ No |
| **OUTPUT** | ❌ No | ✅ Embedded | ❌ No | ✅ Embedded | ✅ Yes |

---

## 🔐 Security & Forensics

### Original Evidence Protection
✅ **Never Modified** - Originals in vault remain unchanged
✅ **Checksums** - SHA-256 hashes verify integrity
✅ **Timestamps** - Original dates preserved
✅ **Separate Archive** - Vault isolated from web files

### Metadata Preservation
✅ **EXIF Data** - DateTimeOriginal, camera, settings
✅ **PDF Metadata** - CreationDate, author, producer
✅ **File Information** - Size, type, modification dates
✅ **GPS Data** - Location if present in EXIF

### Chain of Custody
✅ **VAULT_MANIFEST.txt** - Complete inventory
✅ **Processing logs** - All stages documented
✅ **Checksums** - Before and after verification
✅ **Timestamps** - Processing dates recorded

---

## 🎨 Gallery Features

### What Your Website Will Have

**Main Gallery Page**:
- Responsive grid of thumbnails
- Agency badges on each item
- File count statistics in header
- Filter buttons (All Agencies, Agency A, Agency B)

**Image Detail View**:
- Full-size image display
- Complete EXIF metadata sidebar
- Previous/Next navigation
- Keyboard shortcuts (← → Esc)
- Agency identification

**Document Detail View**:
- Page-by-page navigation
- PDF metadata display
- Page counter (Page X of Y)
- Previous/Next page buttons
- Keyboard shortcuts

**Visual Design**:
- Professional color scheme (#172144 default)
- Clean modern interface
- Smooth animations and transitions
- Legal-ready formatting

---

## 🚨 Important Notes

### Evidence Handling Rules

❌ **NEVER** do this:
- Move files from original location (always copy)
- Modify files in `01-EVIDENCE-VAULT/`
- Delete source evidence
- Skip checksum generation
- Process without documentation

✅ **ALWAYS** do this:
- Copy (never move) evidence files
- Generate checksums before and after
- Document chain of custody
- Verify integrity at each stage
- Maintain multiple backups

### What's Gitignored

For security, these are NOT committed to git:
- `00-SOURCE-EVIDENCE/` (raw evidence)
- `01-EVIDENCE-VAULT/` (preserved originals)
- `02-WEB-OPTIMIZED/` (processed files)
- `03-WEBSITE-OUTPUT/*.json` (data files)
- `*.csv` (metadata files)
- `*checksums*.txt` (integrity files)

**Only templates and scripts are in git.**

---

## 🔄 Typical Timeline

### Small Case (10 photos, 5 documents)
- Setup: 2 minutes
- Stage 1 (Vault): 2 minutes
- Stage 2 (Optimize): 3 minutes
- Stage 3 (Website): 2 minutes
- QA Review: 5 minutes
- **Total**: ~15 minutes

### Medium Case (50 photos, 20 documents)
- Setup: 5 minutes
- Stage 1 (Vault): 5 minutes
- Stage 2 (Optimize): 10 minutes
- Stage 3 (Website): 8 minutes
- QA Review: 10 minutes
- **Total**: ~40 minutes

### Large Case (200 photos, 50 documents)
- Setup: 10 minutes
- Stage 1 (Vault): 15 minutes
- Stage 2 (Optimize): 30 minutes
- Stage 3 (Website): 20 minutes
- QA Review: 20 minutes
- **Total**: ~95 minutes

---

## 📦 Example Output

### What You'll Get

**File Sizes** (Typical Medium Case):
```
00-SOURCE-EVIDENCE:     287 MB (original files)
01-EVIDENCE-VAULT:      287 MB (preserved + metadata)
02-WEB-OPTIMIZED:       43 MB (compressed 85%)
03-WEBSITE-OUTPUT:      51 MB (gallery + data)
```

**Gallery Features**:
- Initial load: 4 MB (1-3 seconds)
- Total evidence: 50 photos, 20 documents
- Agency filtering: Yes (if multi-agency)
- Mobile responsive: Yes
- Offline capable: Yes

---

## 🎯 Use Cases

### Criminal Investigations
- Crime scene photography
- Witness statements (PDF)
- Evidence documentation
- Timeline reconstruction

### Legal Proceedings
- Discovery disclosure
- Court exhibits
- Expert witness materials
- Jury presentations

### Compliance & Auditing
- Evidence archival
- Long-term retention
- Audit trail documentation
- Chain of custody maintenance

---

## 🛠️ Advanced Features

### Multi-Agency Processing
```bash
# Organize by agency
mkdir -p 00-SOURCE-EVIDENCE/agency-a/{photos,documents}
mkdir -p 00-SOURCE-EVIDENCE/agency-b/{photos,documents}

# Copy evidence to respective folders
cp /agency-a/evidence/* 00-SOURCE-EVIDENCE/agency-a/photos/
cp /agency-b/evidence/* 00-SOURCE-EVIDENCE/agency-b/documents/

# Run pipeline (auto-detects agencies)
python3 scripts/run_all.py
```

**Result**: Gallery with agency filtering built-in

### Custom Branding
```python
# Edit scripts/3_generate_website.py
BRAND_COLOR = "#172144"         # Your primary color
AGENCY_NAME = "Your Agency"     # Your agency name
CASE_NUMBER = "2026-001"        # Your case number
```

### Batch Processing
```bash
# Process multiple cases
for case in case-001 case-002 case-003; do
    python3 scripts/run_all.py --case $case
done
```

---

## 📞 Support

### Documentation
- **Complete Workflow**: `docs/workflows/COMPLETE_WORKFLOW.md`
- **Quick Start**: `docs/workflows/QUICK_START.md`
- **Troubleshooting**: `docs/guides/TROUBLESHOOTING.md`

### Issues
Report issues at: https://github.com/Jobikinobi/Digital-Evidence-Gallery-Template/issues

### Community
- Share your experience
- Contribute improvements
- Help other users
- Report bugs or request features

---

## 🎊 What Makes This Template Special

### Ready to Use
- ✅ No configuration needed (works out of the box)
- ✅ All scripts included and tested
- ✅ Complete documentation
- ✅ Example workflows

### Professional Quality
- ✅ Forensically sound methodology
- ✅ Legal compliance built-in
- ✅ Chain of custody procedures
- ✅ Court-ready output

### Efficient Workflow
- ✅ One command runs everything
- ✅ Automatic metadata extraction
- ✅ Smart optimization
- ✅ Fast generation

### Flexible & Customizable
- ✅ Adjust quality vs size tradeoffs
- ✅ Custom brand colors
- ✅ Agency-specific settings
- ✅ Extensible architecture

---

## 🚀 Get Started Now

```bash
# 1. Clone template
git clone https://github.com/Jobikinobi/Digital-Evidence-Gallery-Template.git my-case

# 2. Add evidence
cd my-case
cp /evidence/photos/* 00-SOURCE-EVIDENCE/photos/
cp /evidence/docs/* 00-SOURCE-EVIDENCE/documents/

# 3. Generate gallery
python3 scripts/run_all.py

# 4. View result
cd 03-WEBSITE-OUTPUT && python3 -m http.server 8000
```

**Your professional evidence gallery will be ready in minutes!**

---

## 📝 License

MIT License - Free to use for law enforcement and legal purposes.

See [LICENSE](LICENSE) for details.

---

## 🙏 Credits

Built for law enforcement agencies and legal professionals.

Based on the [Digital Evidence Gallery Generator](https://github.com/Jobikinobi/DIGITAL-Forensics-Toolkit).

---

**This template is your ready-to-go kit for processing digital evidence into professional web galleries.**

**Start processing evidence in 5 minutes!**

---

*Digital Evidence Gallery Template - Ready to Use*
*Version: 1.0.0 | Last Updated: 2026-01-26*
*Get Started: Clone this template and add your evidence!*
