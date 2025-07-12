import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

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
            model="cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"
