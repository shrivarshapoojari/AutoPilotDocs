import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "shrivarshapoojari/CloudNote-Spring"

def fetch_code_context():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
 
    commits_url = f"https://api.github.com/repos/{REPO}/commits"
    commits_res = requests.get(commits_url, headers=headers)
    
    if commits_res.status_code != 200:
        print(f"GitHub API Error: {commits_res.status_code} - {commits_res.text}")
        # Return mock data if API fails
        return {
            "jira_ticket": "DOCGEN-42 | Add Stripe retry logic and clean up legacy flow",
            "git_commits": ["Mock commit: Add Stripe integration", "Mock commit: Remove PayPal legacy code"],
            "slack_messages": ["Team: remember to document retry logic + legacy removal"],
            "code_diff_context": "Mock code context - API unavailable"
        }
    
    commits_data = commits_res.json()
    
    # Check if commits_data is a list (successful response) or dict (error response)
    if not isinstance(commits_data, list):
        print(f"Unexpected GitHub API response: {commits_data}")
        # Return mock data if response is not as expected
        return {
            "jira_ticket": "DOCGEN-42 | Add Stripe retry logic and clean up legacy flow", 
            "git_commits": ["Mock commit: Add Stripe integration", "Mock commit: Remove PayPal legacy code"],
            "slack_messages": ["Team: remember to document retry logic + legacy removal"],
            "code_diff_context": "Mock code context - API response error"
        }

    code_context = []

    for commit in commits_data[:3]:  # 3 latest commits
        sha = commit["sha"]
        message = commit["commit"]["message"]

        # 🔍 Step 2: Get full commit details (includes diffs)
        detail_url = f"https://api.github.com/repos/{REPO}/commits/{sha}"
        detail_res = requests.get(detail_url, headers=headers)
        detail_data = detail_res.json()

        files_info = []

        for file in detail_data.get("files", []):
            filename = file["filename"]
            patch = file.get("patch", "[diff not available]")
            files_info.append(f"\n### {filename}\n```diff\n{patch}\n```")

     
        code_entry = f"""
## Commit: {message}
SHA: {sha}
{''.join(files_info)}
        """
        code_context.append(code_entry)
    
    return {
        "jira_ticket": "CloudNotes improvements",
        "git_commits": [c["commit"]["message"] for c in commits_data[:1]],
        "slack_messages": ["Team: Cloud note updates"],
        "code_diff_context": "\n\n".join(code_context)
    }

def load_input(file_path="data/mock_input.json"):
    """
    Load input data. This function can load from file or fetch live data.
    For now, it fetches live code context from GitHub.
    """
    return fetch_code_context()
