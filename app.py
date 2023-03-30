import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import plotly.express as px
from streamlit_cropper import st_cropper
import io


### Function for the nutrition dataframe to implement and change units
def format_food_table(table):
    new_table = {}
    for title, col in table.items():
        new_col = {}
        new_table[title] = new_col
        for row_name, value in col.items():
            new_row_name = str(int(row_name) + 1)
            if isinstance(value, float):
                if title in ["protein", "fat", "carbohydrates"]:
                    new_col[new_row_name] = str(value) + " g"
                else:
                    new_col[new_row_name] = str(round(value * 1000)) + " mg"
            else:
                new_col[new_row_name] = value
    return new_table


st.set_page_config(page_title="FoodScore", page_icon=":food:", layout="wide")

### DEFINE PAGE CONTAINERS

# Header
with st.container():
    st.markdown(
        """<style>
            @import url('https://fonts.googleapis.com/css2?family=Monoton&display=swap');

                .big-font {
                    font-size:100px !important;
                    color: 2B5DC1;
                    font-family:'Monoton';
                    text-align: center
                    }
                    </style>""",
        unsafe_allow_html=True,
    )

    st.markdown('<p class="big-font">FoodScore</p>', unsafe_allow_html=True)
    st.write(
        f'<p style="font-size:35px; color:"#959EC6";">Do you really know what you are eating?</p>',
        unsafe_allow_html=True,
    )


# Lottie Animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


with st.container():
    left_lottie, right_lottie = st.columns(2)
    with left_lottie:
        # st.header("FoodScore")

        lottie1 = load_lottieurl(
            "https://assets5.lottiefiles.com/temp/lf20_nXwOJj.json"
        )
        st_lottie(lottie1, speed=0.8, height=250)

    with right_lottie:
        lottie2 = load_lottieurl(
            "https://assets5.lottiefiles.com/packages/lf20_tll0j4bb.json"
        )
        st_lottie(lottie2, speed=0.8, height=300)

    st.write(
        f'<p style="font-size:20px; color:"#959EC6";">Upload an image of your food and we will tell you its nutrition facts!</p>',
        unsafe_allow_html=True,
    )


with st.container():
    uploading, left_lottie = st.columns(2)
    with uploading:
        uploaded_file = st.file_uploader(" ", type=["png", "jpg", "bmp", "jpeg"])
        if uploaded_file:
            st.markdown(
                """<style>
                .uploadedFile {display: none} <style>""",
                unsafe_allow_html=True,
            )
    with left_lottie:
        st.empty()

# Image Container
with st.container():
    if uploaded_file is not None:
        url = "https://fastfoodscore-j5kdnfjkoa-ew.a.run.app/upload_image"

        # url = "http://localhost:8000/upload_image"

        # dict_food = requests.post(url,files={'img':open('test_fotos/1.jpg','rb')}).json()
        # dict_food = requests.post(url,files={'img':uploaded_file.getvalue()}).json()

        img = Image.open(uploaded_file)

        col1, col2, col3 = st.columns([5, 1, 4])

        with col1:
            # Get a cropped image from the frontend
            cropped_img = st_cropper(img, aspect_ratio=None)

        with col3:
            # Manipulate cropped image at will
            st.write("Cropped Image")
            # _ = cropped_img.thumbnail((600, 600))
            col3.image(cropped_img, width=400)

        col1, col2, col3 = st.columns([2, 0.1, 5])

        with col1:
            if st.button("Show Nutritions"):
                buffer = io.BytesIO()

                cropped_img.save(buffer, format="jpeg")

                # dict_food = requests.post(url,data=buffer.getvalue()).json()

                dict_food = requests.post(url, files={"img": buffer.getvalue()}).json()

                with col3:
                    st.write(
                        f'<p style="font-size:35px; color:"#959EC6";">Is it {dict_food["name"]["0"]}?</p>',
                        unsafe_allow_html=True,
                    )

                    st.write(
                        '<p style="font-size:20px; color:"#959EC6";">Here you can find the nutrition data for our top predictions per 100g</p>',
                        unsafe_allow_html=True,
                    )
                    dict_food = format_food_table(dict_food)
                    st.dataframe(dict_food)


# Remove the Menu Button and Streamlit Icon
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
