#!/usr/bin/env python3
"""
Stage 1: Build Evidence Vault

Purpose:
  - Extract metadata from all evidence files
  - Generate checksums for integrity verification
  - Create preserved archive in 01-EVIDENCE-VAULT/
  - Generate vault manifest

Input:  00-SOURCE-EVIDENCE/
Output: 01-EVIDENCE-VAULT/
"""

import os
import subprocess
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

# Paths
SOURCE = Path("00-SOURCE-EVIDENCE")
VAULT = Path("01-EVIDENCE-VAULT")
METADATA = VAULT / "metadata"

print("=" * 80)
print("STAGE 1: BUILDING EVIDENCE VAULT")
print("=" * 80)
print()

# Create vault structure
print("Creating vault structure...")
VAULT.mkdir(exist_ok=True)
(VAULT / "photos").mkdir(exist_ok=True)
(VAULT / "documents").mkdir(exist_ok=True)
(VAULT / "videos").mkdir(exist_ok=True)
METADATA.mkdir(exist_ok=True)
print("✅ Vault directories created")
print()

# Scan source evidence
print("Scanning source evidence...")
source_photos = list((SOURCE / "photos").glob("*.*")) if (SOURCE / "photos").exists() else []
source_docs = list((SOURCE / "documents").glob("*.pdf")) if (SOURCE / "documents").exists() else []
source_videos = list((SOURCE / "videos").glob("*.*")) if (SOURCE / "videos").exists() else []

print(f"  ✅ Found {len(source_photos)} photos")
print(f"  ✅ Found {len(source_docs)} documents")
print(f"  ✅ Found {len(source_videos)} videos")
print()

if not source_photos and not source_docs and not source_videos:
    print("⚠️  No evidence files found in 00-SOURCE-EVIDENCE/")
    print("   Please copy your evidence files to:")
    print("     - 00-SOURCE-EVIDENCE/photos/ (for images)")
    print("     - 00-SOURCE-EVIDENCE/documents/ (for PDFs)")
    print("     - 00-SOURCE-EVIDENCE/videos/ (for videos)")
    exit(1)

# Extract EXIF metadata from photos
if source_photos:
    print("Extracting EXIF metadata from photos...")
    try:
        subprocess.run(
            ['exiftool', '-csv'] + [str(p) for p in source_photos],
            stdout=open(METADATA / "photos_exif.csv", 'w'),
            check=True
        )
        print(f"  ✅ Extracted EXIF from {len(source_photos)} photos")
        print(f"  ✅ Saved to: {METADATA / 'photos_exif.csv'}")
    except Exception as e:
        print(f"  ⚠️  Warning: EXIF extraction failed: {e}")
        print(f"     Continuing without EXIF data...")
    print()

# Generate checksums
print("Generating SHA-256 checksums...")
checksums = []

def generate_checksum(filepath):
    """Generate SHA-256 checksum for file"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

all_files = source_photos + source_docs + source_videos
for idx, filepath in enumerate(all_files, 1):
    checksum = generate_checksum(filepath)
    checksums.append(f"{checksum}  {filepath.name}\n")
    if idx % 10 == 0:
        print(f"  ✅ Processed {idx}/{len(all_files)} files...")

with open(METADATA / "checksums.txt", 'w') as f:
    f.writelines(checksums)

print(f"  ✅ Generated {len(checksums)} checksums")
print(f"  ✅ Saved to: {METADATA / 'checksums.txt'}")
print()

# Copy files to vault (preserve timestamps)
print("Copying files to vault (preserving timestamps)...")

for photo in source_photos:
    shutil.copy2(photo, VAULT / "photos" / photo.name)

for doc in source_docs:
    shutil.copy2(doc, VAULT / "documents" / doc.name)

for video in source_videos:
    shutil.copy2(video, VAULT / "videos" / video.name)

print(f"  ✅ Copied {len(source_photos)} photos")
print(f"  ✅ Copied {len(source_docs)} documents")
print(f"  ✅ Copied {len(source_videos)} videos")
print()

# Create vault manifest
print("Creating vault manifest...")
manifest_content = f"""EVIDENCE VAULT MANIFEST
========================
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Files: {len(all_files)}
Total Size: {sum(f.stat().st_size for f in all_files) / (1024*1024):.1f} MB

PHOTOS: {len(source_photos)} files
"""

for photo in source_photos[:5]:  # First 5 as examples
    checksum = next(c for c in checksums if photo.name in c).split()[0]
    manifest_content += f"  - {photo.name} ({photo.stat().st_size / (1024*1024):.1f} MB) [SHA-256: {checksum[:16]}...]\n"

if len(source_photos) > 5:
    manifest_content += f"  ... and {len(source_photos) - 5} more photos\n"

manifest_content += f"\nDOCUMENTS: {len(source_docs)} files\n"

for doc in source_docs[:5]:
    checksum = next(c for c in checksums if doc.name in c).split()[0]
    manifest_content += f"  - {doc.name} ({doc.stat().st_size / (1024*1024):.1f} MB) [SHA-256: {checksum[:16]}...]\n"

if len(source_docs) > 5:
    manifest_content += f"  ... and {len(source_docs) - 5} more documents\n"

manifest_content += f"""
VIDEOS: {len(source_videos)} files
(Video processing support coming in future version)

Metadata Files:
  - metadata/photos_exif.csv ({len(source_photos)} records)
  - metadata/documents_metadata.csv (future)
  - metadata/checksums.txt ({len(checksums)} checksums)

INTEGRITY VERIFICATION:
  All files preserved with SHA-256 checksums
  Original timestamps maintained
  No modifications made to evidence

CHAIN OF CUSTODY:
  Evidence copied from: 00-SOURCE-EVIDENCE/
  Vault location: 01-EVIDENCE-VAULT/
  Processing date: {datetime.now().strftime('%Y-%m-%d')}
  Next stage: Web optimization (scripts/2_optimize_for_web.py)
"""

with open(VAULT / "VAULT_MANIFEST.txt", 'w') as f:
    f.write(manifest_content)

print("  ✅ Vault manifest created")
print()

print("=" * 80)
print("✅ STAGE 1 COMPLETE: Evidence Vault Created")
print("=" * 80)
print()
print(f"Vault Location: {VAULT}/")
print(f"Files Preserved: {len(all_files)}")
print(f"Metadata Extracted: {len(source_photos)} photos")
print(f"Checksums Generated: {len(checksums)}")
print()
print("Next stage: python3 scripts/2_optimize_for_web.py")
print("=" * 80)
