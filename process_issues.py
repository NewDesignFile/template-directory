import re

def fetch_issues():
    """Simulates fetching issues from a GitHub repository."""
    return [
        {
            "title": "AI Code Assistant",
            "body": "An AI-powered tool for code completion and suggestion. URL: http://example.com/ai-code-assistant",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "Image Editor",
            "body": "A simple image editor. URL: http://example.com/image-editor",
            "labels": []
        },
        {
            "title": "AI Text Summarizer",
            "body": "Summarizes long texts using AI. URL: http://example.com/ai-text-summarizer. Category: Text Generation",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "Task Management Tool",
            "body": "A tool for managing tasks and projects. URL: http://example.com/task-manager",
            "labels": []
        },
        {
            "title": "AI Chatbot Platform",
            "body": "Platform for building AI chatbots. URL: http://example.com/ai-chatbot-platform. Category: Chatbots",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "AI Code Assistant", # Duplicate
            "body": "An AI-powered tool for code completion and suggestion. URL: http://example.com/ai-code-assistant",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "AI Data Visualization Tool",
            "body": "Generates interactive data visualizations using AI. URL: http://example.com/ai-data-visualization. Category: Data Analysis",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "Video Editing Software",
            "body": "Software for professional video editing. URL: http://example.com/video-editor",
            "labels": []
        },
         {
            "title": "AI Language Translation Service",
            "body": "AI-powered translation for multiple languages. URL: http://example.com/ai-language-translation. Category: Language",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "AI Writing Assistant",
            "body": "Helps improve writing style and grammar using AI. URL: http://example.com/ai-writing-assistant. Category: Writing",
            "labels": [{"name": "AI"}]
        }
    ]

def parse_issue(issue):
    """Parses issue title and body to extract tool information."""
    name = issue["title"]
    body = issue["body"]

    url_match = re.search(r"URL: (http[s]?://[^\s]+)", body)
    url = url_match.group(1).rstrip('.') if url_match else None # Remove trailing period

    category_match = re.search(r"Category: ([A-Za-z\s]+)", body)
    category = category_match.group(1).strip() if category_match else "General"

    return name, url, category, body

def is_ai_tool(issue_title, issue_body, issue_labels):
    """Checks if the tool is AI-related."""
    ai_keywords = ["ai", "artificial intelligence", "machine learning", "deep learning"]
    if any(keyword in issue_title.lower() for keyword in ai_keywords):
        return True
    if any(keyword in issue_body.lower() for keyword in ai_keywords):
        return True
    if any("AI" in label["name"] for label in issue_labels):
        return True
    return False

def format_tool_name(name):
    """Formats the tool name."""
    if name.lower().startswith("ai "):
        name = name[3:]
    return name.strip()

def format_title(title):
    """Formats the title to be short and in title case (max 3 words)."""
    words = title.split()
    return " ".join(words[:3]).title()

def format_description(body):
    """Formats the body description text to be short and in sentence case (max 50 characters)."""
    # First, try to extract a sentence.
    sentences = re.split(r'(?<=[.!?])\s+', body)
    description = sentences[0] if sentences else body

    # If the first sentence is too long, or no sentence was found, truncate.
    if len(description) > 50 or not sentences or len(sentences[0]) == 0: # check if sentence is empty
        description = body
        if len(description) > 50:
            description = description[:50]
            last_space = description.rfind(' ')
            if last_space != -1:
                description = description[:last_space]
            description += "..."


    # Ensure "AI" is capitalized
    description = re.sub(r'\bai\b', 'AI', description, flags=re.IGNORECASE)

    # Capitalize the first letter of the sentence
    if description:
        description = description[0].upper() + description[1:]

    return description


def process_tools():
    """Processes issues to filter and format AI tools."""
    issues = fetch_issues()
    ai_tools = []
    added_tools = set() # To keep track of added tool URLs to avoid duplicates

    for issue in issues:
        if not is_ai_tool(issue["title"], issue["body"], issue.get("labels", [])):
            print(f"Closing issue (non-AI): {issue['title']}") # Simulate closing issue
            continue

        name, url, category, body_text = parse_issue(issue)

        if url in added_tools:
            print(f"Skipping duplicate tool: {name}")
            continue

        if not url:
            print(f"Skipping tool due to missing URL: {name}")
            continue

        formatted_name = format_tool_name(name)
        formatted_title = format_title(formatted_name)
        formatted_description = format_description(body_text)

        ai_tools.append({
            "name": formatted_name,
            "title": formatted_title,
            "url": url,
            "category": category,
            "description": formatted_description
        })
        added_tools.add(url)

        if len(ai_tools) >= 5: # Collect 4-5 tools
            break

    return ai_tools

if __name__ == "__main__":
    processed_tools = process_tools()
    for tool in processed_tools:
        print(tool)
