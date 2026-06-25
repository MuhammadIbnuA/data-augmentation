import streamlit as st
import matplotlib.pyplot as plt

def show_home_page():
    st.title("AugmentLab")
    st.subheader("Interactive Data Augmentation Simulator")
    st.write("Belajar Data Augmentation secara visual dan interaktif")
    
    st.markdown("---")
    
    st.write("""
    Data augmentation adalah teknik membuat variasi baru dari data latih melalui transformasi realistis tanpa mengubah label asli. Teknik ini membantu model deep learning mengurangi overfitting dan meningkatkan generalisasi pada data baru.
    """)
    
    # Display diagram
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Original Data", value="")
        st.write("Data asli yang digunakan untuk pelatihan")
    
    with col2:
        st.metric(label="Augmentation", value="")
        st.write("Transformasi yang diterapkan pada data")
    
    with col3:
        st.metric(label="More Diverse Training Data", value="")
        st.write("Variasi data yang meningkat")
    
    with col4:
        st.metric(label="Better Generalization", value="")
        st.write("Model yang lebih baik dalam memprediksi data baru")
    
    st.markdown("---")
    
    # Key benefits cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Mengurangi Overfitting**")
        st.write("Dengan menambah variasi data, model menjadi lebih general daripada menghafal data latih")
    
    with col2:
        st.success("**Menambah Variasi Data**")
        st.write("Memperkaya dataset dengan contoh-contoh baru yang realistis")
    
    with col3:
        st.warning("**Meningkatkan Generalisasi Model**")
        st.write("Model menjadi lebih baik dalam memprediksi data yang belum pernah dilihat sebelumnya")
    
    st.markdown("---")
    
    st.write("## Alur Data Augmentation")
    st.write("""
    Data augmentation membantu dalam beberapa cara:
    
    1. **Mencegah overfitting**: Dengan menambah variasi data, model tidak lagi 'menghafal' pola spesifik dari data latih
    2. **Efisiensi biaya**: Lebih murah membuat variasi data daripada mengumpulkan data baru
    3. **Robustness**: Model menjadi lebih tahan terhadap variasi kecil dalam input
    4. **Domain adaptation**: Membantu model beradaptasi dengan variasi antara domain sumber dan target
    """)
    
    st.write("Navigasi ke halaman lain untuk mencoba simulasi teknik-teknik augmentation secara langsung!")