import re
from agents.perception_agent import load_input
from agents.planning_agent import plan_documents
from agents.execution_agent import generate_document

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a string to make it safe for use as a filename.
    """
    # Remove or replace invalid characters for filenames
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove extra dots and asterisks
    filename = re.sub(r'[.*]+', '', filename)
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    # Strip leading/trailing underscores
    filename = filename.strip('_')
    return filename.lower()

def extract_topics(plan_output: str) -> list[str]:
    """
    Very lightweight parser:
    • Looks for lines that start with a dash, number, or bullet,
      then grabs the text up to a dash/colon or EOL.
    • Adjust the regex if your Planning Agent formats lines differently.
    """
    topics = []
    for line in plan_output.strip().splitlines():
        # Examples the regex catches:
        #   1. **Stripe Integration Setup** – explains ...
        #   - Removing Legacy Payment Flow: details ...
        m = re.match(r"^\s*\d+\.\s*\**(.*?)\**(?:\s*[—\-:–]|$)", line)
        if m:
            topic = m.group(1).strip()
            # Remove any remaining markdown formatting and clean up
            topic = re.sub(r'\*+', '', topic)  # Remove asterisks
            topic = topic.strip()
            # Skip obviously empty captures
            if topic:
                topics.append(topic)
    return topics

def main():
    data = load_input()
    jira, commits, slack = data["jira_ticket"], data["git_commits"], data["slack_messages"]

    print("🔍 Planning documentation tasks...")
    plan = plan_documents(jira, commits, slack)
    print("\n🧠 Plan:\n", plan)

    topics = extract_topics(plan)
    if not topics:
        print("⚠️  No topics detected — check Planning Agent output or tweak regex.")
        return

    print("\n📋 Extracted topics:", topics)

    for topic in topics:
        print(f"\n✍️  Generating document for: {topic}")
        doc = generate_document(topic, data)
        filename = f"docs/{sanitize_filename(topic)}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"✅ Document saved → {filename}")

if __name__ == "__main__":
    main()
