import os
from google import genai
from dotenv import load_dotenv

load_dotenv
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-2.5-pro", contents="Explain how AI works in a few words"
)
print(response.text)


# import google.generativeai as genai

# genai.configure()  # Replace with your actual API key
# model = genai.GenerativeModel("gemini-2.5-flash")
# response = model.generate_content("What is the capital of Nigeria?")
# print(response.text)