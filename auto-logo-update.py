#!/usr/bin/env python3
"""
Auto-Logo-Updater for HarmonJa Project
Automatycznie zamienia stare logo SVG na nowe we wszystkich plikach HTML
Tesla-level automation: zero manual work!
"""

import re
import os
from pathlib import Path

# Nowy SVG logo (optimized)
NEW_LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="logo-title-new">
  <title id="logo-title-new">Logo HarmonJa Szkoła Psychoterapii</title>
  
  <!-- Szkoła Psychoterapii (odręczny styl na górze) -->
  <text x="250" y="180" font-family="'Brush Script MT', 'Lucida Handwriting', cursive" font-size="90" font-style="italic" fill="#09395f" opacity="0.9">
    Szkoła Psychoterapii
  </text>
  
  <!-- HarmonJa główny tekst -->
  <text x="180" y="420" font-family="'Segoe UI', Arial, sans-serif" font-size="220" font-weight="700" fill="#09395f" letter-spacing="-5">
    Harmon
  </text>
  
  <!-- "Ja" w niebieskim kwadracie -->
  <rect x="910" y="190" width="280" height="280" fill="#22c7d6" rx="0"/>
  <text x="1050" y="420" font-family="'Segoe UI', Arial, sans-serif" font-size="220" font-weight="700" fill="#ffffff" text-anchor="middle">
    Ja
  </text>
</svg>'''


def find_html_files(directory='.'):
    """Find all HTML files in directory"""
    return list(Path(directory).glob('*.html'))


def replace_logo_in_file(filepath):
    """Replace old SVG logo with new one in a single file"""
    print(f"🔍 Processing: {filepath.name}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match SVG inside logo-container
        # Matches from <svg to </svg> including all attributes and content
        pattern = r'(<div class="logo-container">\s*<a[^>]*>\s*)(<svg[^>]*>.*?</svg>)(\s*</a>)'
        
        # Count matches
        matches = re.findall(pattern, content, re.DOTALL)
        
        if not matches:
            print(f"   ⚠️  No logo found (might use different structure)")
            return False
        
        # Replace
        new_content = re.sub(
            pattern,
            r'\1' + NEW_LOGO_SVG + r'\3',
            content,
            flags=re.DOTALL
        )
        
        # Save backup
        backup_path = filepath.with_suffix('.html.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   💾 Backup saved: {backup_path.name}")
        
        # Write new version
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"   ✅ Logo updated successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("🚀 HarmonJa Logo Auto-Updater")
    print("=" * 60)
    print()
    
    # Get current directory or specify your project path
    project_dir = input("Enter project directory path (or press Enter for current): ").strip()
    if not project_dir:
        project_dir = '.'
    
    html_files = find_html_files(project_dir)
    
    if not html_files:
        print("❌ No HTML files found!")
        return
    
    print(f"\n📁 Found {len(html_files)} HTML file(s):")
    for f in html_files:
        print(f"   - {f.name}")
    
    print("\n" + "=" * 60)
    confirm = input("Proceed with logo replacement? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Cancelled by user")
        return
    
    print("\n🔄 Starting replacement...\n")
    
    success_count = 0
    for filepath in html_files:
        if replace_logo_in_file(filepath):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"✨ Complete! Updated {success_count}/{len(html_files)} files")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Check each file to verify logo looks correct")
    print("   2. Test responsive behavior (mobile/desktop)")
    print("   3. If issues occur, restore from .backup files")
    print("   4. Commit to GitHub when satisfied")
    print()


if __name__ == "__main__":
    main()
