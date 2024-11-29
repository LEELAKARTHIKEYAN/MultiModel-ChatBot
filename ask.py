import google.generativeai as genai

genai.configure(api_key="AIzaSyBxqpDDdWR0EmIYfXxpXADx5W9WXVm_xLc")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)