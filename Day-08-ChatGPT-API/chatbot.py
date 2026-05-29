import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

def main():
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    # Clean placeholders if they are not actual keys
    if openai_key == "insira_sua_chave_aqui":
        openai_key = None
    if gemini_key == "insira_sua_chave_aqui":
        gemini_key = None

    if not openai_key and not gemini_key:
        print("\nError: No API keys found in your .env file.")
        print("Please configure at least one of the following in your .env file:")
        print("OPENAI_API_KEY=your_openai_key")
        print("GEMINI_API_KEY=your_gemini_key\n")
        sys.exit(1)

    # Determine provider
    provider = None
    if openai_key and gemini_key:
        print("Multiple API keys found:")
        print("1) OpenAI (GPT-4o-mini)")
        print("2) Google Gemini (Gemini 2.5 Flash)")
        choice = input("Select your AI provider (1 or 2) [Default: 2]: ").strip()
        if choice == "1":
            provider = "openai"
        else:
            provider = "gemini"
    elif openai_key:
        provider = "openai"
    else:
        provider = "gemini"

    print("=" * 60)
    print(f" Welcome to the AI Console Chatbot ({provider.upper()})! ")
    print(" Type 'exit' or 'quit' to end the conversation.")
    print("=" * 60)

    # Initialize selected provider
    if provider == "openai":
        client = OpenAI(api_key=openai_key)
        messages = [
            {"role": "system", "content": "You are a helpful, concise, and friendly AI assistant."}
        ]
    else:
        # Initialize Gemini Client
        client = genai.Client(api_key=gemini_key)
        # Create a chat session with system instruction
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful, concise, and friendly AI assistant.",
                temperature=0.7
            )
        )

    while True:
        try:
            # Prompt user for input
            user_input = input("\nYou: ").strip()
            
            # Handle exit conditions
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            # Skip empty inputs
            if not user_input:
                continue

            print("AI: ", end="", flush=True)

            if provider == "openai":
                messages.append({"role": "user", "content": user_input})
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    stream=True
                )
                collected_chunks = []
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        print(content, end="", flush=True)
                        collected_chunks.append(content)
                print()
                full_response = "".join(collected_chunks)
                messages.append({"role": "assistant", "content": full_response})
            else:
                # Gemini streaming chat response
                response_stream = chat.send_message_stream(user_input)
                for chunk in response_stream:
                    print(chunk.text, end="", flush=True)
                print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            if provider == "openai" and messages[-1]["role"] == "user":
                messages.pop()

if __name__ == "__main__":
    main()
