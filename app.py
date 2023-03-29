import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import plotly.express as px
from streamlit_cropper import st_cropper




st.set_page_config(page_title="FoodScore", page_icon=":food:", layout="wide")

# For testing purpose. Must be change once API is ready
# model = load_model("model_weights/model_vgg16_cl.h5", compile = False)
# response = requests.get(uploaded_file, params = params).json()
# st.image(model.predict(uploaded_file))




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
                    font-size:200px !important;
                    color: 2B5DC1
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
    uploaded_file = st.file_uploader("Upload your Food!! 🍣🍚🍱",
                                    type=["png","jpg","bmp","jpeg"],
                                    label_visibility="visible")

    if uploaded_file:
       # Hide filename on UI
        st.markdown('''<style>
                    .uploadedFile {display: none} <style>''',
                    unsafe_allow_html=True)



# Image Container
with st.container():
    if uploaded_file is not None:

        #col1, col2 = st.columns([1,1])

        st.image(uploaded_file)


#with col1:
        st.markdown("---")

        # Upload an image and set some options for demo purposes
        # st.header("Cropper Demo")

        # realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
        # box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
        # aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
        # aspect_dict = {
        #     "1:1": (1, 1),
        #     "16:9": (16, 9),
        #     "4:3": (4, 3),
        #     "2:3": (2, 3),
        #     "Free": None
        # }
        # aspect_ratio = aspect_dict[aspect_choice]

        # if uploaded_file:
        #     img = Image.open(uploaded_file)
        #     fig = px.imshow(img)
        #     fig.update_layout(width=500, height=600, margin=dict(l=1, r=1, b=1, t=1))
        #     fig.update_layout(hovermode=False)
        #     fig.update_xaxes(showticklabels=False)
        #     fig.update_yaxes(showticklabels=False)
        #     st.plotly_chart(fig, use_container_width=True)

        #     if not realtime_update:
        #         st.write("Double click to save crop")

        #     # Get a cropped image from the frontend
        #     cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
        #                                 aspect_ratio=aspect_ratio)

        #     # Manipulate cropped image at will
        #     st.write("Preview")
        #     _ = cropped_img.thumbnail((300,300))
        #     st.image(cropped_img)


        # image = Image.open(uploaded_file)
        # fig = px.imshow(image)
        # fig.update_layout(width=500, height=600, margin=dict(l=1, r=1, b=1, t=1))
        # fig.update_layout(hovermode=False)
        # fig.update_xaxes(showticklabels=False)
        # fig.update_yaxes(showticklabels=False)
        # st.plotly_chart(fig, use_container_width=True)


        #with col2:

        st.markdown("---")
        url = "https://foodscore-j5kdnfjkoa-ew.a.run.app/upload_image"

        url = "http://localhost:8000/upload_image"

        #dict_food = requests.post(url,files={'img':open('test_fotos/1.jpg','rb')}).json()



        dict_food = requests.post(url,files={'img':uploaded_file.getvalue()}).json()




        st.write(f"Is it {dict_food['name']['0']}?")

        st.write(f"Or is it {dict_food['name']['1']}, {dict_food['name']['2']},{dict_food['name']['3']} or {dict_food['name']['4']}?")



            #st.write(f"Your food has been categorized as {dict_food['name']['0']}")



            #st.write('<p style="font-size:26px; color:white;">Your food has been categorized as Rice</p>',unsafe_allow_html=True)




            # st.dataframe(df)

            #res = requests.post(url, files={'img': uploaded_file})


            # Adding label to the Foto
            # image = Image.open(uploaded_file)
            # fig = px.imshow(image)
            # fig.update_layout(width=500, height=600, margin=dict(l=1, r=1, b=1, t=1))
            # fig.update_layout(hovermode=False)
            # fig.add_annotation(text="Is it Rice?", x=0.5, y=0.9, xref="paper", yref="paper", showarrow=False,
            #                     font_size=40, font_color='Green', bgcolor="white")
            # fig.update_xaxes(showticklabels=False)
            # fig.update_yaxes(showticklabels=False)
            # st.plotly_chart(fig, use_container_width=True)


# Nutrition Container
# with st.container():
#     if uploaded_file is not None:

#         col3, col4 = st.columns([1,1])


#         with col3:

#             # Testing model weights
#             # image_pred = load_img(uploaded_file, target_size=(224, 224))
#             # image_pred = img_to_array(image_pred) / 255.0
#             # image_pred_exp = np.expand_dims(image_pred, axis=0)

#             # labelPreds = model.predict(image_pred_exp)
#             # st.write(labelPreds)
#             # st.write(f'The label highest probability is: {labelPreds[0][0]:.3f}')
#             # st.write(f'The label highest probability is: {labelPreds[0][1]:.3f}')

#         # Option whole dataset below one image
#         with col4:

            # Show a Table with the nutrition facts. To be fine tuned
            # st.write('<p style="font-size:26px; color:white;">Here you can find your nutrition Data (min/max)</p>', unsafe_allow_html=True)
            # st.dataframe(nutr_df.style.pipe(make_pretty), use_container_width=True)



# Option whole dataset below both images
# st.write(nutr_df['name'][0])


st.write('<p style="font-size:26px; color:white;">Here you can find your nutrition Data (min/max)</p>', unsafe_allow_html=True)


st.dataframe(dict_food)





# Remove the Menu Button and Streamlit Icon
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
