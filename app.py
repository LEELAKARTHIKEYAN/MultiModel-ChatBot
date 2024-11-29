import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# Configure API key
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    st.error("Google API key not found. Please set it as an environment variable.")
else:
    genai.configure(api_key=API_KEY)

# Configure the models
imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")
gemini = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.title("Multi-Modal AI Chatbot")
st.subheader("Seamlessly handles text and image inputs!")

# Chatbot functionality
user_input_type = st.radio("Choose input type:", ["Text", "Image"])

if user_input_type == "Text":
    user_text = st.text_input("Enter your text:")
    if user_text:
        # Generate Text Response
        with st.spinner("Generating response..."):
            try:
                response = gemini.generate_content([user_text])
                st.text_area("Chatbot Response:", response.text)

                # Generate Image from Text
                if st.button("Generate Image from Text"):
                    with st.spinner("Generating image..."):
                        try:
                            result = gemini.generate_images(
                                prompt=user_text,
                                number_of_images=1,
                                safety_filter_level="block_only_high",
                                person_generation="allow_adult",
                                aspect_ratio="3:4"
                            )
                            image = result.images[0]._pil_image
                            st.image(image, caption="Generated Image")
                        except Exception as e:
                            st.error(f"Error generating image: {e}")
            except Exception as e:
                st.error(f"Error generating text: {e}")

elif user_input_type == "Image":
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image")

        # Generate Text Response from Image
        if st.button("Analyze Image and Generate Text"):
            with st.spinner("Analyzing image and generating response..."):
                try:
                    response = gemini.generate_content(["Tell me about this image:", image])
                    st.text_area("Generated Text:", response.text)
                except Exception as e:
                    st.error(f"Error generating text from image: {e}")

        # Generate Related Image
        if st.button("Generate Related Image"):
            with st.spinner("Generating related image..."):
                try:
                    result = gemini.generate_images(
                        prompt="A related scene to the uploaded image",
                        number_of_images=1,
                        safety_filter_level="block_only_high",
                        person_generation="allow_adult",
                        aspect_ratio="3:4"
                    )
                    generated_image = result.images[0]._pil_image
                    st.image(generated_image, caption="Related Generated Image")
                except Exception as e:
                    st.error(f"Error generating related image: {e}")

# Instructions for running in VS Code
st.sidebar.subheader("Instructions")
st.sidebar.write("""
- Ensure you have set the `API_KEY` environment variable with a valid Google API key.
- Run this script in your terminal using: `streamlit run your_script_name.py`.
- For external access, use tools like `ngrok` to expose the local server.
""")
