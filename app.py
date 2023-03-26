import streamlit as st
import requests
import pandas as pd
import h5py
from keras.models import load_model
import cv2
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie

from PIL import Image
# from io import BytesIO
import plotly.express as px
from keras.utils import load_img, img_to_array
import numpy as np

st.set_page_config(page_title="FoodScore", page_icon=":food:", layout="wide")

# For testing purpose. Must be change once API is ready
model = load_model("model_weights/model_vgg16_cl.h5", compile = False)
#response = requests.get(uploaded_file, params = params).json()
# st.image(model.predict(uploaded_file))


### DEFINE PAGE CONTAINERS

# Header
with st.container():

    st.markdown("""<style>
                .big-font {
                    font-size:200px !important;
                    color: red
                    }
                    </style>""",
                    unsafe_allow_html=True)

    st.markdown('<p class="big-font">FoodScore !!</p>', unsafe_allow_html=True)



# Lottie Animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

with st.container():
    left_lottie, right_lottie = st.columns(2)
    with left_lottie:
        st.header('Welcome to FoodScore!! 🍕')
        st.subheader('Do you really know what you are eating?')

        lottie1 = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_tll0j4bb.json')
        st_lottie(lottie1, speed = 0.8, height=250)


    with right_lottie:
        lottie2 = load_lottieurl('https://assets5.lottiefiles.com/temp/lf20_nXwOJj.json')
        st_lottie(lottie2, speed = 0.8, height=400)


# Subheader
with st.container():
    st.subheader('Upload an image of your food and we will tell you its nutrition facts!!')


# Photo Upload
with st.container():
    uploaded_file = st.file_uploader("Upload Image :rocket:",
                                    type=["png","jpg","bmp","jpeg"],
                                    label_visibility="collapsed")



# Image Container
with st.container():
    if uploaded_file is not None:

        col1, col2 = st.columns([1,1])

        image = Image.open(uploaded_file)

        with col1:
            st.markdown("---")
            image = Image.open(uploaded_file)
            fig = px.imshow(image)
            fig.update_layout(width=500, height=600, margin=dict(l=1, r=1, b=1, t=1))
            fig.update_layout(hovermode=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            st.plotly_chart(fig, use_container_width=True)


        with col2:

            st.markdown("---")

            # Adding label to the Foto
            image = Image.open(uploaded_file)
            fig = px.imshow(image)
            fig.update_layout(width=500, height=600, margin=dict(l=1, r=1, b=1, t=1))
            fig.update_layout(hovermode=False)
            fig.add_annotation(text="Is it Rice?", x=0.5, y=0.9, xref="paper", yref="paper", showarrow=False,
                                font_size=40, font_color='Green', bgcolor="red")
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            st.plotly_chart(fig, use_container_width=True)


# Nutrition Container
with st.container():
    if uploaded_file is not None:

        col3, col4 = st.columns([1,1])


        with col3:
            st.write(st.write('<p style="font-size:26px; color:red;">Your label has been selected as Rice</p>',unsafe_allow_html=True))

            # Testing model weights
            image_pred = load_img("test_fotos/1.jpg", target_size=(224, 224))
            image_pred = img_to_array(image_pred) / 255.0
            image_pred_exp = np.expand_dims(image_pred, axis=0)

            labelPreds = model.predict(image_pred_exp)
            st.write('The label is', labelPreds)

        with col4:

            # Show a Table with the nutrition facts. To be fine tuned
            nutr_data = np.random.default_rng().uniform(0, 100, size=(5,4))
            df = pd.DataFrame(nutr_data, columns=list('ABCD'))
            st.write(st.write('<p style="font-size:26px; color:red;">Here you can find your nutrition Data</p>',unsafe_allow_html=True))
            st.write(df)


# Remove the Menu Button and Streamlit Icon
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
