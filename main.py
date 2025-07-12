from agents.perception_agent import load_input
from agents.planning_agent import plan_documents
from agents.execution_agent import generate_document

def main():
    data = load_input()
    jira, commits, slack = data["jira_ticket"], data["git_commits"], data["slack_messages"]

    print("🔍 Planning documentation tasks...")
    plan = plan_documents(jira, commits, slack)
    print("\n🧠 Plan:\n", plan)

    # Simplified: manually extract 2 topics
    topics = ["Stripe Integration Setup", "Removing Legacy Payment Flow"]

    for topic in topics:
        print(f"\n✍️ Generating document for: {topic}")
        doc = generate_document(topic, data)
        filename = f"docs/{topic.replace(' ', '_').lower()}.md"
        with open(filename, "w") as f:
            f.write(doc)
        print(f"✅ Document saved: {filename}")

if __name__ == "__main__":
    main()
