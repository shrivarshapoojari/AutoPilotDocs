import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def generate_document(topic, context):
    try:
        prompt = f"""
Write a full markdown document for: {topic}

Use the following context:
{context}

Make it clear, structured, and professional.
        """

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        print(f"completion {completion}")
        
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"
