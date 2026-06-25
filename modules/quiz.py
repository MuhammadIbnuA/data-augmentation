import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_quiz_page():
    st.title("Best Practice & Quiz")
    st.write("Pelajari praktik terbaik augmentation dan uji pemahaman Anda")
    
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
    
    # Quiz Section
    st.header("Kuis Pemahaman")
    st.write("Uji pemahaman Anda tentang data augmentation:")
    
    # Questions
    questions = [
        {
            "question": "Apakah augmentation boleh diterapkan pada test set?",
            "options": [
                "Ya, agar test set lebih banyak",
                "Tidak, karena test set harus merepresentasikan data asli", 
                "Hanya jika modelnya CNN",
                "Selalu wajib"
            ],
            "correct": 1,
            "explanation": "Test set harus merepresentasikan data dunia nyata yang akan dihadapi model. Jika di-augmentasi, hasil evaluasi tidak realistis."
        },
        {
            "question": "Mengapa bounding box harus ikut berubah saat gambar di-crop?",
            "options": [
                "Agar warna gambar berubah",
                "Karena posisi objek adalah bagian dari label",
                "Agar ukuran file lebih kecil", 
                "Karena model tidak butuh label"
            ],
            "correct": 1,
            "explanation": "Pada object detection, posisi objek (bounding box) adalah bagian dari label. Jika gambar diubah, label juga harus disesuaikan."
        },
        {
            "question": "Apa risiko utama synonym replacement pada NLP?",
            "options": [
                "Gambar menjadi blur",
                "Makna atau sentimen kalimat berubah",
                "Dataset menjadi terlalu kecil",
                "Model tidak bisa membaca angka"
            ],
            "correct": 1,
            "explanation": "Pada NLP, perubahan satu kata dapat mengubah makna atau sentimen kalimat, sehingga label bisa menjadi tidak akurat."
        },
        {
            "question": "Apa perbedaan Mixup dan CutMix?",
            "options": [
                "Mixup mencampur gambar secara transparan, CutMix menempel patch gambar lain",
                "Mixup hanya untuk teks, CutMix hanya untuk audio",
                "Mixup menghapus label, CutMix membuat label baru tanpa gambar",
                "Tidak ada perbedaan"
            ],
            "correct": 0,
            "explanation": "Mixup menggabungkan dua gambar dengan interpolasi, sedangkan CutMix menempelkan bagian dari satu gambar ke gambar lain."
        },
        {
            "question": "Mengapa augmentation berlebihan berbahaya?",
            "options": [
                "Karena dapat membuat data tidak realistis",
                "Karena selalu membuat model terlalu akurat",
                "Karena tidak mengubah gambar",
                "Karena hanya berlaku untuk test set"
            ],
            "correct": 0,
            "explanation": "Augmentation berlebihan dapat membuat data menjadi tidak representatif dari distribusi aslinya, menyebabkan model kesulitan generalisasi."
        }
    ]
    
    # Store answers
    user_answers = []
    
    for i, q in enumerate(questions):
        st.subheader(f"Pertanyaan {i+1}")
        st.write(q["question"])
        
        answer = st.radio(
            f"Jawaban untuk pertanyaan {i+1}:",
            q["options"],
            key=f"q{i}"
        )
        
        # Store the selected option index
        selected_index = q["options"].index(answer)
        user_answers.append(selected_index)
    
    # Calculate score when submit button is clicked
    if st.button("Kirim Jawaban"):
        score = 0
        for i, (user_ans, q) in enumerate(zip(user_answers, questions)):
            if user_ans == q["correct"]:
                score += 1
                st.success(f"Pertanyaan {i+1}: ✅ Benar!")
            else:
                st.error(f"Pertanyaan {i+1}: ❌ Salah!")
            
            st.info(f"Penjelasan: {q['explanation']}")
            st.write("---")
        
        # Display final score
        st.header("Nilai Anda")
        st.write(f"**Skor: {score} / {len(questions)}**")
        
        percentage = (score / len(questions)) * 100
        
        if percentage >= 80:
            st.balloons()
            st.success("🎉 Sangat baik! Anda memahami konsep augmentation dengan baik.")
        elif percentage >= 60:
            st.success("👍 Sudah cukup memahami konsep augmentation.")
        else:
            st.warning("📚 Perlu mengulang konsep dasar augmentation.")
        
        # Show score breakdown
        st.progress(score / len(questions))
        st.write(f"Anda menjawab {score} dari {len(questions)} pertanyaan dengan benar.")

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