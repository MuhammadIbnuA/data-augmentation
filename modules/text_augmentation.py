import streamlit as st
import random
import re
import difflib

# Simple synonym dictionary
SYNONYMS = {
    "pemanfaatan": ["penggunaan", "implementasi", "aplikasi"],
    "teknologi": ["teknologi", "ilmu pengetahuan", "inovasi digital"],
    "dalam": ["pada", "di", "mengenai"],
    "pendidikan": ["edukasi", "pengajaran", "pelatihan"],
    "sangat": ["amat", "sekali", "benar-benar"],
    "membantu": ["menolong", "memudahkan", "mendukung"],
    "proses": ["mekanisme", "langkah", "tahapan"],
    "pembelajaran": ["pengajaran", "edukasi", "pelatihan"],
    "mahasiswa": ["pelajar", "peserta didik", "akademisi"],
    "cepat": ["singkat", "segera", "kilat"],
    "baik": ["bagus", "optimal", "hebat"],
    "ini": ["itu", "berikut", "tersebut"],
    "deep": ["pembelajaran", "mendalam", "profund"],
    "learning": ["pembelajaran", "pengkajian", "study"],
    "konsep": ["ide", "gagasan", "prinsip"],
    "teknik": ["metode", "cara", "pendekatan"],
    "data": ["informasi", "data", "fakta"],
    "augmentation": ["penambahan", "perluasan", "eksposisi"]
}

def synonym_replacement(text, n=1):
    """Replace n words with synonyms"""
    words = text.split()
    replaced_words = []

    for word in words:
        # Clean word for synonym lookup (remove punctuation)
        clean_word = re.sub(r'[^\w]', '', word.lower())

        if clean_word in SYNONYMS and len(SYNONYMS[clean_word]) > 0:
            # Pick a random synonym
            synonym = random.choice(SYNONYMS[clean_word])
            # Preserve capitalization
            if word[0].isupper():
                synonym = synonym.capitalize()
            replaced_words.append(synonym)
        else:
            replaced_words.append(word)

    return " ".join(replaced_words)

def random_deletion(text, p=0.1):
    """Delete words with probability p"""
    words = text.split()
    if len(words) == 1:
        return text

    new_words = []
    for word in words:
        if random.random() > p:
            new_words.append(word)

    if len(new_words) == 0:
        return words[0]

    return " ".join(new_words)

def random_swap(text, n=1):
    """Swap n pairs of words randomly"""
    words = text.split()
    if len(words) < 2:
        return text

    for _ in range(n):
        idx1, idx2 = random.sample(range(len(words)), 2)
        words[idx1], words[idx2] = words[idx2], words[idx1]

    return " ".join(words)

def random_insertion(text, n=1):
    """Insert n synonyms of random words"""
    words = text.split()

    for _ in range(n):
        if len(words) == 0:
            break

        # Pick a random word to find synonym for
        random_idx = random.randint(0, len(words)-1)
        random_word = words[random_idx]

        # Clean word for synonym lookup
        clean_word = re.sub(r'[^\w]', '', random_word.lower())

        if clean_word in SYNONYMS and len(SYNONYMS[clean_word]) > 0:
            synonym = random.choice(SYNONYMS[clean_word])
            # Preserve capitalization
            if random_word[0].isupper():
                synonym = synonym.capitalize()

            # Insert synonym after the original word
            words.insert(random_idx + 1, synonym)

    return " ".join(words)

def paraphrase_text(text):
    """Simple paraphrasing using templates"""
    templates = [
        "Pemanfaatan {teknologi} dalam {pendidikan} {sangat} {membantu} {mahasiswa} dalam {pembelajaran}.",
        "{mahasiswa} {membantu} dalam {pembelajaran} lebih {baik} dengan pemanfaatan {teknologi} dalam {pendidikan}.",
        "Penggunaan {teknologi} dalam {pendidikan} {sangat} {membantu} {mahasiswa} dalam {pembelajaran}.",
        "Teknik pemanfaatan {teknologi} dalam {pendidikan} {membantu} {mahasiswa} dalam {pembelajaran} secara {cepat}."
    ]

    # Fill template with words from the original text
    # This is a simplified version - in practice, you'd have more sophisticated logic
    filled_template = random.choice(templates)

    # Replace placeholders with actual words if available in synonyms
    for placeholder, syn_list in SYNONYMS.items():
        if f"{{{placeholder}}}" in filled_template:
            if syn_list:
                replacement = random.choice(syn_list)
                filled_template = filled_template.replace(f"{{{placeholder}}}", replacement)

    return filled_template

def show_text_augmentation_page():
    st.title("Text Augmentation")
    st.write("Simulasi teknik augmentation pada teks - hati-hati karena perubahan kata dapat mengubah makna")

    # Text input
    default_text = "Pemanfaatan teknologi dalam pendidikan sangat membantu proses pembelajaran mahasiswa."
    user_input = st.text_area(
        "Masukkan kalimat Anda",
        value=default_text,
        height=100
    )

    if not user_input.strip():
        user_input = default_text
        st.info("Menggunakan contoh teks karena input kosong.")

    st.subheader("Teks Asli")
    st.write(user_input)

    # Select augmentation technique
    st.subheader("Pilih Teknik Augmentation")
    technique = st.selectbox(
        "Teknik",
        [
            "Synonym Replacement",
            "Random Deletion",
            "Random Swap",
            "Random Insertion",
            "Paraphrase"
        ]
    )

    # Apply augmentation based on technique
    augmented_text = user_input

    if technique == "Synonym Replacement":
        n = st.slider("Jumlah kata yang diganti", 1, 5, 1)
        augmented_text = synonym_replacement(user_input, n)
    elif technique == "Random Deletion":
        p = st.slider("Probabilitas penghapusan", 0.1, 0.5, 0.1, step=0.05)
        augmented_text = random_deletion(user_input, p)
    elif technique == "Random Swap":
        n = st.slider("Jumlah pertukaran pasangan kata", 1, 3, 1)
        augmented_text = random_swap(user_input, n)
    elif technique == "Random Insertion":
        n = st.slider("Jumlah penyisipan kata", 1, 3, 1)
        augmented_text = random_insertion(user_input, n)
    elif technique == "Paraphrase":
        augmented_text = paraphrase_text(user_input)

    st.subheader("Teks Hasil Augmentation")
    st.write(augmented_text)

    # Technique explanation
    explanations = {
        "Synonym Replacement": "Mengganti kata-kata dengan sinonimnya. Risiko: dapat mengubah makna atau sentimen jika sinonim tidak tepat.",
        "Random Deletion": "Menghapus kata-kata secara acak. Risiko: dapat menghilangkan informasi penting atau membuat kalimat tidak gramatikal.",
        "Random Swap": "Menukar posisi pasangan kata secara acak. Risiko: dapat mengubah struktur sintaksis dan makna kalimat.",
        "Random Insertion": "Menyisipkan sinonim kata secara acak. Risiko: dapat membuat kalimat tidak wajar atau repetitif.",
        "Paraphrase": "Membuat versi parafra kalimat. Risiko: hasil parafra mungkin tidak selalu akurat atau gramatikal."
    }

    st.info(f"**Penjelasan Teknik:** {explanations[technique]}")

    # Warning box
    st.warning("""
    **Hati-hati:** text augmentation tidak boleh mengubah label atau makna utama kalimat.
    Pada NLP, perubahan satu kata dapat mengubah makna, sentimen, atau konteks kalimat.
    """)

    # Show comparison
    st.subheader("Perbandingan")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Teks Original:**")
        st.write(user_input)

    with col2:
        st.write("**Teks Augmented:**")
        # Highlight differences between original and augmented text using difflib
        original_words = user_input.split()
        augmented_words = augmented_text.split()
        
        # Use SequenceMatcher to find differences
        matcher = difflib.SequenceMatcher(None, original_words, augmented_words)
        highlighted_text = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                # Words are the same
                highlighted_text.extend(augmented_words[j1:j2])
            elif tag == 'replace':
                # Words have been replaced, highlight them with high contrast color
                for word in augmented_words[j1:j2]:
                    highlighted_text.append(f'<span style="background-color: #FF6B6B; color: white; padding: 2px 4px; border-radius: 3px;">{word}</span>')
            elif tag == 'delete':
                # Words were deleted from original (shouldn't happen in our case since we're showing augmented text)
                pass
            elif tag == 'insert':
                # Words were inserted, highlight them with high contrast color
                for word in augmented_words[j1:j2]:
                    highlighted_text.append(f'<span style="background-color: #4ECDC4; color: white; padding: 2px 4px; border-radius: 3px;">{word}</span>')
        
        # Join the words back together
        result_text = ' '.join(highlighted_text)
        st.markdown(result_text, unsafe_allow_html=True)