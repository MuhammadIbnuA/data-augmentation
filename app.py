import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import sys
from io import BytesIO

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Page configuration
st.set_page_config(
    page_title="AugmentLab - Interactive Data Augmentation Simulator",
    page_icon="🔍",
    layout="wide"
)

# Navigation sidebar
st.sidebar.title("AugmentLab")
st.sidebar.subheader("Interactive Data Augmentation Simulator")

page = st.sidebar.radio(
    "Select Page:",
    [
        "Home",
        "Image Augmentation",
        "Detection & Segmentation Demo",
        "Mixup & CutMix",
        "Text Augmentation",
        "Audio / Time-Series Demo",
        "Best Practice"
    ]
)

# Import pages dynamically
if page == "Home":
    from modules.home import show_home_page
    show_home_page()
elif page == "Image Augmentation":
    from modules.image_augmentation import show_image_augmentation_page
    show_image_augmentation_page()
elif page == "Detection & Segmentation Demo":
    from modules.detection_demo import show_detection_demo_page
    show_detection_demo_page()
elif page == "Mixup & CutMix":
    from modules.mixup_cutmix import show_mixup_cutmix_page
    show_mixup_cutmix_page()
elif page == "Text Augmentation":
    from modules.text_augmentation import show_text_augmentation_page
    show_text_augmentation_page()
elif page == "Audio / Time-Series Demo":
    from modules.timeseries_demo import show_timeseries_demo_page
    show_timeseries_demo_page()
elif page == "Best Practice":
    from modules.best_practice import show_best_practice_page
    show_best_practice_page()