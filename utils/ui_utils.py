"""
Utility functions for UI elements in AugmentLab
"""

import streamlit as st

def show_technique_explanation(technique_name, explanation_text):
    """Show a formatted explanation for an augmentation technique"""
    st.info(f"**Penjelasan Teknik:** {explanation_text}")

def show_risk_assessment(risk_level, risk_message):
    """Show risk assessment with appropriate styling"""
    if risk_level.lower() == "aman" or risk_level.lower() == "rendah":
        st.success(f"Label Status: {risk_level}")
        st.write(risk_message)
    elif risk_level.lower() == "hati-hati" or risk_level.lower() == "sedang":
        st.warning(f"Label Status: {risk_level}")
        st.write(risk_message)
    else:
        st.error(f"Label Status: {risk_level}")
        st.write(risk_message)

def create_comparison_section(title, original_content, augmented_content):
    """Create a standardized before/after comparison section"""
    st.subheader(title)
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Sebelum Augmentation:**")
        st.write(original_content)
    
    with col2:
        st.write("**Sesudah Augmentation:**")
        st.write(augmented_content)

def show_data_leakage_warning():
    """Display standard warning about data leakage"""
    st.warning("""
    **Peringatan Data Leakage:** 
    Augmentation seharusnya hanya diterapkan pada training set, 
    bukan pada validation atau test set. 
    Menerapkan augmentation pada validation/test set dapat menyebabkan 
    overestimasi performa model karena adanya kebocoran informasi.
    """)

def show_label_preservation_note():
    """Display note about label preservation"""
    st.info("""
    **Catatan Pelestarian Label:** 
    Pastikan bahwa augmentasi yang diterapkan tidak mengubah label sebenarnya dari data. 
    Transformasi harus realistis dan tidak menghilangkan fitur penting 
    yang digunakan untuk klasifikasi atau deteksi.
    """)

def format_accuracy_comparison(original_train, original_val, augmented_train, augmented_val):
    """Format accuracy comparison for display"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Tanpa Augmentation", 
            value=f"Train: {original_train}, Val: {original_val}"
        )
    
    with col2:
        st.metric(
            label="Dengan Augmentation", 
            value=f"Train: {augmented_train}, Val: {augmented_val}"
        )
    
    gap_before = float(original_train[:-1]) - float(original_val[:-1])
    gap_after = float(augmented_train[:-1]) - float(augmented_val[:-1])
    
    if gap_after < gap_before:
        st.success(f"Gap berkurang dari {gap_before}% menjadi {gap_after}%, menunjukkan pengurangan overfitting.")
    else:
        st.warning(f"Gap bertambah dari {gap_before}% menjadi {gap_after}%, mungkin menunjukkan overfitting.")