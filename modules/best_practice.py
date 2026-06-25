import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_best_practice_page():
    st.title("Best Practice")
    st.write("Pelajari praktik terbaik augmentation")
    
    # Best Practice Section
    st.header("Praktik Terbaik Augmentation")
    
    st.markdown("""
    **✅ Augmentation hanya untuk training set**  
    **✅ Validation dan test set harus tetap merepresentasikan data asli**  
    **✅ Transformasi harus realistis sesuai domain**  
    **✅ Label harus tetap valid**  
    **✅ Lakukan eksperimen untuk mengukur dampaknya**
    """)
    
    # Data Leakage Demo
    st.header("Demo Data Leakage")
    st.write("Simulasi bagaimana augmentation pada dataset yang salah dapat menyebabkan data leakage:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Augment Training Set Only"):
            st.success("✅ Benar: augmentation hanya diterapkan pada training set.")
            st.write("Ini adalah pendekatan yang benar karena:")
            st.write("- Training set menjadi lebih bervariasi")
            st.write("- Validation dan test set tetap representatif dari data dunia nyata")
            st.write("- Tidak ada kebocoran informasi dari training ke validation/test")
    
    with col2:
        if st.button("Augment All Dataset"):
            st.error("⚠️ Warning: ini berisiko menyebabkan data leakage.")
            st.write("Ini adalah pendekatan yang berisiko karena:")
            st.write("- Validation dan test set tidak lagi representatif dari data dunia nyata")
            st.write("- Model bisa overestimate performanya")
            st.write("- Hasil evaluasi menjadi tidak realistis")
    
    # Augmentation Impact Simulator
    st.header("Simulator Dampak Augmentation")
    st.write("Lihat bagaimana augmentation mempengaruhi performa model:")
    
    # Create data for the table
    scenarios = {
        "Scenario": [
            "Without Augmentation",
            "Realistic Augmentation", 
            "Excessive Augmentation"
        ],
        "Training Accuracy": ["98%", "91%", "75%"],
        "Validation Accuracy": ["72%", "84%", "70%"],
        "Interpretation": [
            "Overfitting",
            "Better Generalization",
            "Data becomes unrealistic"
        ]
    }
    
    df = pd.DataFrame(scenarios)
    st.table(df)
    
    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(scenarios["Scenario"]))
    width = 0.35
    
    train_acc = [98, 91, 75]
    val_acc = [72, 84, 70]
    
    ax.bar([i - width/2 for i in x], train_acc, width, label='Training Accuracy', alpha=0.8)
    ax.bar([i + width/2 for i in x], val_acc, width, label='Validation Accuracy', alpha=0.8)
    
    ax.set_xlabel('Scenario')
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Impact of Different Augmentation Strategies on Model Performance')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios["Scenario"], rotation=45, ha="right")
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on bars
    for i, v in enumerate(train_acc):
        ax.text(i - width/2, v + 1, f'{v}%', ha='center', va='bottom', fontweight='bold')
    for i, v in enumerate(val_acc):
        ax.text(i + width/2, v + 1, f'{v}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.info("""
    **Analisis Grafik:**
    - Tanpa augmentation: Gap besar antara training dan validation (overfitting)
    - Augmentation realistis: Gap kecil, generalisasi lebih baik
    - Augmentation berlebihan: Performa turun karena data tidak realistis
    """)
    
    st.markdown("---")
    st.header("Ringkasan")
    st.info("""
    **Praktik Terbaik Utama:**
    
    1. Gunakan augmentation hanya pada training set
    2. Jaga agar transformasi tetap realistis
    3. Pastikan label tetap valid setelah augmentation
    4. Evaluasi dampak augmentation pada performa model
    5. Hindari augmentation berlebihan yang membuat data tidak realistis
    """)