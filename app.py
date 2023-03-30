import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import plotly.express as px
from streamlit_cropper import st_cropper
import io

# Title
st.set_page_config(page_title="FoodScore", page_icon=":food:", layout="wide")

subset = ["protein", "calcium", "fat", "carbohydrates", "vitamins"]

# Funciton for styling the Nutrition Dataset
def make_pretty(styler):

                styler.highlight_max(axis=0, color="#EA5432", subset=subset)
                styler.highlight_min(axis=0, color="#72C01F", subset=subset)
                styler.format(formatter="{:.2f}", subset=subset)


                return styler


### DEFINE PAGE CONTAINERS

# Header
with st.container():
    st.markdown("""<style>
                .big-font {
                    font-size:80px !important;
                    color: 2B5DC1
                    }
                    </style>""",
                    unsafe_allow_html=True)

    st.markdown('<p class="big-font">FoodScore</p>', unsafe_allow_html=True)



# Lottie Animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Containers
with st.container():
    text, right_lottie, empty = st.columns(3)
    with text:
        st.header('Welcome to FoodScore!! 🍕')
        st.subheader('Do you really know what you are eating?')
    with right_lottie:
        lottie1 = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_tll0j4bb.json')
        st_lottie(lottie1, speed = 0.5, height=250)
    with empty:
        st.empty()

with st.container():
    text, empty = st.columns(2)
    with text:
        st.subheader('Upload an image of your food and we will tell you its nutrition facts!!')
    with empty:
        st.empty()

with st.container():
    uploading, left_lottie = st.columns(2)
    with uploading:
        uploaded_file = st.file_uploader("Upload your Food!! 🍣🍚🍱",
                                    type=["png","jpg","bmp","jpeg"])
        if uploaded_file:
                st.markdown('''<style>
                .uploadedFile {display: none} <style>''',
                unsafe_allow_html=True)
    with left_lottie:
        lottie2 = load_lottieurl('https://assets5.lottiefiles.com/temp/lf20_nXwOJj.json')
        st_lottie(lottie2, speed = 0.5, height=150)

# Image Container
with st.container():
    if uploaded_file is not None:
        url = "https://fastfoodscore-j5kdnfjkoa-ew.a.run.app/upload_image"
        # url = "http://localhost:8000/upload_image"

        image, aspect = st.columns(2)
        with aspect:
            realtime_update = st.checkbox(label="Update in Real Time", value=True)
            aspect_choice = st.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
            aspect_dict = {
                "1:1": (1, 1),
                 "16:9": (16, 9),
                "4:3": (4, 3),
                "2:3": (2, 3),
                "Free": None
            }
            aspect_ratio = aspect_dict[aspect_choice]

            with image:
                if uploaded_file:
                    img = Image.open(uploaded_file)

                    if not realtime_update:
                        st.write("Double click to save crop")

                    # Get a cropped image from the frontend
                    cropped_img = st_cropper(img, box_color='white', realtime_update=realtime_update,
                                            aspect_ratio=aspect_ratio)

        if st.button('Crop your image'):
            buffer = io.BytesIO()
            cropped_img.save(buffer, format="jpeg")

            dict_food = requests.post(url,files={'img':buffer.getvalue()}).json()

            with st.container():
                empty, text, empty = st.columns(3)
                with empty:
                    st.empty()
                with text:
                    st.write(f"Is it {dict_food['name']['0']}?")
                    st.write(f"Or is it {dict_food['name']['1']}?")
                with empty:
                    st.empty()

            with st.container():
                st.write('<p style="font-size:26px; color:2B5DC1;">And is it healthy?</p>', unsafe_allow_html=True)
                st.dataframe(dict_food, use_container_width=True)


# Remove the Menu Button and Streamlit Icon
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
