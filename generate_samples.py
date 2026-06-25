"""
Script to generate sample images for AugmentLab
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_cat_image():
    """Create a simple cat image"""
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw cat body
    draw.ellipse([50, 80, 150, 180], fill='orange', outline='black', width=2)
    
    # Draw cat head
    draw.ellipse([70, 40, 130, 100], fill='orange', outline='black', width=2)
    
    # Draw ears
    draw.polygon([(80, 40), (70, 20), (90, 30)], fill='orange', outline='black')
    draw.polygon([(120, 40), (110, 20), (130, 30)], fill='orange', outline='black')
    
    # Draw eyes
    draw.ellipse([85, 60, 95, 70], fill='green')
    draw.ellipse([105, 60, 115, 70], fill='green')
    
    # Draw nose
    draw.ellipse([95, 70, 105, 80], fill='pink')
    
    # Draw whiskers
    draw.line([90, 75, 60, 70], fill='black', width=1)
    draw.line([90, 78, 60, 80], fill='black', width=1)
    draw.line([110, 75, 140, 70], fill='black', width=1)
    draw.line([110, 78, 140, 80], fill='black', width=1)
    
    return img

def create_dog_image():
    """Create a simple dog image"""
    img = Image.new('RGB', (200, 200), color='lightgray')
    draw = ImageDraw.Draw(img)
    
    # Draw dog body
    draw.ellipse([40, 100, 160, 180], fill='brown', outline='black', width=2)
    
    # Draw dog head
    draw.ellipse([70, 50, 130, 110], fill='brown', outline='black', width=2)
    
    # Draw ears
    draw.ellipse([60, 40, 80, 70], fill='brown', outline='black', width=2)
    draw.ellipse([120, 40, 140, 70], fill='brown', outline='black', width=2)
    
    # Draw eyes
    draw.ellipse([85, 70, 95, 80], fill='black')
    draw.ellipse([105, 70, 115, 80], fill='black')
    
    # Draw nose
    draw.ellipse([95, 85, 105, 95], fill='black')
    
    # Draw tail
    draw.arc([150, 120, 180, 160], start=0, end=180, fill='brown', width=5)
    
    return img

def create_car_image():
    """Create a simple car image"""
    img = Image.new('RGB', (200, 200), color='skyblue')
    draw = ImageDraw.Draw(img)
    
    # Draw car body
    draw.rectangle([40, 100, 160, 150], fill='red', outline='black', width=2)
    
    # Draw car top
    draw.rectangle([70, 70, 130, 100], fill='red', outline='black', width=2)
    
    # Draw windows
    draw.rectangle([75, 75, 95, 95], fill='lightblue', outline='black', width=1)
    draw.rectangle([105, 75, 125, 95], fill='lightblue', outline='black', width=1)
    
    # Draw wheels
    draw.ellipse([50, 140, 70, 160], fill='black')
    draw.ellipse([130, 140, 150, 160], fill='black')
    
    # Draw headlights
    draw.ellipse([155, 115, 160, 125], fill='yellow')
    
    return img

def create_object_image():
    """Create a simple geometric object image"""
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a house-like shape
    # House base
    draw.rectangle([60, 100, 140, 160], fill='lightblue', outline='black', width=2)
    
    # Roof
    draw.polygon([(60, 100), (100, 60), (140, 100)], fill='red', outline='black')
    
    # Door
    draw.rectangle([90, 130, 110, 160], fill='brown', outline='black', width=1)
    
    # Window
    draw.rectangle([70, 115, 90, 135], fill='yellow', outline='black', width=1)
    draw.rectangle([110, 115, 130, 135], fill='yellow', outline='black', width=1)
    
    # Sun
    draw.ellipse([160, 20, 190, 50], fill='yellow', outline='orange', width=2)
    
    return img

if __name__ == "__main__":
    # Create and save sample images
    cat_img = create_cat_image()
    cat_img.save("assets/sample_cat.jpg")
    
    dog_img = create_dog_image()
    dog_img.save("assets/sample_dog.jpg")
    
    car_img = create_car_image()
    car_img.save("assets/sample_car.jpg")
    
    object_img = create_object_image()
    object_img.save("assets/sample_object.jpg")
    
    print("Sample images generated successfully in assets/ folder!")