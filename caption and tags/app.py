import os
import io
import streamlit as st
from PIL import Image
import google.generativeai as genai
GOOGLE_API_KEY="add your api key here"#add your personal api key here
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
print("api key configured")
image_model=genai.GenerativeModel("gemini-2.5-flash")
def caption(platform,max_length,image):
  min_length=20
  if platform is None:
    text=f"Generate caption for this image {image} with max length of {max_length} and min length of {min_length}"
  else:
    text=f"Generate me a caption for this image {image} for this {platform} which i can uplaod on the platform with max length of{max_length} and min length of {min_length}"
  response=image_model.generate_content([text,image])
  return response.text

def tags(platform,max_tags,image):
  min_tag=3
  if platform is None:
    tags=f"Generate tags for this image {image} with minimum tags {min_tag} and maximum tags{max_tags}"
  else:
    tags=f"Generate tags for this image {image} on this {platform} which i can upload on the {platform} with minimum tags {min_tag} and maximum tags{max_tags} "
  response=image_model.generate_content([tags,image])
  return response.text

st.title("Image Caption And Tag Generator")
st.write("This app generate captions and tags for an image")
upload=st.file_uploader("Choose an image",type=["png","jpeg","jpg"])
max_length=st.slider("Select the length of the caption",50,70,100)
max_tags=st.slider("Select the maximum number of tags",5,7,9,12)

platform=""

if st.button("Identify your image"):
  if upload is not None:
    image=Image.open(upload)
    st.image(image,caption="Uploaded image successfully",use_container_width=True)
    st.write("")
    st.write("Generating captions and tags")
    caption=caption(platform,max_length,image)
    tag=tags(platform,max_tags,image)
    st.write(f"Caption: {caption}\n\n Tags:{tag}")
  else:
    st.write("upload an image first")
if st.button("Instagram Caption and Tags"):
  if upload is not None:
    image=Image.open(upload)
    st.image(image,caption="Uploaded image successfully",use_column_width=True)
    st.write("")
    st.write("Generating captions and tags for instagram")
    caption=caption("Instagram",max_length,image)
    tag=tags("Instagram",max_tags,image)
    st.write(f"Caption: {caption}\n\n Tags:{tag}")
  else:
    st.write("upload an image first")

if st.button("Twitter Caption and Tags"):
  if upload is not None:
    image=Image.open(upload)
    st.image(image,caption="Uploaded image successfully",use_column_width=True)
    st.write("")
    st.write("Generating captions and tags for Twitter")
    caption=caption("Instagram",max_length,image)
    tag=tags("Instagram",max_tags,image)
    st.write(f"Caption: {caption}\n\n Tags:{tag}")
  else:
    st.write("upload an image first")
  

