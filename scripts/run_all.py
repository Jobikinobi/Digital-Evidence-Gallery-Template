#!/usr/bin/env python3
"""
Digital Evidence Gallery - Complete Pipeline
Runs all stages: Vault → Optimize → Website
"""

import subprocess
import sys
import os
from pathlib import Path

print("=" * 80)
print("DIGITAL EVIDENCE GALLERY - COMPLETE PIPELINE")
print("=" * 80)
print()

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)

stages = [
    ("1/3", "Building Evidence Vault", "scripts/1_build_vault.py"),
    ("2/3", "Optimizing for Web", "scripts/2_optimize_for_web.py"),
    ("3/3", "Generating Website", "scripts/3_generate_website.py")
]

for stage_num, stage_name, script in stages:
    print(f"Stage {stage_num}: {stage_name}...")
    print("-" * 80)

    try:
        result = subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=False
        )
        print(f"✅ Stage {stage_num} completed successfully")
        print()
    except subprocess.CalledProcessError as e:
        print(f"❌ Stage {stage_num} failed with error code {e.returncode}")
        print(f"   Check the error messages above")
        print(f"   Fix issues and run: python3 {script}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Script not found: {script}")
        print(f"   Ensure you're running from the project root directory")
        sys.exit(1)

print("=" * 80)
print("✅ COMPLETE! All stages finished successfully")
print("=" * 80)
print()
print("Your evidence gallery is ready at: 03-WEBSITE-OUTPUT/")
print()
print("Next steps:")
print("  1. Review gallery:")
print("       cd 03-WEBSITE-OUTPUT/")
print("       python3 -m http.server 8000")
print("       Open: http://localhost:8000/index.html")
print()
print("  2. Test on mobile using browser DevTools")
print()
print("  3. Deliver to client or publish to web server")
print()
print("=" * 80)
