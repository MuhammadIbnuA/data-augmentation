# Project Specification: AugmentLab

## Interactive Data Augmentation Simulator for Deep Learning Presentation

## 1. Project Overview

Buat sebuah website sederhana bernama **AugmentLab** untuk mengiringi presentasi PPT tentang **Data Augmentation Techniques dalam konteks Deep Learning**.

Website ini bukan sistem training model deep learning penuh, tetapi **simulator edukatif interaktif** yang membantu audiens memahami konsep:

* Apa itu data augmentation.
* Bagaimana data asli diubah menjadi data baru.
* Mengapa augmentation membantu mengurangi overfitting.
* Mengapa augmentation harus tetap menjaga label.
* Bagaimana teknik image, text, Mixup, CutMix, audio/time-series, dan best practice bekerja.

Target pengguna:

* Mahasiswa yang sedang belajar deep learning.
* Dosen/presenter yang ingin mendemokan konsep augmentation secara visual.
* Audiens non-teknis yang butuh pemahaman konseptual.

---

## 2. Main Goal

Website harus mampu menunjukkan alur:

```text
Data Asli → Data Augmentation → Data Lebih Beragam → Model Lebih General
```

Fokus utama web:

1. Visualisasi before-after augmentation.
2. Interaksi sederhana menggunakan tombol, slider, dan pilihan teknik.
3. Penjelasan konsep secara ringkas.
4. Simulasi risiko augmentation yang salah.
5. Quiz singkat untuk mengecek pemahaman.

---

## 3. Recommended Tech Stack

Gunakan **Streamlit** agar cepat dibuat, mudah dipresentasikan, dan ringan dijalankan.

### Required Libraries

```txt
streamlit
pillow
opencv-python
numpy
pandas
matplotlib
```

### Optional Libraries

```txt
albumentations
scikit-image
```

Catatan:

* Jangan membuat sistem training deep learning sungguhan.
* Tidak perlu TensorFlow/PyTorch kecuali benar-benar diperlukan.
* Semua simulasi cukup berbasis image processing, text transformation, dan grafik sederhana.

---

## 4. Website Structure

Gunakan sidebar navigation dengan menu berikut:

```text
1. Home
2. Image Augmentation
3. Detection & Segmentation Demo
4. Mixup & CutMix
5. Text Augmentation
6. Audio / Time-Series Demo
7. Best Practice & Quiz
```

Jika ingin lebih sederhana, minimal buat:

```text
1. Home
2. Image Augmentation
3. Mixup & CutMix
4. Text / Time-Series
5. Best Practice & Quiz
```

---

## 5. Page Requirements

---

# Page 1 — Home

## Purpose

Menjelaskan secara singkat apa itu data augmentation dan mengapa penting dalam deep learning.

## Content

Tampilkan judul besar:

```text
AugmentLab
Interactive Data Augmentation Simulator
```

Tampilkan subjudul:

```text
Belajar Data Augmentation secara visual dan interaktif
```

Tampilkan penjelasan ringkas:

```text
Data augmentation adalah teknik membuat variasi baru dari data latih melalui transformasi realistis tanpa mengubah label asli. Teknik ini membantu model deep learning mengurangi overfitting dan meningkatkan generalisasi pada data baru.
```

## Visual Component

Buat diagram sederhana:

```text
Original Data → Augmentation → More Diverse Training Data → Better Generalization
```

Gunakan `st.columns()` untuk membuat 4 blok visual.

## Key Cards

Buat 3 kartu manfaat:

1. Mengurangi overfitting.
2. Menambah variasi data.
3. Meningkatkan generalisasi model.

---

# Page 2 — Image Augmentation

## Purpose

Menunjukkan teknik dasar image augmentation pada computer vision.

## Features

User dapat:

* Upload gambar sendiri.
* Menggunakan sample image bawaan jika tidak upload.
* Memilih teknik augmentation.
* Mengatur parameter menggunakan slider.
* Melihat gambar asli dan gambar hasil augmentation secara berdampingan.

## Required Augmentation Techniques

Minimal implementasikan:

1. Horizontal Flip
2. Rotation
3. Crop
4. Zoom
5. Brightness
6. Contrast
7. Blur
8. Noise Injection

## UI Layout

Gunakan dua kolom:

```text
[Original Image]    [Augmented Image]
```

Di bawahnya tampilkan explanation box:

```text
Apa yang berubah?
Apakah label masih valid?
Kapan teknik ini cocok digunakan?
```

## Controls

Contoh kontrol:

```text
- Selectbox: pilih teknik augmentation
- Slider rotation: -45 sampai 45 derajat
- Slider brightness: 0.5 sampai 1.5
- Slider contrast: 0.5 sampai 1.5
- Slider blur: 1 sampai 15
- Slider noise: 0 sampai 50
```

## Label Preserving Message

Setelah augmentation, tampilkan status:

```text
Label Status: Aman
Transformasi ini umumnya tidak mengubah makna utama objek.
```

Untuk transformasi berisiko, tampilkan:

```text
Label Status: Hati-hati
Transformasi terlalu ekstrem dapat mengubah makna visual atau menghilangkan objek utama.
```

---

# Page 3 — Detection & Segmentation Demo

## Purpose

Menjelaskan bahwa pada object detection dan segmentation, label spasial seperti bounding box dan mask harus ikut berubah saat gambar diubah.

## Features

Gunakan sample image bawaan dengan bounding box sederhana.

Contoh:

* Gambar objek.
* Bounding box di atas objek.
* Tombol transformasi:

  * Shift
  * Crop
  * Rotate sederhana

## Required Demo Modes

Buat dua mode:

### 1. Correct Mode

Gambar berubah dan bounding box ikut berubah.

Tampilkan pesan:

```text
Benar: bounding box ikut menyesuaikan transformasi gambar.
```

### 2. Wrong Mode

Gambar berubah tetapi bounding box tetap di posisi lama.

Tampilkan pesan:

```text
Salah: gambar berubah, tetapi bounding box tidak ikut berubah. Ini dapat merusak ground truth dan menurunkan performa model.
```

## UI Layout

```text
[Before]
Gambar asli + bounding box

[After Correct]
Gambar berubah + bounding box ikut berubah

[After Wrong]
Gambar berubah + bounding box tetap
```

## Important Concept

Tampilkan highlight box:

```text
Pada klasifikasi, label cukup berupa nama kelas.  
Pada object detection dan segmentation, posisi objek juga bagian dari label.
```

---

# Page 4 — Mixup & CutMix

## Purpose

Menunjukkan augmentation modern yang menggabungkan dua sampel dan labelnya.

## Features

Sediakan dua sample image bawaan:

* Image A
* Image B

User dapat memilih:

1. Mixup
2. CutMix

---

## Mixup Feature

Tampilkan dua gambar input.

Tambahkan slider alpha/ratio:

```text
Rasio Image A: 0% sampai 100%
Rasio Image B: otomatis 100% - rasio Image A
```

Output:

* Gambar campuran transparan.
* Label gabungan.

Contoh label:

```text
Label: 0.7 Cat + 0.3 Dog
```

Explanation:

```text
Mixup mencampur dua gambar dan dua label secara proporsional. Teknik ini membantu model belajar decision boundary yang lebih halus.
```

---

## CutMix Feature

Tampilkan:

* Image A sebagai background.
* Patch dari Image B ditempel pada Image A.
* Ukuran patch dapat diatur dengan slider.

Output label:

```text
Label: 0.75 Image A + 0.25 Image B
```

Explanation:

```text
CutMix menempel bagian gambar lain ke gambar utama. Label disesuaikan berdasarkan proporsi area patch.
```

---

# Page 5 — Text Augmentation

## Purpose

Menunjukkan bahwa augmentation pada teks lebih sensitif karena perubahan kata dapat mengubah makna.

## Features

User dapat memasukkan kalimat sendiri.

Jika input kosong, gunakan contoh:

```text
Aplikasi ini sangat membantu mahasiswa dalam memahami deep learning.
```

## Required Techniques

Minimal implementasikan:

1. Synonym Replacement sederhana berbasis dictionary lokal.
2. Random Deletion.
3. Random Swap.
4. Random Insertion sederhana.
5. Paraphrase sederhana menggunakan template manual.

Tidak perlu menggunakan API LLM eksternal.

## Example Dictionary

Gunakan dictionary sederhana:

```python
synonyms = {
    "membantu": ["menolong", "memudahkan"],
    "mahasiswa": ["pelajar", "peserta didik"],
    "memahami": ["mengerti", "mempelajari"],
    "cepat": ["singkat", "segera"],
    "baik": ["bagus", "optimal"]
}
```

## Output

Tampilkan:

```text
Original Text:
...

Augmented Text:
...

Risk Note:
Pada NLP, perubahan satu kata dapat mengubah makna, sentimen, atau konteks kalimat.
```

## Warning Box

Selalu tampilkan:

```text
Hati-hati: text augmentation tidak boleh mengubah label atau makna utama kalimat.
```

---

# Page 6 — Audio / Time-Series Demo

## Purpose

Menunjukkan bahwa augmentation juga bisa diterapkan pada data sinyal, audio, sensor, dan time-series.

Tidak perlu upload audio asli. Gunakan simulasi grafik.

## Time-Series Simulation

Generate sinyal sederhana:

```python
x = np.linspace(0, 10, 200)
y = np.sin(x)
```

Tampilkan grafik original dan augmented.

## Required Techniques

1. Jittering
   Tambahkan noise kecil ke sinyal.

2. Scaling
   Kalikan nilai sinyal dengan faktor tertentu.

3. Cropping
   Ambil sebagian window dari sinyal.

4. Time Warping sederhana
   Simulasikan perubahan skala waktu.

## UI Layout

```text
[Original Signal Chart]
[Augmented Signal Chart]
```

## Audio Spectrogram Simulation

Opsional:

* Buat gambar matriks random seperti spectrogram.
* Tambahkan:

  * Time masking
  * Frequency masking

Explanation:

```text
Pada audio, augmentation sering diterapkan pada spectrogram menggunakan time masking dan frequency masking.
```

---

# Page 7 — Best Practice & Quiz

## Purpose

Menjelaskan risiko penggunaan augmentation yang salah dan mengecek pemahaman audiens.

---

## Best Practice Section

Tampilkan checklist:

```text
✅ Augmentation hanya untuk training set
✅ Validation dan test set harus tetap merepresentasikan data asli
✅ Transformasi harus realistis sesuai domain
✅ Label harus tetap valid
✅ Lakukan eksperimen untuk mengukur dampaknya
```

## Data Leakage Demo

Buat simulasi sederhana:

Tampilkan tiga dataset split:

```text
Training Set
Validation Set
Test Set
```

Sediakan dua tombol:

1. Augment Training Set Only
2. Augment All Dataset

Jika user memilih tombol 1:

```text
Benar: augmentation hanya diterapkan pada training set.
```

Jika user memilih tombol 2:

```text
Warning: ini berisiko menyebabkan data leakage. Validation dan test set sebaiknya tidak dimodifikasi sembarangan.
```

---

## Augmentation Impact Simulator

Tampilkan tabel:

| Scenario               | Training Accuracy | Validation Accuracy | Interpretation           |
| ---------------------- | ----------------: | ------------------: | ------------------------ |
| Without Augmentation   |               98% |                 72% | Overfitting              |
| Realistic Augmentation |               91% |                 84% | Better Generalization    |
| Excessive Augmentation |               75% |                 70% | Data becomes unrealistic |

Tampilkan juga bar chart sederhana.

---

## Quiz Section

Buat 5 soal multiple choice.

### Question 1

Apakah augmentation boleh diterapkan pada test set?

Options:

* Ya, agar test set lebih banyak.
* Tidak, karena test set harus merepresentasikan data asli.
* Hanya jika modelnya CNN.
* Selalu wajib.

Correct answer:

```text
Tidak, karena test set harus merepresentasikan data asli.
```

### Question 2

Mengapa bounding box harus ikut berubah saat gambar di-crop?

Options:

* Agar warna gambar berubah.
* Karena posisi objek adalah bagian dari label.
* Agar ukuran file lebih kecil.
* Karena model tidak butuh label.

Correct answer:

```text
Karena posisi objek adalah bagian dari label.
```

### Question 3

Apa risiko utama synonym replacement pada NLP?

Options:

* Gambar menjadi blur.
* Makna atau sentimen kalimat berubah.
* Dataset menjadi terlalu kecil.
* Model tidak bisa membaca angka.

Correct answer:

```text
Makna atau sentimen kalimat berubah.
```

### Question 4

Apa perbedaan Mixup dan CutMix?

Options:

* Mixup mencampur gambar secara transparan, CutMix menempel patch gambar lain.
* Mixup hanya untuk teks, CutMix hanya untuk audio.
* Mixup menghapus label, CutMix membuat label baru tanpa gambar.
* Tidak ada perbedaan.

Correct answer:

```text
Mixup mencampur gambar secara transparan, CutMix menempel patch gambar lain.
```

### Question 5

Mengapa augmentation berlebihan berbahaya?

Options:

* Karena dapat membuat data tidak realistis.
* Karena selalu membuat model terlalu akurat.
* Karena tidak mengubah gambar.
* Karena hanya berlaku untuk test set.

Correct answer:

```text
Karena dapat membuat data tidak realistis.
```

Tampilkan skor akhir:

```text
Skor Anda: X / 5
```

Berikan feedback:

* 0–2: Perlu mengulang konsep dasar.
* 3–4: Sudah cukup memahami.
* 5: Sangat baik.

---

## 6. Suggested Folder Structure

Buat struktur project seperti ini:

```text
augmentlab/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── image_augmentation.py
│   ├── detection_demo.py
│   ├── mixup_cutmix.py
│   ├── text_augmentation.py
│   ├── timeseries_demo.py
│   └── quiz.py
│
├── assets/
│   ├── sample_cat.jpg
│   ├── sample_dog.jpg
│   ├── sample_car.jpg
│   └── sample_object.jpg
│
└── utils/
    ├── image_utils.py
    └── ui_utils.py
```

Jika tidak ada asset gambar, buat fallback dengan generated image sederhana menggunakan PIL.

---

## 7. UI Design Guidelines

Gunakan desain sederhana, bersih, dan edukatif.

### Layout Style

* Sidebar untuk navigasi.
* Main area untuk simulasi.
* Gunakan `st.columns()` untuk before-after.
* Gunakan `st.expander()` untuk penjelasan konsep.
* Gunakan `st.info()`, `st.warning()`, dan `st.success()` untuk feedback.

### Tone

Gunakan bahasa Indonesia yang ringkas dan mudah dipahami.

Contoh:

```text
Transformasi ini aman karena objek utama masih dapat dikenali dan label tidak berubah.
```

```text
Transformasi ini berisiko karena dapat mengubah makna visual atau menghilangkan objek utama.
```

---

## 8. Functional Requirements

Website harus memenuhi kebutuhan berikut:

| ID    | Requirement                                                            |
| ----- | ---------------------------------------------------------------------- |
| FR-01 | User dapat membuka halaman Home dan membaca konsep dasar augmentation. |
| FR-02 | User dapat upload gambar atau menggunakan gambar contoh.               |
| FR-03 | User dapat memilih teknik image augmentation.                          |
| FR-04 | User dapat melihat before-after image augmentation.                    |
| FR-05 | User dapat melihat simulasi bounding box benar dan salah.              |
| FR-06 | User dapat mencoba Mixup dengan dua gambar.                            |
| FR-07 | User dapat mencoba CutMix dengan dua gambar.                           |
| FR-08 | User dapat memasukkan teks dan melakukan text augmentation sederhana.  |
| FR-09 | User dapat melihat simulasi time-series augmentation.                  |
| FR-10 | User dapat membaca best practice penggunaan augmentation.              |
| FR-11 | User dapat mengerjakan quiz dan melihat skor.                          |

---

## 9. Non-Functional Requirements

| ID     | Requirement                                          |
| ------ | ---------------------------------------------------- |
| NFR-01 | Website harus berjalan lokal menggunakan Streamlit.  |
| NFR-02 | Website harus ringan dan tidak membutuhkan GPU.      |
| NFR-03 | Website tidak boleh membutuhkan API eksternal.       |
| NFR-04 | Website harus bisa dijalankan dengan satu command.   |
| NFR-05 | UI harus mudah dipakai saat presentasi.              |
| NFR-06 | Semua teks utama menggunakan bahasa Indonesia.       |
| NFR-07 | Jika gambar gagal di-load, tampilkan fallback image. |

---

## 10. Run Command

Project harus bisa dijalankan dengan:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 11. Acceptance Criteria

Project dianggap selesai jika:

1. Website dapat dijalankan tanpa error.
2. Sidebar navigation berjalan.
3. Minimal 5 halaman utama tersedia.
4. Image augmentation dapat menampilkan before-after.
5. Mixup dan CutMix dapat divisualisasikan.
6. Text augmentation dapat menghasilkan variasi kalimat.
7. Time-series augmentation dapat menampilkan grafik original dan augmented.
8. Best practice dan warning data leakage tersedia.
9. Quiz dapat menghitung skor.
10. Website cocok digunakan sebagai pendamping PPT 10 slide tentang data augmentation.

---

## 12. Important Implementation Notes

* Jangan membangun model deep learning sungguhan.
* Jangan melakukan training model karena tujuan web adalah edukasi dan simulasi.
* Fokus pada visualisasi konsep.
* Pastikan semua teknik augmentation memiliki penjelasan singkat.
* Pastikan setiap halaman dapat digunakan saat presentasi tanpa konfigurasi rumit.
* Gunakan sample data bawaan agar web tetap bisa berjalan meskipun user tidak upload file.
* Hindari UI yang terlalu ramai.
* Prioritaskan clarity daripada kompleksitas.

---

## 13. Expected Final Deliverables

Agentic coding model harus menghasilkan:

1. Source code lengkap.
2. `requirements.txt`.
3. `README.md`.
4. Struktur folder rapi.
5. Sample assets atau fallback generated assets.
6. Instruksi menjalankan aplikasi.
7. Aplikasi Streamlit yang siap digunakan untuk presentasi.

---

## 14. README Content Requirement

README harus berisi:

```text
# AugmentLab

AugmentLab adalah website interaktif sederhana untuk mensimulasikan teknik data augmentation dalam konteks deep learning.

## Features

- Image augmentation simulator
- Bounding box transformation demo
- Mixup and CutMix simulator
- Text augmentation simulator
- Audio/time-series augmentation demo
- Best practice and quiz

## Installation

pip install -r requirements.txt

## Run

streamlit run app.py

## Purpose

Website ini dibuat sebagai pendamping presentasi pembelajaran Data Augmentation Techniques dalam Deep Learning.
```

---

## 15. Presentation Mapping

Hubungkan fitur web dengan slide PPT:

| PPT Slide                          | Website Feature                      |
| ---------------------------------- | ------------------------------------ |
| Slide 1 — Why Augmentation Matters | Home                                 |
| Slide 2 — Basic Concept            | Home + Image Augmentation            |
| Slide 3 — Basic Image Augmentation | Image Augmentation                   |
| Slide 4 — Detection & Segmentation | Detection & Segmentation Demo        |
| Slide 5 — Mixup & CutMix           | Mixup & CutMix                       |
| Slide 6 — Automated Augmentation   | Home explanation / optional info box |
| Slide 7 — Text Augmentation        | Text Augmentation                    |
| Slide 8 — Audio & Time-Series      | Audio / Time-Series Demo             |
| Slide 9 — Generative Augmentation  | Optional explanation box             |
| Slide 10 — Best Practice & Risk    | Best Practice & Quiz                 |

---

# Final Instruction for Agentic Model

Build the website as a **Streamlit educational simulator**, not a production machine learning platform.

The final result should be simple, interactive, visually clear, and ready to use during a classroom presentation about **Data Augmentation Techniques in Deep Learning**.
