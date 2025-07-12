import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def verify_document(topic, generated_doc, context_data):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a senior documentation reviewer.

Review the following document titled "{topic}" for correctness, clarity, and completeness.

## Context:
- Jira Ticket: {context_data['jira_ticket']}
- Git Commits: {context_data['git_commits']}
- Slack Messages: {context_data['slack_messages']}

## Document:
{generated_doc}

## Your Task:
Write a Markdown review with the following sections:
1. ✅ Accuracy Check — are all facts consistent with the context?
2. 🔍 Missing Information — what important details were left out?
3. 💬 Clarity Suggestions — which sections need clearer language?
4. 📈 Overall Feedback — 1-2 line summary and improvement ideas.
    """

    payload = {
        "model": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    print(response)
    return response.json()["choices"][0]["message"]["content"]
