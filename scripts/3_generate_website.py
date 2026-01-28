#!/usr/bin/env python3
import os
import csv
import json
import base64
from PIL import Image
import io
import fitz
import subprocess
from pathlib import Path

# Configuration
COUNTY_ATTORNEY_FILES_DIR = "/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Exif-Project/County-Attorney/Input-Files-Jan25th"
EL_PASO_IMAGE_DIR = "/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Exif-Project/El-paso-pd/images:videos"
EL_PASO_DOCUMENT_DIR = "/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Exif-Project/El-paso-pd/Documents"

CA_METADATA_FILE = "/tmp/ca_images_exif.csv"
EL_PASO_METADATA = "/tmp/el_paso_images_exif.csv"

OUTPUT_DIR = "/Volumes/HOLE-RAID-DRIVE/Projects/Digital-Forensics/Analysis-Output"
OUTPUT_FILE = f"{OUTPUT_DIR}/unified-forensic-portal-lazy.html"
IMAGES_DATA_FILE = f"{OUTPUT_DIR}/images-data.json"
DOCUMENTS_DATA_FILE = f"{OUTPUT_DIR}/documents-data.json"
THUMBNAILS_DATA_FILE = f"{OUTPUT_DIR}/thumbnails-data.json"

def get_image_metadata(csv_file):
    """Extract metadata from exiftool CSV"""
    metadata_map = {}
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    filename = row.get('FileName', '').split('/')[-1] if row.get('FileName') else ''
                    if filename:
                        metadata_map[filename] = {
                            'DateTimeOriginal': row.get('DateTimeOriginal', 'Unknown'),
                            'Make': row.get('Make', 'Unknown'),
                            'Model': row.get('Model', 'Unknown'),
                            'ISO': row.get('ISO', 'Unknown'),
                            'FNumber': row.get('FNumber', 'Unknown'),
                            'FocalLength': row.get('FocalLength', 'Unknown'),
                            'ShutterSpeed': row.get('ShutterSpeed', 'Unknown'),
                            'ImageWidth': row.get('ImageWidth', 'Unknown'),
                            'ImageHeight': row.get('ImageHeight', 'Unknown'),
                        }
    except Exception as e:
        print(f"Warning: Could not read metadata file {csv_file}: {e}")
    return metadata_map

def image_to_base64(image_path, quality=75, resize_percent=0.5):
    """Convert image to base64 JPEG"""
    try:
        img = Image.open(image_path)
        if img.format not in ['JPEG', 'PNG', 'HEIC']:
            return None, None

        if resize_percent < 1.0:
            new_width = int(img.width * resize_percent)
            new_height = int(img.height * resize_percent)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{b64}", img.size
    except Exception as e:
        print(f"  Error processing {os.path.basename(image_path)}: {e}")
        return None, None

def create_thumbnail(image_path, quality=40, size=(150, 150)):
    """Create small thumbnail for gallery display"""
    try:
        img = Image.open(image_path)
        if img.format not in ['JPEG', 'PNG', 'HEIC']:
            return None

        # Create small thumbnail
        img.thumbnail(size, Image.Resampling.LANCZOS)

        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        return None

def parse_pdf_date(date_str):
    if not date_str:
        return "Unknown"
    try:
        if isinstance(date_str, str) and date_str.startswith('D:'):
            date_str = date_str[2:8]
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}" if len(date_str) >= 8 else "Unknown"
    except:
        return "Unknown"

def pdf_page_to_base64_optimized(pdf_path, page_num, quality=60, dpi=150):
    """Convert PDF page to base64 JPEG"""
    try:
        pdf_document = fitz.open(pdf_path)
        if page_num >= pdf_document.page_count:
            return None, None

        page = pdf_document[page_num]
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{b64}", img.size
    except Exception as e:
        return None, None

def create_pdf_thumbnail(pdf_path, quality=50, dpi=100):
    """Create thumbnail from first page of PDF"""
    try:
        pdf_doc = fitz.open(pdf_path)
        page = pdf_doc[0]
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        return None

def process_images_lazy(image_dir, metadata_map, agency_name):
    """Process images - create thumbnails for gallery, full data separate"""
    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

    thumbnails = []
    full_images = []

    for filename in image_files:
        image_path = os.path.join(image_dir, filename)
        meta = metadata_map.get(filename, {})

        # Create thumbnail for gallery
        thumb = create_thumbnail(image_path, quality=40, size=(150, 150))
        if thumb:
            thumbnails.append({
                'FileName': filename,
                'Agency': agency_name,
                'DateTimeOriginal': meta.get('DateTimeOriginal', 'Unknown'),
                'thumbnail': thumb
            })

        # Full resolution image (stored separately)
        data_uri, _ = image_to_base64(image_path, quality=75, resize_percent=0.5)
        if data_uri:
            full_images.append({
                'FileName': filename,
                'Agency': agency_name,
                'DateTimeOriginal': meta.get('DateTimeOriginal', 'Unknown'),
                'Make': meta.get('Make', 'Unknown'),
                'Model': meta.get('Model', 'Unknown'),
                'ISO': meta.get('ISO', 'Unknown'),
                'FNumber': meta.get('FNumber', 'Unknown'),
                'FocalLength': meta.get('FocalLength', 'Unknown'),
                'ShutterSpeed': meta.get('ShutterSpeed', 'Unknown'),
                'ImageWidth': meta.get('ImageWidth', 'Unknown'),
                'ImageHeight': meta.get('ImageHeight', 'Unknown'),
                'dataUri': data_uri
            })

    return thumbnails, full_images

def process_documents_lazy(doc_dir, agency_name):
    """Process documents - create thumbnails for gallery, pages loaded on demand"""
    doc_files = sorted([f for f in os.listdir(doc_dir) if f.endswith('.pdf')])
    thumbnails = []
    document_metadata = []
    all_pages = {}

    for filename in doc_files:
        doc_path = os.path.join(doc_dir, filename)
        try:
            pdf_doc = fitz.open(doc_path)
            page_count = pdf_doc.page_count
            file_size = os.path.getsize(doc_path)
            metadata = pdf_doc.metadata

            # Create thumbnail from first page
            preview_uri = create_pdf_thumbnail(doc_path, quality=50, dpi=100)

            # Limit pages based on file size
            if file_size > 20 * 1024 * 1024:
                max_pages = min(page_count, 50)
            elif file_size > 5 * 1024 * 1024:
                max_pages = min(page_count, 75)
            else:
                max_pages = min(page_count, 100)

            # Store thumbnail for gallery
            thumbnails.append({
                'FileName': filename,
                'Agency': agency_name,
                'pageCount': page_count,
                'maxPages': max_pages,
                'CreationDateEmbedded': parse_pdf_date(metadata.get('creationDate') if metadata else None) if metadata else "Unknown",
                'preview': preview_uri
            })

            # Store document metadata
            document_metadata.append({
                'FileName': filename,
                'Agency': agency_name,
                'pageCount': page_count,
                'embeddedPages': max_pages,
                'CreationDateEmbedded': parse_pdf_date(metadata.get('creationDate') if metadata else None) if metadata else "Unknown",
                'ModificationDate': parse_pdf_date(metadata.get('modDate') if metadata else None) if metadata else "Unknown",
                'DocumentAuthor': (metadata.get('author') if metadata else None) or "Unknown",
                'DocumentCreator': (metadata.get('creator') if metadata else None) or "Unknown",
                'DocumentProducer': (metadata.get('producer') if metadata else None) or "Unknown",
                'fileSize': file_size
            })

            # Store pages (will be loaded on demand)
            pages = []
            for page_num in range(max_pages):
                data_uri, _ = pdf_page_to_base64_optimized(doc_path, page_num, quality=60, dpi=150)
                if data_uri:
                    pages.append({'pageNumber': page_num + 1, 'dataUri': data_uri})

            all_pages[filename] = pages

            pdf_doc.close()
        except Exception as e:
            print(f"  Error processing {filename}: {str(e)[:80]}")

    return thumbnails, document_metadata, all_pages

print("=" * 80)
print("UNIFIED FORENSIC EVIDENCE PORTAL - LAZY LOADING OPTIMIZED")
print("=" * 80)

# Extract metadata
print("\nExtracting metadata...")
try:
    subprocess.run(
        ['exiftool', '-csv'] +
        [os.path.join(COUNTY_ATTORNEY_FILES_DIR, f) for f in os.listdir(COUNTY_ATTORNEY_FILES_DIR) if f.lower().endswith(('.jpg', '.jpeg'))],
        stdout=open(CA_METADATA_FILE, 'w'),
        check=True
    )
    print("  ✅ Metadata extracted")
except Exception as e:
    print(f"  ⚠️ Warning: {e}")

# Process images
print("\nProcessing images...")
ca_image_meta = get_image_metadata(CA_METADATA_FILE)
ep_image_meta = get_image_metadata(EL_PASO_METADATA)

ca_thumb, ca_full = process_images_lazy(COUNTY_ATTORNEY_FILES_DIR, ca_image_meta, "County Attorney")
ep_thumb, ep_full = process_images_lazy(EL_PASO_IMAGE_DIR, ep_image_meta, "El Paso PD")

print(f"  County Attorney: {len(ca_thumb)} images")
print(f"  El Paso PD: {len(ep_thumb)} images")

# Process documents
print("\nProcessing documents...")
ca_doc_thumb, ca_doc_meta, ca_doc_pages = process_documents_lazy(COUNTY_ATTORNEY_FILES_DIR, "County Attorney")
ep_doc_thumb, ep_doc_meta, ep_doc_pages = process_documents_lazy(EL_PASO_DOCUMENT_DIR, "El Paso PD")

print(f"  County Attorney: {len(ca_doc_thumb)} documents")
print(f"  El Paso PD: {len(ep_doc_thumb)} documents")

# Combine
all_image_thumbs = ca_thumb + ep_thumb
all_image_full = ca_full + ep_full
all_doc_thumbs = ca_doc_thumb + ep_doc_thumb
all_doc_meta = ca_doc_meta + ep_doc_meta
all_doc_pages = {**ca_doc_pages, **ep_doc_pages}

def sort_thumbs(item):
    return (item['Agency'], item.get('DateTimeOriginal', 'Unknown'))

def sort_doc_thumbs(item):
    return (item['Agency'], item.get('CreationDateEmbedded', 'Unknown'))

all_image_thumbs.sort(key=sort_thumbs)
all_image_full.sort(key=sort_thumbs)
all_doc_thumbs.sort(key=sort_doc_thumbs)
all_doc_meta.sort(key=sort_doc_thumbs)

# Save separate data files
print("\nSaving data files...")

# Thumbnails (embedded in HTML for fast loading)
thumbnails_data = {
    'images': all_image_thumbs,
    'documents': all_doc_thumbs
}

# Full image data (loaded on demand)
with open(IMAGES_DATA_FILE, 'w') as f:
    json.dump(all_image_full, f, ensure_ascii=False)
print(f"  ✅ Images data: {os.path.getsize(IMAGES_DATA_FILE) / (1024*1024):.1f} MB")

# Document data (metadata + pages)
documents_full = {}
for meta in all_doc_meta:
    filename = meta['FileName']
    documents_full[filename] = {
        'metadata': meta,
        'pages': all_doc_pages.get(filename, [])
    }

with open(DOCUMENTS_DATA_FILE, 'w') as f:
    json.dump(documents_full, f, ensure_ascii=False)
print(f"  ✅ Documents data: {os.path.getsize(DOCUMENTS_DATA_FILE) / (1024*1024):.1f} MB")

# Thumbnails data
with open(THUMBNAILS_DATA_FILE, 'w') as f:
    json.dump(thumbnails_data, f, ensure_ascii=False)
print(f"  ✅ Thumbnails: {os.path.getsize(THUMBNAILS_DATA_FILE) / (1024*1024):.1f} MB")

print("\nGenerating HTML portal with lazy loading...")

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unified Forensic Evidence Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            min-height: 100vh;
            padding: 10px;
            color: #172144;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .header {
            background: #172144;
            color: white;
            padding: 20px;
            text-align: center;
        }

        .header h1 {
            font-size: clamp(24px, 5vw, 36px);
            margin-bottom: 8px;
        }

        .header p {
            font-size: clamp(12px, 3vw, 14px);
            opacity: 0.9;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: clamp(20px, 4vw, 24px);
            font-weight: bold;
        }

        .stat-label {
            font-size: 12px;
            opacity: 0.8;
            margin-top: 4px;
        }

        .nav-tabs {
            display: flex;
            background: #f5f5f5;
            border-bottom: 2px solid #e0e0e0;
            flex-wrap: wrap;
        }

        .nav-tab {
            flex: 1;
            min-width: 120px;
            padding: 14px 12px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: clamp(13px, 2vw, 16px);
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
            border-bottom: 3px solid transparent;
        }

        .nav-tab.active {
            color: #172144;
            background: white;
            border-bottom-color: #172144;
        }

        .nav-tab:hover {
            background: #fafafa;
        }

        .content-area {
            display: none;
            padding: clamp(15px, 4vw, 30px);
        }

        .content-area.active {
            display: block;
        }

        .agency-filter {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #172144;
            background: white;
            color: #172144;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            min-height: 44px;
        }

        .filter-btn.active {
            background: #172144;
            color: white;
        }

        .filter-btn:hover {
            background: #172144;
            color: white;
        }

        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 12px;
        }

        @media (min-width: 640px) {
            .gallery {
                grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
                gap: 15px;
            }
        }

        @media (min-width: 1024px) {
            .gallery {
                grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
                gap: 15px;
            }
        }

        .gallery-item {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
            min-height: 160px;
        }

        .gallery-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            border-color: #172144;
        }

        .gallery-thumb {
            width: 100%;
            height: 120px;
            object-fit: cover;
            background: #f0f0f0;
        }

        .gallery-info {
            padding: 10px;
        }

        .gallery-title {
            font-size: clamp(11px, 1.5vw, 12px);
            font-weight: 600;
            color: #172144;
            margin-bottom: 6px;
            word-break: break-word;
            line-height: 1.3;
        }

        .gallery-badge {
            display: inline-block;
            font-size: 10px;
            padding: 3px 6px;
            background: #e8e8e8;
            border-radius: 3px;
            color: #172144;
            font-weight: 600;
        }

        .agency-badge {
            display: inline-block;
            font-size: 10px;
            padding: 3px 6px;
            background: #172144;
            color: white;
            border-radius: 3px;
            margin-right: 4px;
            font-weight: 600;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 10px;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            border-radius: 8px;
            max-width: 95vw;
            max-height: 90vh;
            display: flex;
            overflow: hidden;
            flex-direction: column;
        }

        @media (min-width: 768px) {
            .modal-content {
                flex-direction: row-reverse;
                width: 90vw;
                height: 85vh;
            }
        }

        @media (min-width: 1200px) {
            .modal-content {
                width: 1000px;
                height: 700px;
            }
        }

        .modal-header {
            background: #172144;
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: nowrap;
            gap: 10px;
            flex: 0 0 auto;
        }

        .modal-title {
            font-size: clamp(14px, 3vw, 16px);
            font-weight: 600;
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .close-btn {
            background: none;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 5px;
            min-width: 44px;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .modal-image {
            flex: 1 1 60%;
            padding: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f9f9f9;
            overflow: auto;
            min-width: 0;
        }

        .modal-image img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        .modal-meta {
            flex: 0 0 350px;
            padding: 15px;
            background: white;
            overflow-y: auto;
            border-right: 1px solid #e0e0e0;
        }

        @media (min-width: 768px) {
            .modal-meta {
                border-right: 1px solid #e0e0e0;
                border-left: none;
            }
        }

        @media (max-width: 767px) {
            .modal-content {
                flex-direction: column;
                width: auto;
                height: auto;
            }
            .modal-meta {
                flex: 0 0 auto;
                max-height: 200px;
                border-right: none;
                border-top: 1px solid #e0e0e0;
            }
        }

        .modal-controls {
            display: flex;
            gap: 8px;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .control-btn {
            background: #172144;
            color: white;
            border: none;
            padding: 10px 12px;
            border-radius: 4px;
            cursor: pointer;
            min-height: 44px;
            font-weight: 600;
            flex: 1;
            min-width: 80px;
        }

        .control-btn:hover {
            background: #0f1630;
        }

        .control-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .counter {
            font-size: 13px;
            color: #172144;
            padding: 10px;
            white-space: nowrap;
        }

        .meta-field {
            margin-bottom: 12px;
        }

        .meta-label {
            font-size: 10px;
            color: #999;
            text-transform: uppercase;
            font-weight: 600;
        }

        .meta-value {
            font-size: 13px;
            color: #172144;
            margin-top: 3px;
            word-break: break-word;
        }

        .divider {
            margin: 15px 0;
            border-top: 1px solid #e0e0e0;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #172144;
        }

        .loading::after {
            content: '';
            animation: dots 1.5s steps(4, end) infinite;
        }

        @keyframes dots {
            0%, 20% { content: ''; }
            40% { content: '.'; }
            60% { content: '..'; }
            80%, 100% { content: '...'; }
        }

        @media (max-width: 480px) {
            .container { border-radius: 4px; }
            .header { padding: 15px; }
            .nav-tab { padding: 10px 8px; font-size: 12px; }
            .content-area { padding: 12px; }
            .gallery { grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; }
            .modal-header { padding: 12px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Unified Forensic Evidence Portal</h1>
            <p>Comprehensive evidence review system for law enforcement agencies</p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">22</div>
                    <div class="stat-label">Photographs</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">21</div>
                    <div class="stat-label">Documents</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">LAZY_PAGE_COUNT</div>
                    <div class="stat-label">Pages (Lazy Loaded)</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">2</div>
                    <div class="stat-label">Agencies</div>
                </div>
            </div>
        </div>

        <div class="nav-tabs">
            <button class="nav-tab active" onclick="switchTab('images')">📸 Images</button>
            <button class="nav-tab" onclick="switchTab('documents')">📄 Documents</button>
        </div>

        <div id="images" class="content-area active">
            <h2 style="margin-bottom: 15px; color: #172144;">Evidence Photographs</h2>
            <div class="agency-filter">
                <button class="filter-btn active" onclick="filterByAgency('images', 'all')">All Agencies</button>
                <button class="filter-btn" onclick="filterByAgency('images', 'County Attorney')">County Attorney</button>
                <button class="filter-btn" onclick="filterByAgency('images', 'El Paso PD')">El Paso PD</button>
            </div>
            <div id="imageGallery" class="gallery"></div>
        </div>

        <div id="documents" class="content-area">
            <h2 style="margin-bottom: 15px; color: #172144;">Evidence Documents</h2>
            <div class="agency-filter">
                <button class="filter-btn active" onclick="filterByAgency('documents', 'all')">All Agencies</button>
                <button class="filter-btn" onclick="filterByAgency('documents', 'County Attorney')">County Attorney</button>
                <button class="filter-btn" onclick="filterByAgency('documents', 'El Paso PD')">El Paso PD</button>
            </div>
            <div id="documentGallery" class="gallery"></div>
        </div>
    </div>

    <div id="imageModal" class="modal">
        <div class="modal-content">
            <div style="width: 100%; background: #172144; color: white; padding: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div class="modal-title" id="imageModalTitle"></div>
                <button class="close-btn" onclick="closeModal('imageModal')">✕</button>
            </div>
            <div class="modal-image">
                <img id="modalImage" src="" alt="">
            </div>
            <div class="modal-meta">
                <div id="imageMetaContent"></div>
                <div class="modal-controls">
                    <button class="control-btn" id="imagePrevBtn" onclick="previousImage()">← Prev</button>
                    <div class="counter"><span id="imageCounter"></span></div>
                    <button class="control-btn" id="imageNextBtn" onclick="nextImage()">Next →</button>
                </div>
            </div>
        </div>
    </div>

    <div id="documentModal" class="modal">
        <div class="modal-content">
            <div style="width: 100%; background: #172144; color: white; padding: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div class="modal-title" id="documentModalTitle"></div>
                <button class="close-btn" onclick="closeModal('documentModal')">✕</button>
            </div>
            <div class="modal-image">
                <img id="documentImage" src="" alt="">
            </div>
            <div class="modal-meta">
                <div id="documentMetaContent"></div>
                <div class="modal-controls">
                    <button class="control-btn" id="documentPrevBtn" onclick="previousPage()">← Prev Page</button>
                    <div class="counter"><span id="pageCounter"></span></div>
                    <button class="control-btn" id="documentNextBtn" onclick="nextPage()">Next Page →</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Embedded thumbnail data (small, fast to load)
        const thumbnailData = THUMBNAILS_DATA_PLACEHOLDER;

        // These will be loaded on demand
        let imageDataCache = null;
        let documentDataCache = null;

        let currentImageFilter = 'all';
        let currentDocumentFilter = 'all';
        let currentImageIndex = 0;
        let currentDocumentIndex = 0;
        let currentPageIndex = 0;

        // Load image data on demand
        async function loadImageData() {
            if (imageDataCache) return imageDataCache;
            try {
                const response = await fetch('images-data.json');
                imageDataCache = await response.json();
                return imageDataCache;
            } catch (e) {
                console.error('Failed to load image data:', e);
                return [];
            }
        }

        // Load document data on demand
        async function loadDocumentData() {
            if (documentDataCache) return documentDataCache;
            try {
                const response = await fetch('documents-data.json');
                documentDataCache = await response.json();
                return documentDataCache;
            } catch (e) {
                console.error('Failed to load document data:', e);
                return {};
            }
        }

        function switchTab(tabName) {
            document.querySelectorAll('.content-area').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function filterByAgency(type, agency) {
            if (type === 'images') {
                currentImageFilter = agency;
                renderImageGallery();
            } else {
                currentDocumentFilter = agency;
                renderDocumentGallery();
            }

            event.target.parentElement.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }

        function renderImageGallery() {
            const gallery = document.getElementById('imageGallery');
            const filtered = currentImageFilter === 'all' ?
                thumbnailData.images :
                thumbnailData.images.filter(img => img.Agency === currentImageFilter);

            let html = '';
            filtered.forEach((img, idx) => {
                const actualIdx = thumbnailData.images.indexOf(img);
                html += `<div class="gallery-item" onclick="openImageModal(${actualIdx})">
                    <img src="${img.thumbnail}" class="gallery-thumb" alt="${escapeHtml(img.FileName)}">
                    <div class="gallery-info">
                        <div class="agency-badge">${escapeHtml(img.Agency.split(' ')[0])}</div>
                        <div class="gallery-title" title="${escapeHtml(img.FileName)}">${escapeHtml(img.FileName.substring(0, 20))}</div>
                    </div>
                </div>`;
            });
            gallery.innerHTML = html || '<div class="loading">No images found</div>';
        }

        function renderDocumentGallery() {
            const gallery = document.getElementById('documentGallery');
            const filtered = currentDocumentFilter === 'all' ?
                thumbnailData.documents :
                thumbnailData.documents.filter(doc => doc.Agency === currentDocumentFilter);

            let html = '';
            filtered.forEach((doc, idx) => {
                const actualIdx = thumbnailData.documents.indexOf(doc);
                html += `<div class="gallery-item" onclick="openDocumentModal(${actualIdx})">
                    ${doc.preview ? `<img src="${doc.preview}" class="gallery-thumb">` : '<div class="gallery-thumb" style="display:flex;align-items:center;justify-content:center;background:#e0e0e0;"><span style="color:#999;">📄</span></div>'}
                    <div class="gallery-info">
                        <div class="agency-badge">${escapeHtml(doc.Agency.split(' ')[0])}</div>
                        <div class="gallery-title" title="${escapeHtml(doc.FileName)}">${escapeHtml(doc.FileName.substring(0, 20))}</div>
                        <div class="gallery-badge">${doc.pageCount} pages</div>
                    </div>
                </div>`;
            });
            gallery.innerHTML = html || '<div class="loading">No documents found</div>';
        }

        async function openImageModal(idx) {
            const imageData = await loadImageData();
            currentImageIndex = idx;
            displayImage(imageData);
            document.getElementById('imageModal').classList.add('active');
        }

        async function openDocumentModal(idx) {
            const documentData = await loadDocumentData();
            currentDocumentIndex = idx;
            currentPageIndex = 0;
            displayDocument(documentData);
            document.getElementById('documentModal').classList.add('active');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }

        async function displayImage(imageData) {
            const img = imageData[currentImageIndex];
            document.getElementById('modalImage').src = img.dataUri;
            document.getElementById('imageModalTitle').textContent = escapeHtml(img.FileName);
            document.getElementById('imageCounter').textContent = `${currentImageIndex + 1} / ${imageData.length}`;

            let meta = `<span class="agency-badge">${escapeHtml(img.Agency)}</span>`;
            meta += '<div class="divider"></div>';
            meta += '<div class="meta-field"><div class="meta-label">Date/Time</div><div class="meta-value">' + escapeHtml(img.DateTimeOriginal) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Camera</div><div class="meta-value">' + escapeHtml(img.Make) + ' ' + escapeHtml(img.Model) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">ISO</div><div class="meta-value">' + escapeHtml(img.ISO) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Aperture</div><div class="meta-value">' + escapeHtml(img.FNumber) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Shutter Speed</div><div class="meta-value">' + escapeHtml(img.ShutterSpeed) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Focal Length</div><div class="meta-value">' + escapeHtml(img.FocalLength) + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Resolution</div><div class="meta-value">' + escapeHtml(img.ImageWidth) + ' × ' + escapeHtml(img.ImageHeight) + '</div></div>';

            document.getElementById('imageMetaContent').innerHTML = meta;
            document.getElementById('imagePrevBtn').disabled = currentImageIndex === 0;
            document.getElementById('imageNextBtn').disabled = currentImageIndex === imageData.length - 1;
        }

        async function displayDocument(documentData) {
            const docThumb = thumbnailData.documents[currentDocumentIndex];
            const docKey = docThumb.FileName;
            const doc = documentData[docKey];

            if (!doc) {
                document.getElementById('documentMetaContent').innerHTML = '<div class="loading">Loading document</div>';
                return;
            }

            const pages = doc.pages;
            if (pages.length === 0) {
                document.getElementById('documentMetaContent').innerHTML = '<div class="loading">No pages available</div>';
                return;
            }

            const page = pages[currentPageIndex];
            document.getElementById('documentImage').src = page.dataUri;
            document.getElementById('documentModalTitle').textContent = escapeHtml(docThumb.FileName);
            document.getElementById('pageCounter').textContent = `Page ${currentPageIndex + 1} of ${pages.length}`;

            const metadata = doc.metadata;
            let meta = `<span class="agency-badge">${escapeHtml(metadata.Agency)}</span>`;
            meta += '<div class="divider"></div>';
            meta += '<div class="meta-field"><div class="meta-label">Created</div><div class="meta-value">' + metadata.CreationDateEmbedded + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Total Pages</div><div class="meta-value">' + metadata.pageCount + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Embedded Pages</div><div class="meta-value">' + metadata.embeddedPages + '</div></div>';
            meta += '<div class="meta-field"><div class="meta-label">Author</div><div class="meta-value">' + metadata.DocumentAuthor + '</div></div>';

            document.getElementById('documentMetaContent').innerHTML = meta;
            document.getElementById('documentPrevBtn').disabled = currentPageIndex === 0;
            document.getElementById('documentNextBtn').disabled = currentPageIndex === pages.length - 1;
        }

        async function previousImage() {
            if (currentImageIndex > 0) {
                const imageData = await loadImageData();
                currentImageIndex--;
                displayImage(imageData);
            }
        }

        async function nextImage() {
            const imageData = await loadImageData();
            if (currentImageIndex < imageData.length - 1) {
                currentImageIndex++;
                displayImage(imageData);
            }
        }

        async function previousPage() {
            const documentData = await loadDocumentData();
            const docThumb = thumbnailData.documents[currentDocumentIndex];
            const doc = documentData[docThumb.FileName];
            if (currentPageIndex > 0) {
                currentPageIndex--;
                displayDocument(documentData);
            }
        }

        async function nextPage() {
            const documentData = await loadDocumentData();
            const docThumb = thumbnailData.documents[currentDocumentIndex];
            const doc = documentData[docThumb.FileName];
            if (currentPageIndex < doc.pages.length - 1) {
                currentPageIndex++;
                displayDocument(documentData);
            }
        }

        function escapeHtml(text) {
            const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
            return String(text).replace(/[&<>"']/g, m => map[m]);
        }

        document.addEventListener('keydown', async (e) => {
            if (document.getElementById('imageModal').classList.contains('active')) {
                if (e.key === 'ArrowLeft') previousImage();
                if (e.key === 'ArrowRight') nextImage();
                if (e.key === 'Escape') closeModal('imageModal');
            }
            if (document.getElementById('documentModal').classList.contains('active')) {
                if (e.key === 'ArrowLeft') previousPage();
                if (e.key === 'ArrowRight') nextPage();
                if (e.key === 'Escape') closeModal('documentModal');
            }
        });

        // Initialize galleries
        renderImageGallery();
        renderDocumentGallery();
    </script>
</body>
</html>'''

html_content = html_template.replace('THUMBNAILS_DATA_PLACEHOLDER', json.dumps(thumbnails_data, ensure_ascii=False))
total_pages = sum(len(pages) for pages in all_doc_pages.values())
html_content = html_content.replace('LAZY_PAGE_COUNT', str(total_pages))

with open(OUTPUT_FILE, 'w') as f:
    f.write(html_content)

main_file_size = os.path.getsize(OUTPUT_FILE) / (1024*1024)
total_size = main_file_size + (os.path.getsize(IMAGES_DATA_FILE) + os.path.getsize(DOCUMENTS_DATA_FILE) + os.path.getsize(THUMBNAILS_DATA_FILE)) / (1024*1024)

print(f"\n✅ Lazy-loading portal created!")
print(f"\nFile Breakdown:")
print(f"  Main HTML: {main_file_size:.1f} MB (with embedded thumbnails)")
print(f"  Images Data: {os.path.getsize(IMAGES_DATA_FILE) / (1024*1024):.1f} MB (loaded on demand)")
print(f"  Documents Data: {os.path.getsize(DOCUMENTS_DATA_FILE) / (1024*1024):.1f} MB (loaded on demand)")
print(f"  Thumbnails Index: {os.path.getsize(THUMBNAILS_DATA_FILE) / (1024*1024):.1f} MB")
print(f"\nTotal with all data: {total_size:.1f} MB")
print(f"Initial load: {main_file_size:.1f} MB (fast - only thumbnails!)")
print(f"Optimization: ~{((1-main_file_size/total_size)*100):.0f}% of data loaded on-demand")
print(f"\n🎯 Access: {OUTPUT_FILE}")
print("=" * 80)
