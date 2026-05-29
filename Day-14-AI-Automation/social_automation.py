import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini Client
# Ensure you have GEMINI_API_KEY set in your .env file
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

def generate_caption(topic: str, platform: str = "Twitter") -> str:
    """
    Generates a social media caption using Gemini.
    """
    if not client:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return None
        
    prompt = f"You are an expert social media manager. Write an engaging, highly-converting {platform} caption about: {topic}. Include relevant hashtags and emojis. Keep it under 280 characters if Twitter."
    
    try:
        # Using the standard model for general text tasks
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        # If the model is experiencing high demand (503), try a fallback model
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            print("⏳ Model gemini-2.5-flash is busy. Trying fallback model (gemini-1.5-flash)...")
            try:
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                return response.text.strip()
            except Exception as fallback_e:
                print(f"Error generating caption with fallback: {fallback_e}")
                return None
        else:
            print(f"Error generating caption: {e}")
            return None

def save_to_cms(topic: str, platform: str, caption: str):
    """
    Simulates saving the generated content to a CMS (by saving it to a local file).
    """
    # Create CMS directory if it doesn't exist
    cms_dir = os.path.join(os.path.dirname(__file__), "CMS")
    os.makedirs(cms_dir, exist_ok=True)
    
    # Create a safe filename
    safe_topic = "".join([c if c.isalnum() else "_" for c in topic]).lower()[:20]
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{platform.lower()}_{safe_topic}.md"
    filepath = os.path.join(cms_dir, filename)
    
    content = f"# Topic: {topic}\n"
    content += f"**Platform:** {platform}\n"
    content += f"**Generated At:** {datetime.now().isoformat()}\n\n"
    content += f"## Caption\n\n{caption}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✅ Successfully saved content to CMS: {filepath}")

def main():
    print("🤖 Welcome to the AI Social Media Automation Tool!")
    print("--------------------------------------------------")
    
    topic = input("What is the topic of your post? ")
    platform = input("Which platform (e.g., Twitter, LinkedIn, Instagram)? [Default: Twitter]: ")
    if not platform:
        platform = "Twitter"
        
    print(f"\n⏳ Generating {platform} caption for '{topic}'...")
    
    caption = generate_caption(topic, platform)
    
    if caption:
        print("\n✨ Generated Caption ✨")
        print("--------------------------------------------------")
        print(caption)
        print("--------------------------------------------------\n")
        
        save_choice = input("Do you want to save this to the CMS? (y/n): ")
        if save_choice.lower() == 'y':
            save_to_cms(topic, platform, caption)
        else:
            print("Content discarded.")
    else:
        print("Failed to generate caption. Please check your API key.")

if __name__ == "__main__":
    main()
