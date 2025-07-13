import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL=os.getenv("MODEL")
def plan_documents(jira, commits, slack, code_diff):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an expert software documentation planner.

Use the following context to determine **which documents need to be written** based on recent GitHub commits and the related project discussion.

---

### 🧾 Jira Ticket:
{jira}

### 🧵 Slack Summary:
{slack}

### 🔀 Git Commit Messages:
{commits}

### 🧠 Code Diffs:
{code_diff}

---

📋 Now, your job is to output a **list of documentation topics**. Each topic should be:

1. Clear
2. Actionable
3. Closely related to what changed in the code

Format as a bullet list like:
- <title> — <1-sentence explanation>

Avoid vague titles. Be specific about modules, classes, configs, or APIs changed.
"""

    payload = {
        "model":  MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    print(res)
    return res.json()["choices"][0]["message"]["content"]
