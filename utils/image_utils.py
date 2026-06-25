"""
Utility functions for image processing in AugmentLab
"""

import numpy as np
import cv2
from PIL import Image

def pil_to_cv2(pil_image):
    """Convert PIL image to OpenCV format"""
    # Convert PIL to numpy array
    img_array = np.array(pil_image)
    # Convert RGB to BGR (OpenCV uses BGR)
    if len(img_array.shape) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    return img_array

def cv2_to_pil(cv2_image):
    """Convert OpenCV image to PIL format"""
    # Convert BGR to RGB (OpenCV uses BGR)
    if len(cv2_image.shape) == 3:
        cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    # Convert to PIL
    return Image.fromarray(cv2_image)

def resize_image_keep_aspect(image, target_size):
    """Resize image while keeping aspect ratio"""
    original_width, original_height = image.size
    target_width, target_height = target_size
    
    # Calculate aspect ratios
    aspect_ratio = original_width / original_height
    
    # Determine new dimensions
    if target_width / target_height > aspect_ratio:
        # Height is limiting factor
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
    else:
        # Width is limiting factor
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    
    # Resize image
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return resized_image, (new_width, new_height)

def pad_image_to_size(image, target_size):
    """Pad image to target size with centered content"""
    target_width, target_height = target_size
    original_width, original_height = image.size
    
    # Calculate padding
    delta_width = target_width - original_width
    delta_height = target_height - original_height
    
    # Calculate padding amounts
    pad_left = delta_width // 2
    pad_top = delta_height // 2
    pad_right = delta_width - pad_left
    pad_bottom = delta_height - pad_top
    
    # Pad image
    padded_image = Image.new('RGB', (target_width, target_height), (255, 255, 255))
    padded_image.paste(image, (pad_left, pad_top))
    
    return padded_image