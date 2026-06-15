# 🏠 AI Interior Designer

An AI-powered interior design assistant built with **Streamlit**, **Google Gemini**, and **Stable Diffusion XL**. Upload a photo of any room and instantly get professional redesign suggestions, colour palettes with HEX codes, a curated shopping list, and a photorealistic AI-generated visualisation of the redesigned space.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📐 **Design Suggestions** | Layout, furniture, wall colour, and lighting recommendations |
| 🎨 **Color Palette** | Cohesive palette with HEX codes and visual swatches |
| 🛋️ **Shopping List** | Curated furniture & décor items with style and material notes |
| 🖼️ **Room Visualisation** | AI-generated photorealistic render of the redesigned room |
| ⬇️ **Download Outputs** | Export suggestions as `.txt` and generated images as `.png` |

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Web UI framework
- **[Google Gemini 2.5 Flash](https://ai.google.dev/)** — Vision model for room analysis
- **[Google Gemini 2.0 Flash](https://ai.google.dev/)** — Text model for design suggestions
- **[Stable Diffusion XL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)** — Image generation via Hugging Face Inference API
- **[Pillow](https://python-pillow.org/)** — Image processing

---

## 📋 Prerequisites

- Python 3.9 or higher
- A **Google AI Studio** API key → [Get one here](https://aistudio.google.com/app/apikey)
- A **Hugging Face** API key → [Get one here](https://huggingface.co/settings/tokens)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-interior-designer.git
cd ai-interior-designer
```

### 2. Install dependencies

```bash
pip install streamlit google-generativeai pillow requests
```



### 4. Run the app

```bash
streamlit run interior_design_app.py
```

The app will open at `http://localhost:8501` in your browser.

---

```

Create a `.env` file in the project root:
```
HF_API_KEY=hf_your_key
GOOGLE_API_KEY=your_key
```



---

## 🖥️ How to Use

1. **Upload** a photo of your room using the sidebar uploader (JPG, PNG, or WEBP).
2. **Select** an optional design style (e.g. Scandinavian, Bohemian, Industrial) and budget range.
3. Navigate the **four tabs**:

   - **📐 Design Suggestions** — Click *Generate Design Suggestions* to receive a structured redesign plan covering layout, colour, furniture, and lighting.
   - **🎨 Color Palette** — Click *Generate Color Palette* to see a curated palette with HEX codes and live colour swatches.
   - **🛋️ Shopping List** — Click *Generate Shopping List* for a list of recommended furniture and décor items with style notes.
   - **🖼️ Visualize** — Describe your ideal room (or use auto-filled suggestions), then click *Generate Room Visualisation* to produce an AI-rendered image. A before/after comparison is shown on completion.

4. **Download** any output using the download buttons that appear after generation.

---

## 📁 Project Structure

```
ai-interior-designer/
├── interior_design_app.py   # Main application file
├── requirements.txt         # Python dependencies
├── .env                     # API keys (do not commit)
├── .gitignore
└── README.md
```

---

## 📦 requirements.txt

```
streamlit>=1.35.0
google-generativeai>=0.7.0
Pillow>=10.0.0
requests>=2.31.0
```

---

## ⚙️ Configuration

| Variable | Description | Default |
|---|---|---|
| `HF_API_KEY` | Hugging Face API key for image generation | `""` |
| `GOOGLE_API_KEY` | Google AI Studio key for Gemini models | `""` |
| `API_URL` | Hugging Face model endpoint | SDXL base 1.0 |

The image generation model (`stabilityai/stable-diffusion-xl-base-1.0`) runs on Hugging Face's free Inference API. Cold-start times can reach 30–60 seconds — if you get a 503 error, wait a moment and try again.

---

## 🧠 How It Works

```
User uploads room photo
        │
        ▼
Gemini 2.5 Flash (vision)
→ Generates detailed room description
        │
        ▼
Gemini 2.0 Flash (text)
→ Produces design suggestions / colour palette / shopping list
        │
        ▼
Stable Diffusion XL (via Hugging Face)
→ Renders photorealistic room visualisation
```

Each tab calls Gemini Vision first to get a room description, then passes that description along with user preferences to the text model for tailored recommendations.

---

## 🔒 Notes on API Usage & Costs

- **Google Gemini** — Both models used here are available on the free tier with generous rate limits. Check [Google AI Studio pricing](https://ai.google.dev/pricing) for details.
- **Hugging Face Inference API** — Free tier supports SDXL with rate limits. For production use, consider the [Serverless Inference API Pro](https://huggingface.co/pricing) plan or self-hosting.
- Results are cached in `st.session_state` for the duration of the session, so switching tabs won't re-trigger API calls.

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `503` error on image generation | The SDXL model is cold-starting. Wait 30 seconds and retry. |
| Gemini API returns empty response | Check your `GOOGLE_API_KEY` is valid and has Gemini API access enabled. |
| `Bearer` authentication fails on HF | Ensure there is a space: `f"Bearer {HF_API_KEY}"` not `f"Bearer{HF_API_KEY}"`. |
| App is slow on first run | Gemini Vision analysis + text generation takes 10–20 seconds per tab. |
| Image looks unrelated to the room | Provide a more detailed description in the Visualize tab's text area. |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

