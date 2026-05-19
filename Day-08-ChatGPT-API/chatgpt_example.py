import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

resp = openai.ChatCompletion.create(
    model='gpt-4o-mini',
    messages=[{'role':'user','content':'Hello, explain what AI is in one paragraph.'}]
)
print(resp['choices'][0]['message']['content'])
