import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO and WARNING messages

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --- Load external CSS file ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# --- Tensorflow Lite Model Prediction ---
def model_prediction(test_image):
    # Load the TFLite model and allocate tensors
    interpreter = tf.lite.Interpreter(model_path="tomato_disease_model.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Pre-process the image to match the model's input requirements
    image = Image.open(test_image)
    image = image.resize((256, 256))  # Use the same image size as in training
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch

    # Set the tensor to point to the input data to be inferred
    interpreter.set_tensor(input_details[0]['index'], input_arr)

    # Run the inference
    interpreter.invoke()

    # Get the results
    predictions = interpreter.get_tensor(output_details[0]['index'])

    return np.argmax(predictions)  # Return index of max element

# --- UI elements ---

# Sidebar
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition"])

# Home Page
if app_mode == "Home":
    st.markdown('<h1 class="stHeader">TOMATO DISEASE RECOGNITION SYSTEM</h1>', unsafe_allow_html=True)
    image_path = "home_page.jpeg"
    st.image(image_path, use_column_width=True)
    st.markdown("""
    <div class="markdown-text-container">
    Welcome to the Tomato Disease Recognition System! 🍅🔍
    <br><br>
    Our mission is to help in identifying tomato plant diseases efficiently. Upload an image of a tomato leaf, and our system will analyze it to detect any signs of diseases. Together, let's protect our crops and ensure a healthier harvest!
    <br><br>
    <b>How It Works</b>
    <ol>
        <li><b>Upload Image:</b> Go to the <b>Disease Recognition</b> page and upload an image of a tomato leaf.</li>
        <li><b>Analysis:</b> Our system will process the image using a trained model to identify potential diseases.</li>
        <li><b>Results:</b> View the diagnosis and take action.</li>
    </ol>
    <b>Get Started</b><br>
    Click on the <b>Disease Recognition</b> page in the sidebar to begin!
    </div>
    """, unsafe_allow_html=True)

# About Page
elif app_mode == "About":
    st.markdown('<h1 class="stHeader">About</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="markdown-text-container">
    <b>About Dataset</b><br>
    This model is trained on the PlantVillage dataset, focusing specifically on 10 classes of tomato leaf diseases and healthy leaves. The dataset consists of thousands of RGB images of tomato leaves.
    <br><br>
    <b>Content</b><br>
    The model can identify the following 10 conditions:
    <ul>
        <li>Tomato Bacterial spot</li>
        <li>Tomato Early blight</li>
        <li>Tomato Late blight</li>
        <li>Tomato Leaf Mold</li>
        <li>Tomato Septoria leaf spot</li>
        <li>Tomato Spider mites Two-spotted spider mite</li>
        <li>Tomato Target Spot</li>
        <li>Tomato Yellow Leaf Curl Virus</li>
        <li>Tomato mosaic virus</li>
        <li>Tomato healthy</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Prediction Page
elif app_mode == "Disease Recognition":
    st.markdown('<h1 class="stHeader">Disease Recognition</h1>', unsafe_allow_html=True)
    test_image = st.file_uploader("Choose an Image:", type=["jpg", "jpeg", "png"])

    # Check if an image has been uploaded
    if test_image is not None:
        # Display the uploaded image
        st.image(test_image, caption="Your Uploaded Image.", width=400)  # Set a fixed width

        # Add a "Predict" button
        if st.button("Get Diagnosis"):
            with st.spinner("Analyzing the image..."):
                st.snow()
                result_index = model_prediction(test_image)

                # Reading Labels from your training notebook
                class_name = [
                    'Tomato___Bacterial_spot',
                    'Tomato___Early_blight',
                    'Tomato___Late_blight',
                    'Tomato___Leaf_Mold',
                    'Tomato___Septoria_leaf_spot',
                    'Tomato___Spider_mites Two-spotted_spider_mite',
                    'Tomato___Target_Spot',
                    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                    'Tomato___Tomato_mosaic_virus',
                    'Tomato___healthy'
                ]

                # Display the result
                st.success(f"**Diagnosis:** The model predicts this is **{class_name[result_index].replace('_', ' ')}**.")