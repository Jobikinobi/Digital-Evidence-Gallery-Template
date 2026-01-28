#!/usr/bin/env python3
"""
Stage 2: Optimize for Web

Purpose:
  - Create web-optimized versions of photos (50% resolution, JPEG Q75)
  - Generate thumbnails for gallery (150×150, JPEG Q40)
  - Render PDF pages at 150 DPI (JPEG Q60)
  - Apply smart page limiting for large PDFs

Input:  01-EVIDENCE-VAULT/
Output: 02-WEB-OPTIMIZED/
"""

import os
from PIL import Image
import io
from pathlib import Path
from datetime import datetime

# Configuration
VAULT = Path("01-EVIDENCE-VAULT")
WEB_OPT = Path("02-WEB-OPTIMIZED")

# Image settings
IMAGE_RESIZE_PERCENT = 0.5
IMAGE_JPEG_QUALITY = 75
THUMBNAIL_SIZE = (150, 150)
THUMBNAIL_QUALITY = 40

# Document settings (PDF rendering)
DOCUMENT_DPI = 150
DOCUMENT_JPEG_QUALITY = 60
MAX_PAGES_HUGE = 50   # Files > 20 MB
MAX_PAGES_LARGE = 75  # Files 5-20 MB
MAX_PAGES_SMALL = 100 # Files < 5 MB

print("=" * 80)
print("STAGE 2: OPTIMIZING FOR WEB")
print("=" * 80)
print()

# Create output structure
print("Creating optimization directories...")
WEB_OPT.mkdir(exist_ok=True)
(WEB_OPT / "photos").mkdir(exist_ok=True)
(WEB_OPT / "thumbnails").mkdir(exist_ok=True)
(WEB_OPT / "documents").mkdir(exist_ok=True)
print("✅ Directories created")
print()

# Process photos
photos = list((VAULT / "photos").glob("*.*")) if (VAULT / "photos").exists() else []

if photos:
    print(f"Processing {len(photos)} photos...")
    photo_original_size = 0
    photo_optimized_size = 0
    thumbnail_size = 0

    for idx, photo_path in enumerate(photos, 1):
        try:
            # Track original size
            photo_original_size += photo_path.stat().st_size

            # Load image
            img = Image.open(photo_path)

            # Skip non-photos
            if img.format not in ['JPEG', 'PNG', 'HEIC']:
                print(f"  ⚠️  Skipping {photo_path.name} (unsupported format: {img.format})")
                continue

            # Create optimized version
            if IMAGE_RESIZE_PERCENT < 1.0:
                new_width = int(img.width * IMAGE_RESIZE_PERCENT)
                new_height = int(img.height * IMAGE_RESIZE_PERCENT)
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                img_resized = img

            # Convert to RGB if needed
            if img_resized.mode == 'RGBA':
                rgb_img = Image.new('RGB', img_resized.size, (255, 255, 255))
                rgb_img.paste(img_resized, mask=img_resized.split()[3])
                img_resized = rgb_img
            elif img_resized.mode != 'RGB':
                img_resized = img_resized.convert('RGB')

            # Save optimized version
            output_path = WEB_OPT / "photos" / f"{photo_path.stem}.jpg"
            img_resized.save(output_path, format='JPEG', quality=IMAGE_JPEG_QUALITY, optimize=True)
            photo_optimized_size += output_path.stat().st_size

            # Create thumbnail
            img_thumb = img.copy()
            img_thumb.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

            if img_thumb.mode != 'RGB':
                img_thumb = img_thumb.convert('RGB')

            thumb_path = WEB_OPT / "thumbnails" / f"{photo_path.stem}_thumb.jpg"
            img_thumb.save(thumb_path, format='JPEG', quality=THUMBNAIL_QUALITY, optimize=True)
            thumbnail_size += thumb_path.stat().st_size

            if idx % 5 == 0:
                print(f"  ✅ Processed {idx}/{len(photos)} photos...")

        except Exception as e:
            print(f"  ❌ Error processing {photo_path.name}: {e}")

    print()
    print(f"Photos Summary:")
    print(f"  Original Total: {photo_original_size / (1024*1024):.1f} MB")
    print(f"  Optimized Total: {photo_optimized_size / (1024*1024):.1f} MB")
    print(f"  Thumbnails Total: {thumbnail_size / (1024):.0f} KB")
    print(f"  Reduction: {((photo_original_size - photo_optimized_size) / photo_original_size * 100):.0f}%")
    print()
else:
    print("No photos to process")
    print()

# Process documents
documents = list((VAULT / "documents").glob("*.pdf")) if (VAULT / "documents").exists() else []

if documents:
    print(f"Processing {len(documents)} documents...")
    print("  NOTE: PDF rendering requires PyMuPDF (fitz)")
    print("  Install with: pip3 install PyMuPDF")
    print()

    try:
        import fitz

        doc_original_size = 0
        doc_pages_total = 0

        for idx, doc_path in enumerate(documents, 1):
            try:
                doc_original_size += doc_path.stat().st_size

                # Open PDF
                pdf = fitz.open(doc_path)
                page_count = pdf.page_count

                # Determine page limit based on file size
                file_size = doc_path.stat().st_size
                if file_size > 20 * 1024 * 1024:
                    max_pages = min(page_count, MAX_PAGES_HUGE)
                elif file_size > 5 * 1024 * 1024:
                    max_pages = min(page_count, MAX_PAGES_LARGE)
                else:
                    max_pages = min(page_count, MAX_PAGES_SMALL)

                print(f"  [{idx}/{len(documents)}] {doc_path.name} ({page_count} pages, {file_size / (1024*1024):.1f} MB)")
                print(f"      → Rendering first {max_pages} pages at {DOCUMENT_DPI} DPI...")

                # Render pages
                for page_num in range(max_pages):
                    page = pdf[page_num]
                    mat = fitz.Matrix(DOCUMENT_DPI/72, DOCUMENT_DPI/72)
                    pix = page.get_pixmap(matrix=mat, alpha=False)

                    # Convert to PIL Image
                    img = Image.open(io.BytesIO(pix.tobytes("ppm")))

                    # Save as JPEG
                    output_path = WEB_OPT / "documents" / f"{doc_path.stem}_page_{page_num+1:03d}.jpg"
                    img.save(output_path, format='JPEG', quality=DOCUMENT_JPEG_QUALITY, optimize=True)
                    doc_pages_total += 1

                pdf.close()
                print(f"      ✅ Rendered {max_pages} pages")

            except Exception as e:
                print(f"  ❌ Error processing {doc_path.name}: {e}")

        print()
        print(f"Documents Summary:")
        print(f"  Original Total: {doc_original_size / (1024*1024):.1f} MB")
        print(f"  Pages Rendered: {doc_pages_total}")
        print(f"  Est. Optimized Size: {doc_pages_total * 0.1:.1f} MB (~100 KB/page)")
        print()

    except ImportError:
        print("  ⚠️  PyMuPDF not installed - skipping document optimization")
        print("     Install with: pip3 install PyMuPDF")
        print()
else:
    print("No documents to process")
    print()

# Create optimization log
log_content = f"""WEB OPTIMIZATION LOG
====================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SETTINGS USED:
  Image Resize: {int(IMAGE_RESIZE_PERCENT * 100)}%
  Image JPEG Quality: {IMAGE_JPEG_QUALITY}
  Thumbnail Size: {THUMBNAIL_SIZE[0]}×{THUMBNAIL_SIZE[1]}
  Thumbnail Quality: {THUMBNAIL_QUALITY}
  Document DPI: {DOCUMENT_DPI}
  Document JPEG Quality: {DOCUMENT_JPEG_QUALITY}

RESULTS:
  Photos Optimized: {len(photos)}
  Thumbnails Created: {len(photos)}
  Document Pages Rendered: {doc_pages_total if documents else 0}

  Original Size: {(photo_original_size + (doc_original_size if documents else 0)) / (1024*1024):.1f} MB
  Optimized Size: {(photo_optimized_size + (doc_pages_total * 100000 if documents else 0)) / (1024*1024):.1f} MB
  Reduction: {((photo_original_size - photo_optimized_size) / photo_original_size * 100 if photo_original_size > 0 else 0):.0f}%

FILES CREATED:
  {WEB_OPT}/photos/ ({len(photos)} files)
  {WEB_OPT}/thumbnails/ ({len(photos)} files)
  {WEB_OPT}/documents/ ({doc_pages_total if documents else 0} pages)

Next stage: Generate website (scripts/3_generate_website.py)
"""

with open(WEB_OPT / "OPTIMIZATION_LOG.txt", 'w') as f:
    f.write(log_content)

print("=" * 80)
print("✅ STAGE 2 COMPLETE: Web Optimization Done")
print("=" * 80)
print()
print(f"Output Location: {WEB_OPT}/")
print(f"Photos: {len(photos)} files")
print(f"Thumbnails: {len(photos)} files")
print(f"Document Pages: {doc_pages_total if documents else 0}")
print()
print("Next stage: python3 scripts/3_generate_website.py")
print("=" * 80)
