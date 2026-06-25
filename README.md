# AugmentLab

AugmentLab adalah website interaktif sederhana untuk mensimulasikan teknik data augmentation dalam konteks deep learning.

## Features

- Image augmentation simulator (with user image upload support)
- Bounding box transformation demo (with user image upload support)
- Mixup and CutMix simulator (with user image upload support)
- Text augmentation simulator
- Audio/time-series augmentation demo
- Best practice guide

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Purpose

Website ini dibuat sebagai pendamping presentasi pembelajaran Data Augmentation Techniques dalam Deep Learning.

## Project Structure

```
augmentlab/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── home.py
│   ├── image_augmentation.py
│   ├── detection_demo.py
│   ├── mixup_cutmix.py
│   ├── text_augmentation.py
│   ├── timeseries_demo.py
│   └── best_practice.py
│
└── assets/
    └── (sample images would go here)
```

## Pages

1. **Home**: Penjelasan konsep dasar augmentation
2. **Image Augmentation**: Simulator teknik dasar augmentation gambar
3. **Detection & Segmentation Demo**: Demonstrasi bagaimana bounding box harus berubah saat transformasi
4. **Mixup & CutMix**: Simulator teknik augmentation modern
5. **Text Augmentation**: Simulator augmentation teks sederhana
6. **Audio / Time-Series Demo**: Simulator augmentation sinyal
7. **Best Practice**: Panduan praktik terbaik augmentation

## Tech Stack

- Streamlit: Framework untuk antarmuka web
- Pillow: Manipulasi gambar
- OpenCV: Operasi komputer visi
- NumPy: Operasi numerik
- Matplotlib: Visualisasi grafik
- Pandas: Pengolahan data tabular (untuk simulasi)