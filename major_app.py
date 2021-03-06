import streamlit as st
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
from PIL import Image
import cv2
import os
from tensorflow.keras.models import model_from_json

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

@st.cache()

def load_model():
    # model = keras.models.load_model('major_model.hdf5')

    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    return loaded_model

st.title("MAJOR PROJECT")
upload = st.sidebar.file_uploader(label="UPLOAD IMAGE HERE")

if upload is not None:
    file_bytes = np.asarray(bytearray(upload.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    img = Image.open(upload)
    st.image(img, caption='Uploaded Image', width=400)
    model = load_model()

    if st.sidebar.button('PREDICT'):
        st.sidebar.write("Result:")
        x = cv2.resize(opencv_image, (600, 600))
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        y = model.predict(x)
        # label = decode_predictions(y)
        category = ["MS Dhoni", "Roger Federer", "Neymar", "LeBron James"]
        my_list = [y[0][0],y[0][1],y[0][2],y[0][3]]
        if max(my_list) == y[0][0]:
            st.sidebar.subheader(category[0])

        elif max(my_list) == y[0][1]:
            st.sidebar.subheader(category[1])

        elif max(my_list) == y[0][2]:
            st.sidebar.subheader(category[2])

        elif max(my_list) == y[0][3]:
            st.sidebar.subheader(category[3])


# summary of project
if st.button("ABOUT"):
    st.write("This is an image classifier with four classes that is category = [MS Dhoni, Roger Federer, Neymar, LeBron James]."
         "I am using Transfer Learning (InceptionV3) here giving my own dataset downloaded with the help of bing downloader library,"
         "and forming it into training and testing datasets."
         "You can predict within the category given above by uploading an image and clicking on predict.")

    st.subheader("I am taking 250 images of each athlete for training and testing.")
