import streamlit as st
import cv2
import pytesseract
import numpy as np
import google.generativeai as genai

# ⚠️ WARNING: Hardcoding API keys is not secure for production. Use st.secrets in real deployments.
GOOGLE_API_KEY = "AIzaSyABcgB6_ekXpU1FffEt9ANh2fLEMWRbLu8"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

st.title("📇 Business Card Reader with Gemini AI")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        st.error("Failed to load image.")
    else:
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        extracted_text = pytesseract.image_to_string(gray).strip()
        
        if not extracted_text:
            st.warning("No text found in the image.")
        else:
            st.subheader("📄 Extracted Text")
            st.text_area("OCR Text", extracted_text, height=200)
            
            if st.button("Generate Summary"):
                with st.spinner("Summarizing with Gemini AI..."):
                    prompt = f"""
Summarize the following OCR-extracted content in detail as if you're writing for a university-level report. 
Ensure the summary is at least 150 words, includes the main points, and is clear and structured.

\"\"\"{extracted_text}\"\"\"
"""
                    try:
                        response = model.generate_content(prompt)
                        st.subheader("📝 Gemini Summary")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Gemini API error: {e}")
