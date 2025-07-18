import streamlit as st
from PIL import Image
import easyocr
import google.generativeai as genai

# Set your Google API Key
GOOGLE_API_KEY = "AIzaSyABcgB6_ekXpU1FffEt9ANh2fLEMWRbLu8"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")
st.title("📇 Business Card Reader with Gemini AI")

uploaded_image = st.file_uploader("Upload Business Card", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Extracting text..."):
        reader = easyocr.Reader(['en'], gpu=False)
        text = reader.readtext(uploaded_image, detail=0)
        extracted_text = "\n".join(text)

    st.text_area("Extracted Text", extracted_text, height=200)

    if st.button("Analyze with Gemini"):
        prompt = f"""Extract key information from this business card text:

{extracted_text}

Format:
- Name:
- Job Title:
- Company:
- Email:
- Phone:
- Address:
"""
        response = model.generate_content(prompt)
        st.markdown(response.text)

