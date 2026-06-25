import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def generate_sample_images():
    """Generate two distinct sample images"""
    import os
    
    # Try to load sample images from assets folder
    sample_images = [
        "assets/sample_cat.jpg",
        "assets/sample_dog.jpg", 
        "assets/sample_car.jpg",
        "assets/sample_object.jpg"
    ]
    
    # Load two different sample images if available
    if len(sample_images) >= 2 and all(os.path.exists(img) for img in sample_images[:2]):
        img_a = Image.open(sample_images[0]).convert('RGB').resize((200, 200), Image.Resampling.LANCZOS)
        img_b = Image.open(sample_images[1]).convert('RGB').resize((200, 200), Image.Resampling.LANCZOS)
        return img_a, img_b
    else:
        # Fallback: Create simple sample images
        # Image A - Blue square
        img_a = Image.new('RGB', (200, 200), color='lightblue')
        draw_a = ImageDraw.Draw(img_a)
        draw_a.rectangle([50, 50, 150, 150], fill='darkblue', outline='black', width=2)
        
        # Image B - Red circle
        img_b = Image.new('RGB', (200, 200), color='lightcoral')
        draw_b = ImageDraw.Draw(img_b)
        draw_b.ellipse([50, 50, 150, 150], fill='darkred', outline='black', width=2)
        
        return img_a, img_b

def apply_mixup(img1, img2, alpha=0.5):
    """Apply Mixup augmentation"""
    # Convert to numpy arrays
    arr1 = np.array(img1).astype(np.float32) / 255.0
    arr2 = np.array(img2).astype(np.float32) / 255.0
    
    # Apply mixup
    mixed = alpha * arr1 + (1 - alpha) * arr2
    
    # Convert back to image
    mixed = np.clip(mixed, 0, 1)
    mixed = (mixed * 255).astype(np.uint8)
    
    return Image.fromarray(mixed)

def apply_cutmix(img1, img2, alpha=0.5):
    """Apply CutMix augmentation"""
    # Convert to numpy arrays
    arr1 = np.array(img1).astype(np.uint8)
    arr2 = np.array(img2).astype(np.uint8)
    
    # Calculate the size of the patch based on alpha
    h, w = arr1.shape[:2]
    cut_ratio = np.sqrt(1. - alpha)
    cut_h = int(h * cut_ratio)
    cut_w = int(w * cut_ratio)
    
    # Randomly select the center of the patch
    cy = np.random.randint(h)
    cx = np.random.randint(w)
    
    # Calculate the corner coordinates of the patch
    y1 = np.clip(cy - cut_h // 2, 0, h)
    y2 = np.clip(cy + cut_h // 2, 0, h)
    x1 = np.clip(cx - cut_w // 2, 0, w)
    x2 = np.clip(cx + cut_w // 2, 0, w)
    
    # Create the CutMix image
    arr_result = arr1.copy()
    arr_result[y1:y2, x1:x2] = arr2[y1:y2, x1:x2]
    
    return Image.fromarray(arr_result)

def show_mixup_cutmix_page():
    st.title("Mixup & CutMix")
    st.write("Simulasi teknik augmentation modern yang menggabungkan dua sampel")
    
    # File uploaders for user images
    st.subheader("Upload Gambar Anda")
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_img_a = st.file_uploader("Upload Image A", type=["jpg", "jpeg", "png"], key="img_a")
    
    with col2:
        uploaded_img_b = st.file_uploader("Upload Image B", type=["jpg", "jpeg", "png"], key="img_b")
    
    # Use uploaded images or generate samples
    if uploaded_img_a is not None and uploaded_img_b is not None:
        img_a = Image.open(uploaded_img_a).convert('RGB').resize((200, 200), Image.Resampling.LANCZOS)
        img_b = Image.open(uploaded_img_b).convert('RGB').resize((200, 200), Image.Resampling.LANCZOS)
        st.info("Menggunakan gambar yang diupload.")
    else:
        # Generate sample images
        img_a, img_b = generate_sample_images()
        if uploaded_img_a is None and uploaded_img_b is None:
            st.info("Menggunakan gambar contoh karena tidak ada upload. Silakan upload dua gambar Anda.")
        elif uploaded_img_a is None:
            st.info("Image A menggunakan gambar contoh. Silakan upload Image A.")
        elif uploaded_img_b is None:
            st.info("Image B menggunakan gambar contoh. Silakan upload Image B.")
    
    st.subheader("Gambar Input")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(img_a, caption="Image A", width="stretch")
    
    with col2:
        st.image(img_b, caption="Image B", width="stretch")
    
    st.subheader("Pilih Teknik Augmentation")
    technique = st.radio(
        "Teknik",
        ["Mixup", "CutMix"]
    )
    
    # Alpha/ratio slider
    alpha = st.slider(
        "Rasio Image A (Image B = 100% - Rasio Image A)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05
    )
    
    # Apply selected technique
    if technique == "Mixup":
        result_img = apply_mixup(img_a, img_b, alpha)
        st.subheader("Hasil Mixup")
        st.image(result_img, caption=f"Mixed Image ({alpha:.0%} Image A + {1-alpha:.0%} Image B)", width="stretch")
        
        st.info(f"""
        **Label:** {alpha:.0%} Square + {1-alpha:.0%} Circle
        
        **Penjelasan:** Mixup mencampur dua gambar dan dua label secara proporsional. 
        Teknik ini membantu model belajar decision boundary yang lebih halus.
        """)
    
    elif technique == "CutMix":
        result_img = apply_cutmix(img_a, img_b, alpha)
        st.subheader("Hasil CutMix")
        st.image(result_img, caption=f"CutMix Image ({alpha:.0%} Image A + {1-alpha:.0%} Image B)", width="stretch")
        
        st.info(f"""
        **Label:** {alpha:.0%} Image A + {1-alpha:.0%} Image B
        
        **Penjelasan:** CutMix menempel bagian gambar lain ke gambar utama. 
        Label disesuaikan berdasarkan proporsi area patch.
        """)
    
    st.markdown("---")
    st.subheader("Perbandingan Teknik")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Mixup**")
        st.write("- Mencampur dua gambar secara transparan")
        st.write("- Menggunakan interpolasi linear antara dua gambar")
        st.write("- Label juga diinterpolasi")
        st.write("- Cocok untuk meningkatkan generalisasi")
    
    with col2:
        st.write("**CutMix**")
        st.write("- Menempel bagian gambar lain ke gambar utama")
        st.write("- Menggunakan patch rectangular dari gambar kedua")
        st.write("- Label berdasarkan proporsi area patch")
        st.write("- Cocok untuk mencegah overfitting")
    
    st.write("")
    st.write("**Kapan menggunakan masing-masing teknik?**")
    st.write("- **Mixup**: Ketika ingin membuat representasi kontinu antara dua kelas")
    st.write("- **CutMix**: Ketika ingin mempertahankan elemen diskrit dari kedua gambar")
    
    st.markdown("---")
    st.subheader("Konsep Penting")
    st.info("""
    **Mixup dan CutMix adalah teknik augmentation lanjutan yang:**
    
    - Menggabungkan informasi dari dua contoh berbeda
    - Membantu model belajar hubungan antar kelas
    - Mengurangi overfitting dengan membuat data latih lebih bervariasi
    - Memerlukan modifikasi label yang sesuai dengan kombinasi gambar
    """)
    
    st.warning("""
    **Catatan penting:** Pada teknik ini, label tidak hanya bergantung pada gambar,
    tetapi juga pada proporsi kontribusi masing-masing gambar dalam hasil augmentasi.
    """)