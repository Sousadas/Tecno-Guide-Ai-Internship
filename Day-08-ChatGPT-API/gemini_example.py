import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini GenAI client
# It automatically picks up the GEMINI_API_KEY from environment variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use the recommended gemini-2.5-flash model
print("Calling Gemini API...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello, explain what AI is in one paragraph."
)

print("\nResponse from Gemini:")
print(response.text)
