import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

resp = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role':'user','content':'Hello, explain what AI is in one paragraph.'}]
)
print(resp.choices[0].message.content)

