import streamlit as st
from PIL import Image
import easyocr
import google.generativeai as genai

# Set your Google API Key
GOOGLE_API_KEY = "AIzaSyABcgB6_ekXpU1FffEt9ANh2fLEMWRbLu8"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

st.set_page_config(page_title="Business Card Reader", layout="centered")
st.title("📇 Business Card Reader with Gemini AI")

uploaded_image = st.file_uploader("Upload a Business Card Image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Business Card", use_column_width=True)

    with st.spinner("🔍 Extracting text from image..."):
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(uploaded_image, detail=0)
        extracted_text = "\n".join(result)

    st.success("✅ Text Extracted")
    st.subheader("📄 Raw Extracted Text")
    st.text_area("Text", extracted_text, height=200)

    if st.button("🔍 Analyze with Gemini"):
        with st.spinner("Thinking..."):
            prompt = f"""Extract key information from the following business card text:

{extracted_text}

Return it in this format:
- Name:
- Job Title:
- Company:
- Email:
- Phone:
- Address:
"""
            response = model.generate_content(prompt)
        st.success("✅ Gemini AI Result")
        st.markdown(response.text)
