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
    st.subheader("Simulasi Audio Spectrogram")
    
    # Create a simple spectrogram-like visualization
    st.write("Simulasi augmentasi pada spektrogram audio:")
    
    # Generate a simple spectrogram
    freqs = np.linspace(0, 10, 100)
    times = np.linspace(0, 5, 200)
    spectrogram = np.zeros((len(freqs), len(times)))
    
    # Create some frequency patterns
    for i, f in enumerate(freqs):
        for j, t in enumerate(times):
            # Create some patterns
            val = np.sin(2 * np.pi * f * 0.1) * np.exp(-(t-2.5)**2/2)
            spectrogram[i, j] = val
    
    # Add some noise for realism
    spectrogram += np.random.normal(0, 0.1, spectrogram.shape)
    
    # Plot original spectrogram
    fig, ax = plt.subplots(figsize=(10, 4))
    im = ax.imshow(spectrogram, aspect='auto', origin='lower', 
                   extent=[times.min(), times.max(), freqs.min(), freqs.max()])
    ax.set_title('Original Spectrogram Simulation')
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency')
    plt.colorbar(im, ax=ax)
    st.pyplot(fig)
    
    # Show time and frequency masking
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Time Masking**")
        # Apply time masking
        masked_spectrogram = spectrogram.copy()
        time_mask_len = 30
        time_mask_start = np.random.randint(0, spectrogram.shape[1] - time_mask_len)
        masked_spectrogram[:, time_mask_start:time_mask_start+time_mask_len] = 0
        
        fig, ax = plt.subplots(figsize=(10, 4))
        im = ax.imshow(masked_spectrogram, aspect='auto', origin='lower',
                       extent=[times.min(), times.max(), freqs.min(), freqs.max()])
        ax.set_title('Spectrogram with Time Masking')
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        plt.colorbar(im, ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.write("**Frequency Masking**")
        # Apply frequency masking
        masked_spectrogram_freq = spectrogram.copy()
        freq_mask_len = 15
        freq_mask_start = np.random.randint(0, spectrogram.shape[0] - freq_mask_len)
        masked_spectrogram_freq[freq_mask_start:freq_mask_start+freq_mask_len, :] = 0
        
        fig, ax = plt.subplots(figsize=(10, 4))
        im = ax.imshow(masked_spectrogram_freq, aspect='auto', origin='lower',
                       extent=[times.min(), times.max(), freqs.min(), freqs.max()])
        ax.set_title('Spectrogram with Frequency Masking')
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        plt.colorbar(im, ax=ax)
        st.pyplot(fig)
    
    st.info("""
    **Pada audio**, augmentation sering diterapkan pada spektrogram menggunakan time masking dan frequency masking.
    Ini membantu model menjadi lebih robust terhadap gangguan temporal dan frekuensi.
    """)
    
    st.write("")
    st.write("**Time Masking:** Menyembunyikan sebagian frame waktu secara acak")
    st.write("**Frequency Masking:** Menyembunyikan sebagian frekuensi secara acak")
    
    st.markdown("---")
    st.subheader("Konsep Penting")
    st.info("""
    **Augmentation pada sinyal time-series dan audio:**
    
    - Tujuannya sama: membuat model lebih robust dan generalizable
    - Tekniknya berbeda karena sifat data yang sequential
    - Harus mempertahankan karakteristik temporal dari data
    - Tidak boleh mengubah label atau informasi esensial
    """)