import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import os

def apply_augmentation(image, technique, params):
    """Apply selected augmentation technique to the image"""
    img_array = np.array(image)
    
    if technique == "Horizontal Flip":
        return cv2.flip(img_array, 1)
    elif technique == "Rotation":
        angle = params.get('rotation_angle', 0)
        center = (img_array.shape[1] // 2, img_array.shape[0] // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(img_array, rotation_matrix, (img_array.shape[1], img_array.shape[0]))
    elif technique == "Crop":
        height, width = img_array.shape[:2]
        crop_percent = params.get('crop_percent', 0.8)
        crop_h = int(height * crop_percent)
        crop_w = int(width * crop_percent)
        start_y = (height - crop_h) // 2
        start_x = (width - crop_w) // 2
        return img_array[start_y:start_y+crop_h, start_x:start_x+crop_w]
    elif technique == "Zoom":
        scale_factor = params.get('zoom_factor', 1.0)
        height, width = img_array.shape[:2]
        new_height, new_width = int(height * scale_factor), int(width * scale_factor)
        
        # Resize the image
        zoomed_img = cv2.resize(img_array, (new_width, new_height))
        
        # Center crop to original size
        start_y = (new_height - height) // 2
        start_x = (new_width - width) // 2
        return zoomed_img[start_y:start_y+height, start_x:start_x+width]
    elif technique == "Brightness":
        factor = params.get('brightness_factor', 1.0)
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * factor, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    elif technique == "Contrast":
        factor = params.get('contrast_factor', 1.0)
        img_array = img_array.astype(np.float64)
        mean = np.mean(img_array, axis=(0, 1), keepdims=True)
        adjusted = (img_array - mean) * factor + mean
        return np.clip(adjusted, 0, 255).astype(np.uint8)
    elif technique == "Blur":
        kernel_size = int(params.get('blur_kernel', 1))
        if kernel_size % 2 == 0:
            kernel_size += 1  # Ensure odd kernel size
        kernel_size = max(1, kernel_size)
        return cv2.GaussianBlur(img_array, (kernel_size, kernel_size), 0)
    elif technique == "Noise Injection":
        noise_factor = params.get('noise_factor', 0.0)
        noise = np.random.normal(0, noise_factor, img_array.shape)
        noisy_image = img_array + noise
        return np.clip(noisy_image, 0, 255).astype(np.uint8)
    
    return img_array

def apply_cutout(image, size, random_position=True):
    """Apply Cutout augmentation to the image"""
    img_array = np.array(image).copy()
    h, w = img_array.shape[:2]
    
    # Calculate cutout size
    cutout_h = int(h * size)
    cutout_w = int(w * size)
    
    if random_position:
        # Random position
        y = np.random.randint(0, h - cutout_h)
        x = np.random.randint(0, w - cutout_w)
    else:
        # Center position
        y = (h - cutout_h) // 2
        x = (w - cutout_w) // 2
    
    # Apply cutout (fill with zeros - black)
    img_array[y:y+cutout_h, x:x+cutout_w] = 0
    
    return Image.fromarray(img_array)

def apply_gridmask(image, grid_size, mask_ratio):
    """Apply GridMask augmentation to the image"""
    img_array = np.array(image).copy()
    h, w = img_array.shape[:2]
    
    # Calculate grid cell size
    cell_h = grid_size
    cell_w = grid_size
    
    # Calculate unmasked region size within each cell
    unmask_h = int(cell_h * (1 - mask_ratio))
    unmask_w = int(cell_w * (1 - mask_ratio))
    
    # Start position for unmasked regions
    start_h = (cell_h - unmask_h) // 2
    start_w = (cell_w - unmask_w) // 2
    
    # Create mask
    for i in range(0, h, cell_h):
        for j in range(0, w, cell_w):
            # Calculate the actual unmasked region in this cell
            end_i = min(i + start_h, h)
            end_j = min(j + start_w, w)
            end_i2 = min(i + start_h + unmask_h, h)
            end_j2 = min(j + start_w + unmask_w, w)
            
            # Keep unmasked region, mask the rest
            if len(img_array.shape) == 3:
                img_array[i:i+cell_h, j:j+cell_w] = 0  # Mask entire cell
                # Then unmask the specific region
                if end_i2 > end_i and end_j2 > end_j:
                    img_array[end_i:end_i2, end_j:end_j2] = np.array(image)[end_i:end_i2, end_j:end_j2]
            else:
                img_array[i:i+cell_h, j:j+cell_w] = 0  # Mask entire cell
                if end_i2 > end_i and end_j2 > end_j:
                    img_array[end_i:end_i2, end_j:end_j2] = np.array(image)[end_i:end_i2, end_j:end_j2]
    
    # More effective GridMask implementation
    img_array = np.array(image).copy()
    h, w = img_array.shape[:2]
    
    # Create a pattern mask
    mask = np.ones((h, w), dtype=bool)
    
    # Calculate the number of cells
    n_cells_h = h // grid_size
    n_cells_w = w // grid_size
    
    for i in range(n_cells_h):
        for j in range(n_cells_w):
            # Calculate the start position of the cell
            start_h = i * grid_size
            start_w = j * grid_size
            
            # Calculate the unmasked region within the cell
            unmask_start_h = start_h + int(grid_size * mask_ratio / 2)
            unmask_end_h = start_h + grid_size - int(grid_size * mask_ratio / 2)
            unmask_start_w = start_w + int(grid_size * mask_ratio / 2)
            unmask_end_w = start_w + grid_size - int(grid_size * mask_ratio / 2)
            
            # Mark the unmasked region as False (so it won't be masked)
            mask[unmask_start_h:unmask_end_h, unmask_start_w:unmask_end_w] = False
    
    # Apply the mask to the image
    if len(img_array.shape) == 3:
        for c in range(img_array.shape[2]):
            img_array[mask, c] = 0
    else:
        img_array[mask] = 0
    
    return Image.fromarray(img_array)

def create_mosaic(images):
    """Create mosaic from 4 images"""
    # Resize all images to the same size
    target_size = (200, 200)
    resized_images = []
    
    for img in images:
        if isinstance(img, str):
            # If it's a file path, load the image
            img = Image.open(img).convert('RGB')
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
        resized_images.append(resized_img)
    
    # Create a canvas for the mosaic (2x2 arrangement)
    mosaic_img = Image.new('RGB', (target_size[0]*2, target_size[1]*2), color='white')
    
    # Paste the four images in the quadrants
    mosaic_img.paste(resized_images[0], (0, 0))  # Top-left
    mosaic_img.paste(resized_images[1], (target_size[0], 0))  # Top-right
    mosaic_img.paste(resized_images[2], (0, target_size[1]))  # Bottom-left
    mosaic_img.paste(resized_images[3], (target_size[0], target_size[1]))  # Bottom-right
    
    return mosaic_img

def apply_copy_paste(background, source, patch_size, x_pos, y_pos):
    """Apply Copy-Paste augmentation"""
    bg_array = np.array(background).copy()
    src_array = np.array(source).copy()
    
    h, w = bg_array.shape[:2]
    
    # Calculate patch dimensions
    patch_h = int(h * patch_size)
    patch_w = int(w * patch_size)
    
    # Resize source patch to desired size
    src_resized = cv2.resize(src_array, (patch_w, patch_h))
    
    # Calculate paste position
    paste_y = min(max(y_pos, 0), h - patch_h)
    paste_x = min(max(x_pos, 0), w - patch_w)
    
    # Paste the source patch onto the background
    bg_array[paste_y:paste_y+patch_h, paste_x:paste_x+patch_w] = src_resized
    
    return Image.fromarray(bg_array)

def get_sample_images():
    """Provide sample images if user doesn't upload"""
    import os
    from PIL import Image as PILImage
    
    # Try to load sample images from assets folder
    sample_images = [
        "assets/sample_cat.jpg",
        "assets/sample_dog.jpg", 
        "assets/sample_car.jpg",
        "assets/sample_object.jpg"
    ]
    
    # Return first available sample image
    for img_path in sample_images:
        if os.path.exists(img_path):
            return PILImage.open(img_path).convert('RGB')
    
    # Fallback: Create a simple sample image
    sample_img = np.zeros((200, 200, 3), dtype=np.uint8)
    sample_img[50:150, 50:150] = [255, 100, 100]  # Red square
    sample_img[75:125, 75:125] = [100, 255, 100]  # Green square inside
    return Image.fromarray(sample_img)

def show_image_augmentation_page():
    st.title("Image Augmentation")
    st.write("Coba berbagai teknik augmentasi gambar dan lihat perbedaannya")
    
    # Create tabs for different augmentation types
    tabs = st.tabs(["Basic", "Cutout", "GridMask", "Mosaic", "Copy-Paste"])
    
    with tabs[0]:
        st.subheader("Basic Image Augmentation")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload gambar Anda", type=["jpg", "jpeg", "png"], key="basic_upload")
        
        # Use uploaded image or sample
        if uploaded_file is not None:
            original_image = Image.open(uploaded_file)
        else:
            original_image = get_sample_images()
            st.info("Menggunakan gambar contoh karena tidak ada upload. Silakan upload gambar Anda.")
        
        # Convert to RGB if needed
        if original_image.mode != 'RGB':
            original_image = original_image.convert('RGB')
        
        # Display original image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gambar Asli")
            st.image(original_image, caption="Gambar Input", width="stretch")
        
        # Augmentation controls
        st.subheader("Pengaturan Augmentation")
        technique = st.selectbox(
            "Pilih teknik augmentation",
            [
                "Horizontal Flip",
                "Rotation",
                "Crop",
                "Zoom",
                "Brightness",
                "Contrast",
                "Blur",
                "Noise Injection"
            ],
            key="basic_technique"
        )
        
        # Define parameters based on technique
        params = {}
        if technique == "Rotation":
            params['rotation_angle'] = st.slider("Sudut Rotasi (derajat)", -45, 45, 0, key="basic_rotation")
        elif technique == "Crop":
            params['crop_percent'] = st.slider("Persentase Crop", 0.5, 1.0, 0.8, key="basic_crop")
        elif technique == "Zoom":
            params['zoom_factor'] = st.slider("Faktor Zoom", 1.0, 3.0, 1.0, key="basic_zoom")
        elif technique == "Brightness":
            params['brightness_factor'] = st.slider("Faktor Kecerahan", 0.5, 1.5, 1.0, key="basic_brightness")
        elif technique == "Contrast":
            params['contrast_factor'] = st.slider("Faktor Kontras", 0.5, 1.5, 1.0, key="basic_contrast")
        elif technique == "Blur":
            params['blur_kernel'] = st.slider("Kernel Blur", 1, 15, 1, key="basic_blur")
        elif technique == "Noise Injection":
            params['noise_factor'] = st.slider("Faktor Noise", 0, 50, 0, key="basic_noise")
        
        # Apply augmentation
        augmented_image = apply_augmentation(original_image, technique, params)
        
        with col2:
            st.subheader("Gambar Hasil Augmentation")
            st.image(augmented_image, caption=f"{technique} Result", width="stretch")
        
        # Explanation
        st.subheader("Penjelasan")
        
        # Determine risk level
        risk_level = "Aman"
        risk_msg = "Transformasi ini umumnya tidak mengubah makna utama objek."
        
        if technique in ["Rotation", "Horizontal Flip"]:
            if abs(params.get('rotation_angle', 0)) > 30:
                risk_level = "Hati-hati"
                risk_msg = "Rotasi terlalu ekstrem dapat mengubah orientasi objek dan mengganggu interpretasi."
        elif technique == "Crop":
            if params.get('crop_percent', 0.8) < 0.6:
                risk_level = "Hati-hati"
                risk_msg = "Crop terlalu besar dapat menghilangkan informasi penting dari objek."
        elif technique == "Zoom":
            if params.get('zoom_factor', 1.0) > 2.0:
                risk_level = "Hati-hati"
                risk_msg = "Zoom terlalu besar dapat menyebabkan distorsi dan kehilangan detail."
        elif technique == "Blur":
            if params.get('blur_kernel', 1) > 7:
                risk_level = "Hati-hati"
                risk_msg = "Blur terlalu tinggi dapat mengaburkan fitur penting objek."
        elif technique == "Noise Injection":
            if params.get('noise_factor', 0) > 30:
                risk_level = "Hati-hati"
                risk_msg = "Noise terlalu tinggi dapat menutupi fitur penting dari objek."
        
        # Display risk assessment
        if risk_level == "Aman":
            st.success(f"Label Status: {risk_level}")
            st.write(risk_msg)
        else:
            st.warning(f"Label Status: {risk_level}")
            st.write(risk_msg)
        
        # Technique explanation
        explanations = {
            "Horizontal Flip": "Membalik gambar secara horizontal. Teknik ini umum digunakan untuk data augmentation karena banyak objek simetris horizontal.",
            "Rotation": "Memutar gambar dengan sudut tertentu. Berguna untuk membuat model robust terhadap variasi orientasi.",
            "Crop": "Memotong bagian dari gambar. Dapat digunakan untuk fokus pada bagian tertentu atau membuat variasi lokasi.",
            "Zoom": "Memperbesar gambar. Membantu model belajar untuk mengenali objek dalam berbagai ukuran.",
            "Brightness": "Mengubah kecerahan gambar. Membantu model beradaptasi dengan kondisi pencahayaan yang berbeda.",
            "Contrast": "Mengubah kontras gambar. Membantu model beradaptasi dengan variasi kontras.",
            "Blur": "Memberikan efek blur pada gambar. Membantu model menjadi lebih robust terhadap gambar yang sedikit kabur.",
            "Noise Injection": "Menambahkan noise acak ke gambar. Membantu model menjadi lebih robust terhadap noise."
        }
        
        st.info(f"**Penjelasan Teknik:** {explanations[technique]}")
        
        # Show differences
        st.subheader("Perbedaan yang Terjadi")
        st.write("- Apa yang berubah: ", technique)
        st.write("- Apakah label masih valid: Ya, selama objek utama masih dapat dikenali")
        st.write("- Kapan teknik ini cocok digunakan: Untuk meningkatkan robustness model terhadap variasi yang realistis")
    
    with tabs[1]:
        st.subheader("Cutout Augmentation")
        st.write("Cutout menutup sebagian area gambar dengan kotak kosong. Teknik ini membantu model belajar fitur penting dari objek, bukan hanya mengandalkan satu bagian visual tertentu.")
        
        # Demo example for Cutout
        st.subheader("Contoh Sebelum & Sesudah")
        demo_img = get_sample_images()
        demo_cutout = apply_cutout(demo_img, 0.2, True)
        
        col_demo1, col_demo2 = st.columns(2)
        with col_demo1:
            st.image(demo_img, caption="Gambar Asli", width="stretch")
        with col_demo2:
            st.image(demo_cutout, caption="Hasil Cutout", width="stretch")
        
        # File uploader for Cutout
        uploaded_file_cutout = st.file_uploader("Upload gambar Anda", type=["jpg", "jpeg", "png"], key="cutout_upload_user")
        
        # Use uploaded image or sample for Cutout
        if uploaded_file_cutout is not None:
            original_image_cutout = Image.open(uploaded_file_cutout)
        else:
            original_image_cutout = get_sample_images()
            st.info("Menggunakan gambar contoh karena tidak ada upload. Silakan upload gambar Anda.")
        
        # Convert to RGB if needed
        if original_image_cutout.mode != 'RGB':
            original_image_cutout = original_image_cutout.convert('RGB')
        
        # Cutout controls
        st.subheader("Pengaturan Cutout")
        cutout_size = st.slider("Ukuran Cutout (persentase)", 0.1, 0.5, 0.2, key="cutout_size_user")
        random_position = st.checkbox("Posisi Acak", True, key="cutout_random_user")
        
        if st.button("Generate Cutout", key="cutout_button_user"):
            cutout_result = apply_cutout(original_image_cutout, cutout_size, random_position)
            
            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.image(original_image_cutout, caption="Gambar Asli", width="stretch")
            with col2:
                st.image(cutout_result, caption="Hasil Cutout", width="stretch")
            
            # Risk assessment for Cutout
            if cutout_size > 0.3:
                st.warning("Label Status: Hati-hati")
                st.write("Ukuran cutout terlalu besar dapat menyembunyikan informasi penting dari objek.")
            else:
                st.success("Label Status: Aman")
                st.write("Cutout dengan ukuran ini masih memungkinkan untuk mengenali objek utama.")
            
            st.info("**Penjelasan Teknik:** Cutout menutup sebagian area gambar dengan kotak kosong. Teknik ini membantu model belajar fitur penting dari objek, bukan hanya mengandalkan satu bagian visual tertentu.")
    
    with tabs[2]:
        st.subheader("GridMask Augmentation")
        st.write("GridMask menghapus bagian gambar menggunakan pola grid. Teknik ini membuat model lebih robust karena model tidak boleh bergantung hanya pada area visual tertentu.")
        
        # Demo example for GridMask
        st.subheader("Contoh Sebelum & Sesudah")
        demo_img_grid = get_sample_images()
        demo_gridmask = apply_gridmask(demo_img_grid, 30, 0.5)
        
        col_demo1, col_demo2 = st.columns(2)
        with col_demo1:
            st.image(demo_img_grid, caption="Gambar Asli", width="stretch")
        with col_demo2:
            st.image(demo_gridmask, caption="Hasil GridMask", width="stretch")
        
        # File uploader for GridMask
        uploaded_file_grid = st.file_uploader("Upload gambar Anda", type=["jpg", "jpeg", "png"], key="gridmask_upload_user")
        
        # Use uploaded image or sample for GridMask
        if uploaded_file_grid is not None:
            original_image_grid = Image.open(uploaded_file_grid)
        else:
            original_image_grid = get_sample_images()
            st.info("Menggunakan gambar contoh karena tidak ada upload. Silakan upload gambar Anda.")
        
        # Convert to RGB if needed
        if original_image_grid.mode != 'RGB':
            original_image_grid = original_image_grid.convert('RGB')
        
        # GridMask controls
        st.subheader("Pengaturan GridMask")
        grid_size = st.slider("Ukuran Grid", 10, 100, 30, key="grid_size_user")
        mask_ratio = st.slider("Rasio Mask", 0.1, 0.8, 0.5, key="mask_ratio_user")
        
        if st.button("Apply GridMask", key="gridmask_button_user"):
            gridmask_result = apply_gridmask(original_image_grid, grid_size, mask_ratio)
            
            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.image(original_image_grid, caption="Gambar Asli", width="stretch")
            with col2:
                st.image(gridmask_result, caption="Hasil GridMask", width="stretch")
            
            # Risk assessment for GridMask
            if mask_ratio > 0.6:
                st.warning("Label Status: Hati-hati")
                st.write("Rasio mask terlalu besar dapat menyembunyikan terlalu banyak informasi dari objek.")
            else:
                st.success("Label Status: Aman")
                st.write("GridMask dengan rasio ini masih memungkinkan untuk mengenali objek utama.")
            
            st.info("**Penjelasan Teknik:** GridMask menghapus bagian gambar menggunakan pola grid. Teknik ini membuat model lebih robust karena model tidak boleh bergantung hanya pada area visual tertentu.")
    
    with tabs[3]:
        st.subheader("Mosaic Augmentation")
        st.write("Mosaic menggabungkan empat gambar menjadi satu gambar baru. Teknik ini sering digunakan pada object detection karena model dapat belajar dari beberapa objek dan konteks sekaligus.")
        
        # Demo example for Mosaic
        st.subheader("Contoh Sebelum & Sesudah")
        demo_images = [get_sample_images() for _ in range(4)]
        demo_mosaic = create_mosaic(demo_images)
        
        st.write("Gambar Input:")
        cols = st.columns(4)
        for i, img in enumerate(demo_images):
            cols[i].image(img, caption=f"Image {i+1}", width="stretch")
        
        st.write("Hasil Mosaic:")
        st.image(demo_mosaic, caption="Mosaic Result", width="stretch")
        
        # File uploaders for Mosaic
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            uploaded_img1 = st.file_uploader("Upload Image 1", type=["jpg", "jpeg", "png"], key="mosaic_img1_user")
        with col2:
            uploaded_img2 = st.file_uploader("Upload Image 2", type=["jpg", "jpeg", "png"], key="mosaic_img2_user")
        with col3:
            uploaded_img3 = st.file_uploader("Upload Image 3", type=["jpg", "jpeg", "png"], key="mosaic_img3_user")
        with col4:
            uploaded_img4 = st.file_uploader("Upload Image 4", type=["jpg", "jpeg", "png"], key="mosaic_img4_user")
        
        # Prepare images for mosaic
        sample_images = [
            "assets/sample_cat.jpg",
            "assets/sample_dog.jpg", 
            "assets/sample_car.jpg",
            "assets/sample_object.jpg"
        ]
        
        images = []
        upload_count = sum(x is not None for x in [uploaded_img1, uploaded_img2, uploaded_img3, uploaded_img4])
        
        # Use uploaded images or sample/fallback images
        for i, uploaded_img in enumerate([uploaded_img1, uploaded_img2, uploaded_img3, uploaded_img4]):
            if uploaded_img is not None:
                img = Image.open(uploaded_img).convert('RGB')
                images.append(img)
            else:
                # Try to load sample image or create fallback
                if i < len(sample_images) and os.path.exists(sample_images[i]):
                    img = Image.open(sample_images[i]).convert('RGB')
                    images.append(img)
                else:
                    # Create a simple fallback image
                    fallback_img = Image.new('RGB', (200, 200), color=('red' if i == 0 else 'blue' if i == 1 else 'green' if i == 2 else 'yellow'))
                    images.append(fallback_img)
        
        if upload_count < 4:
            st.info(f"Menggunakan {4-upload_count} gambar contoh karena tidak semua gambar diupload. Silakan upload semua gambar.")
        
        if st.button("Generate Mosaic", key="mosaic_button_user"):
            mosaic_result = create_mosaic(images)
            
            # Display results
            st.subheader("Gambar Input")
            cols = st.columns(4)
            for i, img in enumerate(images):
                cols[i].image(img, caption=f"Image {i+1}", width="stretch")
            
            st.subheader("Hasil Mosaic")
            st.image(mosaic_result, caption="Mosaic Result", width="stretch")
            
            # Risk assessment for Mosaic
            st.info("Label Status: Tergantung tugas")
            st.write("Pada klasifikasi, label tunggal bisa membingungkan. Pada deteksi objek, setiap objek harus memiliki bounding box masing-masing.")
            
            st.info("**Penjelasan Teknik:** Mosaic menggabungkan empat gambar menjadi satu gambar baru. Teknik ini sering digunakan pada object detection karena model dapat belajar dari beberapa objek dan konteks sekaligus.")
    
    with tabs[4]:
        st.subheader("Copy-Paste Augmentation")
        st.write("Copy-Paste mengambil bagian dari satu gambar lalu menempelkannya ke gambar lain. Teknik ini dapat membantu model belajar objek dalam konteks background yang lebih beragam.")
        
        # Demo example for Copy-Paste
        st.subheader("Contoh Sebelum & Sesudah")
        demo_bg = get_sample_images()
        demo_src = get_sample_images()
        demo_copypaste = apply_copy_paste(demo_bg, demo_src, 0.2, 50, 50)
        
        cols_demo = st.columns(3)
        with cols_demo[0]:
            st.image(demo_bg, caption="Background Image", width="stretch")
        with cols_demo[1]:
            st.image(demo_src, caption="Source Image", width="stretch")
        with cols_demo[2]:
            st.image(demo_copypaste, caption="Hasil Copy-Paste", width="stretch")
        
        # File uploaders for Copy-Paste
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_bg = st.file_uploader("Upload Background Image", type=["jpg", "jpeg", "png"], key="copypaste_bg_user")
        with col2:
            uploaded_src = st.file_uploader("Upload Source Image", type=["jpg", "jpeg", "png"], key="copypaste_src_user")
        
        # Prepare background and source images
        sample_images = [
            "assets/sample_cat.jpg",
            "assets/sample_dog.jpg"
        ]
        
        # Use uploaded images or sample/fallback images
        if uploaded_bg is not None:
            background_img = Image.open(uploaded_bg).convert('RGB')
        else:
            if os.path.exists(sample_images[0]):
                background_img = Image.open(sample_images[0]).convert('RGB')
            else:
                background_img = Image.new('RGB', (200, 200), color='lightblue')
            st.info("Menggunakan gambar contoh sebagai background karena tidak ada upload.")
        
        if uploaded_src is not None:
            source_img = Image.open(uploaded_src).convert('RGB')
        else:
            if len(sample_images) > 1 and os.path.exists(sample_images[1]):
                source_img = Image.open(sample_images[1]).convert('RGB')
            else:
                source_img = Image.new('RGB', (200, 200), color='lightcoral')
            st.info("Menggunakan gambar contoh sebagai source karena tidak ada upload.")
        
        # Copy-Paste controls
        st.subheader("Pengaturan Copy-Paste")
        patch_size = st.slider("Ukuran Patch", 0.1, 0.5, 0.2, key="copypaste_size_user")
        x_pos = st.slider("Posisi Tempel X", 0, 200, 50, key="copypaste_x_user")
        y_pos = st.slider("Posisi Tempel Y", 0, 200, 50, key="copypaste_y_user")
        
        if st.button("Apply Copy-Paste", key="copypaste_button_user"):
            copypaste_result = apply_copy_paste(background_img, source_img, patch_size, x_pos, y_pos)
            
            # Display results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(background_img, caption="Background Image", width="stretch")
            with col2:
                st.image(source_img, caption="Source Image", width="stretch")
            with col3:
                st.image(copypaste_result, caption="Hasil Copy-Paste", width="stretch")
            
            # Risk assessment for Copy-Paste
            st.warning("Label Status: Perlu hati-hati")
            st.write("Jika digunakan untuk deteksi atau segmentasi, label objek dan posisi harus ikut diperbarui.")
            
            st.info("**Penjelasan Teknik:** Copy-Paste mengambil bagian dari satu gambar lalu menempelkannya ke gambar lain. Teknik ini dapat membantu model belajar objek dalam konteks background yang lebih beragam.")