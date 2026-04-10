#!/usr/bin/env python3
"""
Simple PWA Icon Generator (No dependencies)
Creates basic placeholder icons using only Python standard library
"""

import os

# Icon sizes needed for PWA
ICON_SIZES = [16, 32, 72, 96, 120, 128, 144, 152, 180, 192, 384, 512]

# Output directory
OUTPUT_DIR = 'static/icons'

def create_svg_icon(size, output_path):
    """Create a simple SVG icon"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="{size}" height="{size}" fill="url(#grad)" rx="{size//8}"/>
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="{size//4}" 
        font-weight="bold" fill="white" text-anchor="middle" dy=".35em">
    THPT
  </text>
</svg>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"OK: Created {output_path}")

def create_png_placeholder(size, output_path):
    """Create a simple PNG using PIL if available, otherwise SVG"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create image with gradient
        img = Image.new('RGB', (size, size))
        draw = ImageDraw.Draw(img)
        
        # Draw gradient background
        for y in range(size):
            r = int(102 + (118 - 102) * y / size)
            g = int(133 + (75 - 133) * y / size)
            b = int(244 + (162 - 244) * y / size)
            draw.line([(0, y), (size, y)], fill=(r, g, b))
        
        # Add text
        try:
            font_size = size // 4
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        text = "THPT"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x+2, y+2), text, fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        img.save(output_path, 'PNG', optimize=True)
        print(f"OK: Created {output_path}")
        return True
    except ImportError:
        # Fallback to SVG if PIL not available
        svg_path = output_path.replace('.png', '.svg')
        create_svg_icon(size, svg_path)
        print(f"WARNING: PIL not available, created SVG instead: {svg_path}")
        print(f"   Install Pillow for PNG: pip install Pillow")
        return False

def generate_placeholder_icons():
    """Generate placeholder icons"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 60)
    print("PWA Icon Generator for Ôn Thi THPTQG")
    print("=" * 60)
    print()
    
    has_pil = False
    try:
        from PIL import Image
        has_pil = True
        print("✓ PIL/Pillow detected - will generate PNG icons")
    except ImportError:
        print("WARNING: PIL/Pillow not found - will generate SVG icons")
        print("   For PNG icons, install: pip install Pillow")
    
    print()
    print("Generating icons...")
    print()
    
    # Generate each size
    for size in ICON_SIZES:
        output_path = os.path.join(OUTPUT_DIR, f'icon-{size}x{size}.png')
        create_png_placeholder(size, output_path)
    
    # Create apple-touch-icon
    create_png_placeholder(180, os.path.join(OUTPUT_DIR, 'apple-touch-icon.png'))
    
    # Create favicon (just copy 32x32)
    if has_pil:
        try:
            from PIL import Image
            img = Image.open(os.path.join(OUTPUT_DIR, 'icon-32x32.png'))
            img.save(os.path.join(OUTPUT_DIR, 'favicon.ico'), format='ICO')
            print(f"OK: Created favicon.ico")
        except:
            print(f"WARNING: Could not create favicon.ico")
    
    print()
    print("=" * 60)
    print("SUCCESS: Icon generation complete!")
    print(f"   Location: {OUTPUT_DIR}/")
    print()
    print("Generated sizes:")
    print("  - 16x16, 32x32 (favicon)")
    print("  - 72x72, 96x96, 128x128, 144x144 (Android)")
    print("  - 152x152, 180x180 (iOS)")
    print("  - 192x192, 384x384, 512x512 (PWA)")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. python manage.py collectstatic")
    print("  2. python manage.py runserver")
    print("  3. Open http://localhost:8000")
    print("=" * 60)

if __name__ == '__main__':
    generate_placeholder_icons()
