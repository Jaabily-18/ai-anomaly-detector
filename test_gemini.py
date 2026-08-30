import os
from google import genai
from dotenv import load_dotenv

# Load key from .env file
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use the recommended active model
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Explain in one sentence why automated anomaly detection is useful for businesses."
)

print("\n🤖 Response from Gemini:")
print(response.text)