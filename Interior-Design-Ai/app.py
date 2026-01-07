import streamlit as st
import os
import io
from PIL import Image
import google.generativeai as genai
import requests


HF_API_KEY=""#add api key here
headers={"Authorization":f"Bearer{HF_API_KEY}"}
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"


GOOGLE_API_KEY=""#add google api key here
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

image_model=genai.GenerativeModel("gemini-2.5-flash")
text_model=genai.GenerativeModel("gemini-2.0-flash")

def get_room_description(image):
    text=f"Describe the image of the room in details,how the room looks like, what is in the room and what color it looks like "
    response=image_model.generate_content([text,image],stream=True)
    response.resolve()
    return response.text


def suggest_design(image,style_pref="",budget=""):
    room_desc=get_room_description(image)
    prompt=f"""You are an expert interior designer.Based on the room description:{room_desc}
    suggest how to improve layout color,give new ideas of how to design the furniture in the room 
    and wall colors and different decoration in the room
    Style Preference:{style_pref if style_pref else "No specific style preference"}
    Budget:{budget if budget else "No specific budget"}
    provide clear and detailed design suggestion.
    
    """
    response=text_model.generate_content([prompt])
    response.resolve()
    return response.text


def generate_color_palette(image,style_pref=""):
    room_desc=get_room_description(image)
    prompt=f"""You are an expert interior designer.Based on the room description:{room_desc}
    suggest a color palette that would suit well
    include wall paint colors,curtain color,rugs colorand accent color give the result in HEX color if possible
    Style Prefernce:{style_pref if style_pref else "Any"}
 """
    response=text_model.generate_content(prompt)
    response.resolve()
    return response.text

def get_shopping_list(image,style_pref):
    room_desc=get_room_description(image)
    prompt=f"""you are an expert interior designer.Based on the room description:{room_desc}
    suggest the list of furniture and decoration iteam that would improve the room design
    
    Style Preference:{style_pref if style_pref else "Any"}
    Format the  output with clear list as
    -Item name
    -suggested style,material,color
    -category(sofa,rug,shelve,curtain,bed,lamp,wall art)
    Include only category and description"""
    response=text_model.generate_content(prompt)
    response.resolve()
    return response.text
   

def generate_image_from_design