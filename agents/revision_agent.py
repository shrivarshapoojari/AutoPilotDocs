import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL=os.getenv("MODEL")
def revise_document(topic, original_doc, review_feedback):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an expert documentation writer.

You wrote the following original documentation titled "{topic}":
{original_doc}

It was reviewed with the following feedback:
{review_feedback}

Now, revise and improve the document **based on the feedback**, correcting any inaccuracies, filling in missing details, and clarifying unclear sections.

Return the **full improved Markdown document** only.
    """

    payload = {
        "model":  MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    print(response)
    return response.json()["choices"][0]["message"]["content"]
