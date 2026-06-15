import streamlit as st
import os
import io
import re
import requests
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

headers = {"Authorization": f"Bearer {HF_API_KEY}"}
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

genai.configure(api_key=GOOGLE_API_KEY)

image_model = genai.GenerativeModel("gemini-2.5-flash")
text_model  = genai.GenerativeModel("gemini-2.0-flash")




def get_room_description(image):
    """Describe the uploaded room image using Gemini Vision."""
    text = (
        "Describe the image of the room in detail: how the room looks, "
        "what furniture and objects are in it, what colors are present, "
        "and what the overall style feels like."
    )
    response = image_model.generate_content([text, image], stream=True)
    response.resolve()
    return response.text


def suggest_design(image, style_pref="", budget=""):
    """Generate interior design suggestions based on the room image."""
    room_desc = get_room_description(image)
    prompt = f"""You are an expert interior designer.
Based on this room description:
{room_desc}

Suggest how to improve the layout, wall colors, furniture arrangement, and decoration.
Be specific about changes and explain why each suggestion would improve the space.

Style Preference: {style_pref if style_pref else "No specific style preference"}
Budget: {budget if budget else "No specific budget"}

Structure your response with clear sections:
1. Layout Improvements
2. Color & Paint Recommendations
3. Furniture Arrangement
4. Decor & Accessories
5. Lighting Suggestions
"""
    response = text_model.generate_content([prompt])
    response.resolve()
    return response.text


def generate_color_palette(image, style_pref=""):
    """Suggest a color palette with HEX codes for the room."""
    room_desc = get_room_description(image)
    prompt = f"""You are an expert interior designer.
Based on this room description:
{room_desc}

Suggest a cohesive color palette that suits the space.
For EACH color, provide:
- Role (e.g., Wall Paint, Accent, Rug, Curtains)
- Color name
- HEX code (e.g., #F5E6D3)
- Brief reason why it works

Style Preference: {style_pref if style_pref else "Any"}

Format each entry clearly so HEX codes are easy to spot.
"""
    response = text_model.generate_content(prompt)
    response.resolve()
    return response.text


def get_shopping_list(image, style_pref=""):
    """Generate a shopping list of furniture and decor items."""
    room_desc = get_room_description(image)
    prompt = f"""You are an expert interior designer.
Based on this room description:
{room_desc}

Suggest furniture and decor items that would improve the room.

Style Preference: {style_pref if style_pref else "Any"}

For each item provide:
- Item name
- Suggested style, material, and color
- Category (sofa / rug / shelving / curtains / bed / lamp / wall art / table / chair / other)

List 8–12 items. Be specific and practical.
"""
    response = text_model.generate_content(prompt)
    response.resolve()
    return response.text


def generate_image_from_design(design_description, style_pref=""):
    """Generate a redesigned room image using Stable Diffusion XL."""
    style_tag = f", {style_pref} style" if style_pref else ""
    sd_prompt = (
        f"Interior design render of a beautifully redesigned room{style_tag}. "
        f"{design_description[:300]}. "
        "Photorealistic, professional interior photography, soft natural lighting, "
        "high resolution, 4K, architectural digest quality."
    )
    negative_prompt = (
        "blurry, low quality, distorted, dark, messy, ugly, unrealistic, "
        "cartoon, sketch, overexposed"
    )
    payload = {
        "inputs": sd_prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "width": 1024,
            "height": 768,
        },
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)

    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    elif response.status_code == 503:
        raise RuntimeError(
            "The image generation model is loading. Please wait 20–30 seconds and try again."
        )
    else:
        raise RuntimeError(
            f"Image generation failed (HTTP {response.status_code}): {response.text}"
        )



def extract_hex_colors(text):
    """Pull all #RRGGBB / #RGB hex codes from a string."""
    return re.findall(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", text)




def main():
    st.set_page_config(
        page_title="AI Interior Designer",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .stApp { background-color: #F9F6F2; }

        [data-testid="stSidebar"] { background: #1C1917; }
        [data-testid="stSidebar"] * { color: #E7E5E4 !important; }
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stTextInput label,
        [data-testid="stSidebar"] .stFileUploader label { color: #A8A29E !important; }

        .app-header {
            background: linear-gradient(135deg, #292524 0%, #44403C 100%);
            color: #FAFAF9;
            padding: 2rem 2.5rem 1.8rem;
            border-radius: 16px;
            margin-bottom: 1.8rem;
        }
        .app-header h1 { margin: 0; font-size: 2rem; letter-spacing: -0.5px; }
        .app-header p  { margin: 0.4rem 0 0; color: #A8A29E; font-size: 1rem; }

        .stTabs [data-baseweb="tab-list"] {
            background: #EFEBE6; border-radius: 10px; padding: 4px; gap: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px; color: #57534E; font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background: #292524 !important; color: #FAFAF9 !important;
        }

        .result-card {
            background: #FFFFFF; border: 1px solid #E7E5E4;
            border-radius: 12px; padding: 1.5rem; margin-top: 1rem;
        }

        .swatch-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 0.8rem; }
        .swatch {
            width: 48px; height: 48px; border-radius: 8px;
            border: 2px solid rgba(0,0,0,0.08); flex-shrink: 0;
        }

        .stButton > button {
            background: #292524; color: #FAFAF9; border: none;
            border-radius: 8px; font-weight: 600;
            padding: 0.55rem 1.4rem; transition: background 0.2s;
        }
        .stButton > button:hover { background: #44403C; color: #FAFAF9; }
        .stSpinner > div { border-top-color: #292524 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

 
    if not GOOGLE_API_KEY:
        st.error(
            "⚠️ **GOOGLE_API_KEY** not found. "
            "Create a `.env` file in the project folder and add your key. "
            "See the README for instructions."
        )
        st.stop()

    
    st.markdown(
        """
        <div class="app-header">
            <h1>🏠 AI Interior Designer</h1>
            <p>Upload a photo of your room and get professional redesign suggestions,
               color palettes, shopping lists, and AI-generated visualizations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("## ⚙️ Preferences")
        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Upload your room photo",
            type=["jpg", "jpeg", "png", "webp"],
            help="Supports JPG, PNG, WEBP up to 200 MB",
        )

        style_pref = st.selectbox(
            "Design style",
            [
                "",
                "Modern Minimalist",
                "Scandinavian",
                "Bohemian",
                "Industrial",
                "Mid-Century Modern",
                "Japandi",
                "Traditional / Classic",
                "Coastal / Beach",
                "Art Deco",
                "Rustic / Farmhouse",
            ],
            format_func=lambda x: "No preference" if x == "" else x,
        )

        budget = st.selectbox(
            "Budget range",
            ["", "Under $500", "$500–$2,000", "$2,000–$5,000", "$5,000–$15,000", "$15,000+"],
            format_func=lambda x: "No preference" if x == "" else x,
        )

        st.markdown("---")

        # Show which keys are loaded
        st.markdown("**🔑 API Status**")
        st.markdown(
            f"{'✅' if GOOGLE_API_KEY else '❌'} Google Gemini  \n"
            f"{'✅' if HF_API_KEY else '⚠️'} Hugging Face *(needed for visualise tab)*"
        )

        st.markdown("---")
        st.markdown(
            "<small style='color:#78716C'>Powered by Gemini + Stable Diffusion XL</small>",
            unsafe_allow_html=True,
        )

 
    if uploaded_file is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("👈 Upload a room photo in the sidebar to get started.")
            st.markdown(
                """
                **What you'll get:**
                - 📐 Layout & design suggestions
                - 🎨 Color palette with HEX codes
                - 🛋️ Personalised shopping list
                - 🖼️ AI-generated room visualisation
                """
            )
        return

    image = Image.open(uploaded_file)

    col_img, col_meta = st.columns([2, 1])
    with col_img:
        st.image(image, caption="Your room", use_container_width=True)
    with col_meta:
        st.markdown("### Room photo uploaded ✅")
        w, h = image.size
        st.markdown(f"**Resolution:** {w} × {h} px")
        if style_pref:
            st.markdown(f"**Style:** {style_pref}")
        if budget:
            st.markdown(f"**Budget:** {budget}")
        st.markdown("Select a tab below and click **Generate** to begin.")

    st.markdown("---")

    
    tab_design, tab_palette, tab_shopping, tab_visualize = st.tabs(
        ["📐 Design Suggestions", "🎨 Color Palette", "🛋️ Shopping List", "🖼️ Visualize"]
    )

  
    with tab_design:
        st.markdown("### Get expert redesign advice")
        st.markdown(
            "Gemini analyses your room and returns layout, colour, furniture, "
            "and lighting recommendations tailored to your style and budget."
        )
        if st.button("Generate Design Suggestions", key="btn_design"):
            with st.spinner("Analysing your room and crafting suggestions…"):
                try:
                    result = suggest_design(image, style_pref, budget)
                    st.session_state["design_result"] = result
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        if "design_result" in st.session_state:
            st.markdown(
                f'<div class="result-card">{st.session_state["design_result"]}</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇️ Download suggestions",
                data=st.session_state["design_result"],
                file_name="design_suggestions.txt",
                mime="text/plain",
            )

    
    with tab_palette:
        st.markdown("### Discover your room's ideal palette")
        st.markdown(
            "Get wall paint, accent, rug, and curtain colour recommendations "
            "with HEX codes you can take straight to the paint store."
        )
        if st.button("Generate Color Palette", key="btn_palette"):
            with st.spinner("Crafting your colour story…"):
                try:
                    result = generate_color_palette(image, style_pref)
                    st.session_state["palette_result"] = result
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        if "palette_result" in st.session_state:
            palette_text = st.session_state["palette_result"]
            hex_colors = extract_hex_colors(palette_text)
            if hex_colors:
                swatch_html = '<div class="swatch-row">'
                for c in hex_colors:
                    swatch_html += f'<div class="swatch" style="background:{c}" title="{c}"></div>'
                swatch_html += "</div>"
                st.markdown(swatch_html, unsafe_allow_html=True)

            st.markdown(
                f'<div class="result-card">{palette_text}</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇️ Download palette",
                data=palette_text,
                file_name="color_palette.txt",
                mime="text/plain",
            )

   
    with tab_shopping:
        st.markdown("### Build your shopping list")
        st.markdown(
            "Get a curated list of furniture and décor pieces — with style, "
            "material, and colour notes — matched to your preferences."
        )
        if st.button("Generate Shopping List", key="btn_shopping"):
            with st.spinner("Curating your perfect pieces…"):
                try:
                    result = get_shopping_list(image, style_pref)
                    st.session_state["shopping_result"] = result
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        if "shopping_result" in st.session_state:
            st.markdown(
                f'<div class="result-card">{st.session_state["shopping_result"]}</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇️ Download shopping list",
                data=st.session_state["shopping_result"],
                file_name="shopping_list.txt",
                mime="text/plain",
            )

    
    with tab_visualize:
        st.markdown("### See your redesigned room")
        st.markdown(
            "Describe how you want the room to look and Stable Diffusion XL "
            "will generate a photorealistic visualisation."
        )

        default_desc = ""
        if "design_result" in st.session_state:
            default_desc = st.session_state["design_result"][:250]

        custom_desc = st.text_area(
            "Describe the redesigned room (or use auto-generated suggestions above)",
            value=default_desc,
            height=130,
            placeholder=(
                "e.g. Bright Scandinavian living room with white walls, "
                "oak flooring, linen sofa, lots of plants, warm pendant lighting…"
            ),
        )

        if st.button("Generate Room Visualisation", key="btn_visualize"):
            if not custom_desc.strip():
                st.warning("Please describe the room you'd like to visualise, or generate design suggestions first.")
            elif not HF_API_KEY:
                st.error(
                    "⚠️ **HF_API_KEY** not found in your `.env` file. "
                    "Add it to enable room visualisation."
                )
            else:
                with st.spinner("Rendering your redesigned room — this takes ~30 seconds…"):
                    try:
                        generated_img = generate_image_from_design(custom_desc, style_pref)
                        st.session_state["generated_img"] = generated_img
                    except RuntimeError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Image generation failed: {e}")

        if "generated_img" in st.session_state:
            st.image(
                st.session_state["generated_img"],
                caption="AI-generated room concept",
                use_container_width=True,
            )

            buf = io.BytesIO()
            st.session_state["generated_img"].save(buf, format="PNG")
            st.download_button(
                "⬇️ Download image",
                data=buf.getvalue(),
                file_name="redesigned_room.png",
                mime="image/png",
            )

            col_orig, col_gen = st.columns(2)
            with col_orig:
                st.markdown("**Original**")
                st.image(image, use_container_width=True)
            with col_gen:
                st.markdown("**AI Redesign**")
                st.image(st.session_state["generated_img"], use_container_width=True)


if __name__ == "__main__":
    main()