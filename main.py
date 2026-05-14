# 1
from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def main():
    print("--- AI responding ---")
    
    target_model = 'gemini-3.1-flash-lite' 
    
    try:
        response_stream = client.models.generate_content_stream(
            model=target_model,
            contents='Explain async programming in 100 words.'
        )

        for chunk in response_stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                
    except Exception as e:
        print(f"\n❌ error: {e}")

if __name__ == "__main__":
    main()