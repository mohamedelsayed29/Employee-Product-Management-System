#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create application icon for مصراوي سات
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple application icon"""
    
    # Create a 256x256 image with a blue background
    size = 256
    img = Image.new('RGBA', (size, size), (25, 118, 210, 255))  # Blue background
    draw = ImageDraw.Draw(img)
    
    # Add a white circle in the center
    circle_center = size // 2
    circle_radius = size // 3
    draw.ellipse(
        [circle_center - circle_radius, circle_center - circle_radius,
         circle_center + circle_radius, circle_center + circle_radius],
        fill=(255, 255, 255, 255)
    )
    
    # Add text "م س" (abbreviation for مصراوي سات)
    try:
        # Try to use a system font that supports Arabic
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 80)
        except:
            font = ImageFont.load_default()
    
    text = "م س"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = circle_center - text_width // 2
    text_y = circle_center - text_height // 2
    
    # Draw text in blue
    draw.text((text_x, text_y), text, fill=(25, 118, 210, 255), font=font)
    
    # Save as ICO file
    img.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    # Also save as PNG for reference
    img.save('app_icon.png', format='PNG')
    
    print("✓ Application icon created successfully!")
    print("✓ Files created: app_icon.ico, app_icon.png")

if __name__ == "__main__":
    create_icon() 