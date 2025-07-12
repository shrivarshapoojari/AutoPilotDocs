import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def plan_documents(jira, commits, slack):
    try:
        completion = client.chat.completions.create(
            model="cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a documentation planning agent. Based on:

- Jira Ticket: {jira}
- Git Commits: {commits}
- Slack Messages: {slack}

List 2-3 documentation topics and a one-line reason for each.
Respond in plain text.
                    """
                }
            ]
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"
