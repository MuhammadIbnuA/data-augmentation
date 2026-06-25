import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def generate_signal(length=200, freq=1):
    """Generate a basic time series signal"""
    x = np.linspace(0, 10, length)
    y = np.sin(freq * x) + 0.5 * np.sin(3 * freq * x)
    return x, y

def apply_jittering(signal, noise_factor=0.02):
    """Apply jittering (add small noise)"""
    noise = np.random.normal(scale=noise_factor, size=signal.shape)
    return signal + noise

def apply_scaling(signal, scale_factor=1.2):
    """Apply scaling"""
    return signal * scale_factor

def apply_cropping(signal, crop_start=20, crop_length=160):
    """Apply cropping"""
    if crop_length > len(signal):
        crop_length = len(signal)
    return signal[crop_start:crop_start + crop_length]

def apply_time_warping(signal, warp_factor=1.1):
    """Apply simple time warping simulation"""
    # This is a simplified version - real time warping is more complex
    # For demonstration, we'll resample the signal
    original_len = len(signal)
    new_len = int(original_len / warp_factor)
    
    # Resample using interpolation
    x_original = np.linspace(0, 1, original_len)
    x_new = np.linspace(0, 1, new_len)
    
    # Linear interpolation
    warped_signal = np.interp(x_new, x_original, signal)
    
    # Pad or truncate to original length
    result = np.zeros(original_len)
    if len(warped_signal) <= original_len:
        result[:len(warped_signal)] = warped_signal
    else:
        result = warped_signal[:original_len]
    
    return result

def show_timeseries_demo_page():
    st.title("Audio / Time-Series Demo")
    st.write("Simulasi augmentation pada data sinyal, audio, sensor, dan time-series")
    
    # Generate original signal
    x, original_signal = generate_signal()
    
    # Plot original signal
    st.subheader("Sinyal Asli")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, original_signal, label='Original Signal', linewidth=2)
    ax.set_title('Original Time Series Signal')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    
    # Select augmentation technique
    st.subheader("Pilih Teknik Augmentation")
    technique = st.selectbox(
        "Teknik",
        [
            "Jittering",
            "Scaling",
            "Cropping",
            "Time Warping"
        ]
    )
    
    # Apply augmentation based on selection
    augmented_signal = original_signal.copy()
    
    if technique == "Jittering":
        noise_factor = st.slider("Faktor Noise", 0.0, 0.1, 0.02, step=0.01)
        augmented_signal = apply_jittering(original_signal, noise_factor)
        
        # Adjust x-axis for plotting
        plot_x = x
        title = f'Jittering (Noise Factor: {noise_factor})'
        
    elif technique == "Scaling":
        scale_factor = st.slider("Faktor Skala", 0.5, 2.0, 1.2, step=0.1)
        augmented_signal = apply_scaling(original_signal, scale_factor)
        
        plot_x = x
        title = f'Scaling (Factor: {scale_factor})'
        
    elif technique == "Cropping":
        crop_start = st.slider("Titik Awal Crop", 0, 50, 20)
        crop_length = st.slider("Panjang Crop", 100, 180, 160)
        augmented_signal = apply_cropping(original_signal, crop_start, crop_length)
        
        # Adjust x-axis for cropped signal
        plot_x = x[crop_start:crop_start + crop_length]
        title = f'Cropping (Start: {crop_start}, Length: {crop_length})'
        
    elif technique == "Time Warping":
        warp_factor = st.slider("Faktor Warp", 0.8, 1.3, 1.1, step=0.1)
        augmented_signal = apply_time_warping(original_signal, warp_factor)
        
        plot_x = x
        title = f'Time Warping (Factor: {warp_factor})'
    
    # Plot augmented signal
    st.subheader("Sinyal Hasil Augmentation")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(plot_x, augmented_signal, label=title, color='orange', linewidth=2)
    ax.set_title(f'Augmented Signal - {technique}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    
    # Show both signals for comparison
    st.subheader("Perbandingan")
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plot both signals
    ax.plot(x, original_signal, label='Original Signal', linewidth=2)
    
    # Handle different lengths for cropping
    if len(augmented_signal) != len(original_signal):
        if technique == "Cropping":
            crop_start = st.slider("Titik Awal Crop", 0, 50, 20, key="compare_crop_start")
            crop_length = st.slider("Panjang Crop", 100, 180, 160, key="compare_crop_length")
            aug_plot_x = x[crop_start:crop_start + crop_length]
            ax.plot(aug_plot_x, augmented_signal, label='Augmented Signal', linewidth=2)
        else:
            # For other techniques, plot up to the minimum length
            min_len = min(len(original_signal), len(augmented_signal))
            ax.plot(x[:min_len], augmented_signal[:min_len], label='Augmented Signal', linewidth=2)
    else:
        ax.plot(plot_x, augmented_signal, label='Augmented Signal', linewidth=2)
    
    ax.set_title('Original vs Augmented Signal Comparison')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    
    # Technique explanation
    explanations = {
        "Jittering": "Menambahkan noise kecil ke sinyal. Membantu model menjadi lebih robust terhadap noise dan variansi kecil dalam data.",
        "Scaling": "Mengalikan nilai sinyal dengan faktor tertentu. Membantu model beradaptasi dengan variasi amplitudo.",
        "Cropping": "Mengambil sebagian window dari sinyal. Membantu model belajar fitur yang lokal dan invariant terhadap posisi.",
        "Time Warping": "Mensimulasikan perubahan skala waktu. Membantu model beradaptasi dengan kecepatan yang berbeda dalam data temporal."
    }
    
    st.info(f"**Penjelasan Teknik:** {explanations[technique]}")
    
    st.markdown("---")
    st.subheader("Definisi Teknik Augmentation")
    
    st.write("**Jittering:** Menambahkan noise kecil ke sinyal. Membantu model menjadi lebih robust terhadap noise dan variansi kecil dalam data.")
    st.write("**Scaling:** Mengalikan nilai sinyal dengan faktor tertentu. Membantu model beradaptasi dengan variasi amplitudo.")
    st.write("**Cropping:** Mengambil sebagian window dari sinyal. Membantu model belajar fitur yang lokal dan invariant terhadap posisi.")
    st.write("**Time Warping:** Mensimulasikan perubahan skala waktu. Membantu model beradaptasi dengan kecepatan yang berbeda dalam data temporal.")
    
    st.info("""
    **Pada audio dan time-series**, augmentation membantu model menjadi lebih robust terhadap variasi temporal dan amplitudo.
    Teknik-teknik ini membuat model lebih generalizable pada data dunia nyata yang bervariasi.
    """)
    
    st.markdown("---")
    st.subheader("Konsep Penting")
    st.info("""
    **Augmentation pada sinyal time-series dan audio:**
    
    - Tujuannya sama: membuat model lebih robust dan generalizable
    - Tekniknya berbeda karena sifat data yang sequential
    - Harus mempertahankan karakteristik temporal dari data
    - Tidak boleh mengubah label atau informasi esensial
    """)