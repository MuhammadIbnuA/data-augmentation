import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def draw_bbox(image, bbox, color='red', thickness=3):
    """Draw bounding box on image"""
    draw = ImageDraw.Draw(image)
    x1, y1, x2, y2 = bbox
    draw.rectangle([x1, y1, x2, y2], outline=color, width=thickness)
    return image

def transform_bbox(bbox, transform_type, img_size, params=None):
    """Apply transformation to bounding box"""
    x1, y1, x2, y2 = bbox
    width, height = img_size
    
    if transform_type == "shift":
        offset_x = params.get('offset_x', 0)
        offset_y = params.get('offset_y', 0)
        return [x1+offset_x, y1+offset_y, x2+offset_x, y2+offset_y]
    elif transform_type == "crop":
        crop_left = params.get('crop_left', 0)
        crop_top = params.get('crop_top', 0)
        # Adjust bbox coordinates relative to crop
        # The bounding box coordinates need to be adjusted to the new coordinate system after cropping
        new_x1 = x1 - crop_left
        new_y1 = y1 - crop_top
        new_x2 = x2 - crop_left
        new_y2 = y2 - crop_top
        
        # Ensure the bounding box stays within the new image bounds
        # (coordinates could become negative if bbox was near the cropped edge)
        new_x1 = max(0, new_x1)
        new_y1 = max(0, new_y1)
        new_x2 = max(0, new_x2)
        new_y2 = max(0, new_y2)
        
        # Make sure x2 > x1 and y2 > y1
        new_x2 = max(new_x1 + 1, new_x2)
        new_y2 = max(new_y1 + 1, new_y2)
        
        return [new_x1, new_y1, new_x2, new_y2]
    elif transform_type == "rotate_simple":
        # For simplicity, assume 90-degree rotation
        angle = params.get('angle', 0)
        if angle == 90:
            # Rotate 90 degrees clockwise (from original perspective)
            # Coordinates transform: (x,y) -> (height-y, x)
            new_x1 = height - y2
            new_y1 = x1
            new_x2 = height - y1
            new_y2 = x2
            # Ensure coordinates are within bounds
            # Since rotation with expand changes image dimensions, we need to be careful
            # For 300x300 input rotated 90deg, output is still 300x300 if it's a square
            new_x1, new_x2 = max(0, min(width, new_x1)), max(0, min(width, new_x2))
            new_y1, new_y2 = max(0, min(height, new_y1)), max(0, min(height, new_y2))
            return [min(new_x1, new_x2), min(new_y1, new_y2), max(new_x1, new_x2), max(new_y1, new_y2)]
        elif angle == -90:
            # Rotate 90 degrees counter-clockwise (from original perspective)
            # Coordinates transform: (x,y) -> (y, width-x)
            new_x1 = y1
            new_y1 = width - x2
            new_x2 = y2
            new_y2 = width - x1
            # Ensure coordinates are within bounds
            new_x1, new_x2 = max(0, min(width, new_x1)), max(0, min(width, new_x2))
            new_y1, new_y2 = max(0, min(height, new_y1)), max(0, min(height, new_y2))
            return [min(new_x1, new_x2), min(new_y1, new_y2), max(new_x1, new_x2), max(new_y1, new_y2)]
        else:
            return bbox  # No rotation or unsupported rotation
    
    return bbox

def generate_sample_image_with_bbox():
    """Generate a sample image with a bounding box"""
    import os
    
    # Try to load a sample image from assets folder
    sample_images = [
        "assets/sample_cat.jpg",
        "assets/sample_dog.jpg", 
        "assets/sample_car.jpg",
        "assets/sample_object.jpg"
    ]
    
    # Load first available sample image and resize it
    for img_path in sample_images:
        if os.path.exists(img_path):
            img = Image.open(img_path).convert('RGB')
            # Resize image to fit our needs
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            break
    else:
        # Fallback: Create a simple sample image
        img = Image.new('RGB', (300, 300), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple object (a circle representing a ball)
        draw.ellipse([100, 100, 200, 200], fill='red', outline='black', width=2)
    
    # Define bounding box around the main object (approximate location)
    # For the generated images, we'll put a bounding box around the central object
    bbox = [75, 75, 225, 225]  # Central area of the image
    
    return img, bbox

def show_detection_demo_page():
    st.title("Detection & Segmentation Demo")
    st.write("Simulasi bagaimana bounding box harus berubah saat gambar ditransformasi")
    
    # File uploader for user image
    uploaded_file = st.file_uploader("Upload gambar Anda (opsional)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Use uploaded image
        original_img = Image.open(uploaded_file).convert('RGB')
        # Resize to appropriate size
        original_img = original_img.resize((300, 300), Image.Resampling.LANCZOS)
        # Define a default bounding box in the center
        original_bbox = [75, 75, 225, 225]  # Central area of the 300x300 image
        st.info("Menggunakan gambar yang diupload. Bounding box ditempatkan di tengah gambar.")
    else:
        # Use sample image
        import os
        # Try to load a sample image from assets folder
        sample_images = [
            "assets/sample_cat.jpg",
            "assets/sample_dog.jpg", 
            "assets/sample_car.jpg",
            "assets/sample_object.jpg"
        ]
        
        # Load first available sample image and resize it
        for img_path in sample_images:
            if os.path.exists(img_path):
                original_img = Image.open(img_path).convert('RGB')
                # Resize image to fit our needs
                original_img = original_img.resize((300, 300), Image.Resampling.LANCZOS)
                break
        else:
            # Fallback: Create a simple sample image
            original_img = Image.new('RGB', (300, 300), color='lightblue')
            draw = ImageDraw.Draw(original_img)
            
            # Draw a simple object (a circle representing a ball)
            draw.ellipse([100, 100, 200, 200], fill='red', outline='black', width=2)
        
        # Define bounding box around the main object (approximate location)
        # For the generated images, we'll put a bounding box around the central object
        original_bbox = [75, 75, 225, 225]  # Central area of the image
        
        st.info("Menggunakan gambar contoh karena tidak ada upload. Silakan upload gambar Anda.")
    
    st.subheader("Gambar Asli dengan Bounding Box")
    img_with_bbox = draw_bbox(original_img.copy(), original_bbox)
    st.image(img_with_bbox, caption="Gambar Asli + Bounding Box", width="stretch")
    
    # Transformation options
    st.subheader("Pilih Transformasi")
    transform_type = st.selectbox(
        "Jenis Transformasi",
        ["Shift", "Crop", "Rotate (Simple)"]
    )
    
    # Parameters based on transform type
    params = {}
    if transform_type == "Shift":
        params['offset_x'] = st.slider("Offset X", -50, 50, 0)
        params['offset_y'] = st.slider("Offset Y", -50, 50, 0)
    elif transform_type == "Crop":
        params['crop_left'] = st.slider("Crop Left", 0, 100, 0)
        params['crop_top'] = st.slider("Crop Top", 0, 100, 0)
    elif transform_type == "Rotate (Simple)":
        params['angle'] = st.selectbox("Sudut Rotasi", [0, 90, -90])
    
    # Buttons to demonstrate correct vs wrong approaches
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Demonstrasi Pendekatan BENAR"):
            st.subheader("Hasil: Benar - Bounding Box Ikut Berubah")
            
            # Apply transformation to image
            transformed_img = original_img.copy()
            if transform_type == "Shift":
                # For shift, we just visualize the concept
                shifted_img = Image.new('RGB', (400, 400), color='white')
                offset_x = params['offset_x'] + 50  # Add offset to center in larger canvas
                offset_y = params['offset_y'] + 50
                shifted_img.paste(original_img, (offset_x, offset_y))
                transformed_img = shifted_img
                
                # Transform bbox accordingly
                transformed_bbox = transform_bbox(original_bbox, 'shift', (400, 400), params)  # Updated size for shifted image
                
            elif transform_type == "Crop":
                crop_left = params['crop_left']
                crop_top = params['crop_top']
                transformed_img = original_img.crop((crop_left, crop_top, 300, 300))
                
                # Transform bbox accordingly - adjust coordinates to new image system
                transformed_bbox = transform_bbox(original_bbox, 'crop', (300, 300), params)
                
            elif transform_type == "Rotate (Simple)":
                angle = params['angle']
                if angle == 90:
                    transformed_img = original_img.rotate(-90, expand=True)  # Negative because PIL rotates counter-clockwise by default
                    # Transform bbox with the original image dimensions since rotation transform function expects original size
                    transformed_bbox = transform_bbox(original_bbox, 'rotate_simple', (300, 300), params)
                elif angle == -90:
                    transformed_img = original_img.rotate(90, expand=True)
                    transformed_bbox = transform_bbox(original_bbox, 'rotate_simple', (300, 300), params)
                else:
                    transformed_bbox = original_bbox
            
            # Draw transformed bbox on transformed image
            img_with_transformed_bbox = draw_bbox(transformed_img, transformed_bbox, color='green', thickness=3)
            st.image(img_with_transformed_bbox, caption=f"Gambar Ditransformasi + Bounding Box Disesuaikan", width="stretch")
            
            st.success("Benar: bounding box ikut menyesuaikan transformasi gambar.")
    
    with col2:
        if st.button("Demonstrasi Pendekatan SALAH"):
            st.subheader("Hasil: Salah - Bounding Box Tidak Ikut Berubah")
            
            # Apply transformation to image only
            transformed_img = original_img.copy()
            
            if transform_type == "Shift":
                # For shift, we just visualize the concept
                shifted_img = Image.new('RGB', (400, 400), color='white')
                offset_x = params['offset_x'] + 50  # Add offset to center in larger canvas
                offset_y = params['offset_y'] + 50
                shifted_img.paste(original_img, (offset_x, offset_y))
                transformed_img = shifted_img
                # For the WRONG approach, we use the original bbox without adjustment (this demonstrates the error)
                wrong_bbox = original_bbox[:]
                
            elif transform_type == "Crop":
                crop_left = params['crop_left']
                crop_top = params['crop_top']
                transformed_img = original_img.crop((crop_left, crop_top, 300, 300))
                # For the WRONG approach, we keep the original bbox coordinates (not adjusted for crop)
                # This shows the mistake - the bbox stays in the original coordinates
                # which are now wrong relative to the cropped image
                wrong_bbox = original_bbox[:]
                # The original bbox remains in its original position, but the image content has moved
                # due to cropping, making the bbox misaligned with the actual object
                
            elif transform_type == "Rotate (Simple)":
                angle = params['angle']
                if angle == 90:
                    transformed_img = original_img.rotate(-90, expand=True)  # Negative because PIL rotates counter-clockwise by default
                elif angle == -90:
                    transformed_img = original_img.rotate(90, expand=True)
                # For the WRONG approach, we use the original bbox without transformation
                wrong_bbox = original_bbox[:]
            
            # Draw ORIGINAL bbox on transformed image (wrong approach)
            # In the wrong approach, we simply draw the original bbox on the transformed image
            # This demonstrates the problem where the bbox doesn't match the transformed object
            img_with_original_bbox = draw_bbox(transformed_img, wrong_bbox, color='red', thickness=3)
            st.image(img_with_original_bbox, caption="Gambar Ditransformasi + Bounding Box Tetap", width="stretch")
            
            st.error("Salah: gambar berubah, tetapi bounding box tidak ikut berubah. Ini dapat merusak ground truth dan menurunkan performa model.")
    
    st.markdown("---")
    st.subheader("Konsep Penting")
    st.info("""
    **Pada klasifikasi**, label cukup berupa nama kelas.  
    **Pada object detection dan segmentation**, posisi objek juga bagian dari label.
    
    Saat melakukan augmentation pada data untuk object detection atau segmentation:
    - Gambar harus ditransformasi
    - Bounding box atau mask juga harus ditransformasi dengan cara yang sama
    - Ini memastikan bahwa koordinat objek tetap sesuai dengan posisi barunya setelah transformasi
    """)
    
    st.write("### Contoh Kasus:")
    st.write("- Jika gambar dirotasi 90 derajat, maka bounding box juga harus dirotasi 90 derajat")
    st.write("- Jika gambar dicrop, maka bounding box harus disesuaikan dengan posisi baru")
    st.write("- Jika gambar diresize, maka koordinat bounding box harus diskalakan sesuai")