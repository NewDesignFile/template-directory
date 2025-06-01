import json
import re

def to_title_case(text):
    return ' '.join(word.capitalize() for word in text.split())

def to_sentence_case(text):
    if not text:
        return ""
    text = text.strip()
    return text[0].upper() + text[1:].lower()

def process_issues(input_filepath, output_filepath):
    with open(input_filepath, 'r') as f:
        issues = json.load(f)

    processed_tools = []
    seen_titles = set()
    tools_added_count = 0

    for issue in issues:
        is_ai_tool = False
        category = "Other" # Default category
        raw_labels = issue.get("labels", [])

        for label in raw_labels:
            if label.get("name") == "AI tool":
                is_ai_tool = True
            elif category == "Other": # Assign first non-"AI tool" label as category
                category = label.get("name", "Other")


        if not is_ai_tool:
            continue

        title = issue.get("title", "")
        body = issue.get("body", "")
        url = issue.get("html_url", "")

        # Process title
        if title.lower().startswith("ai tool: "):
            title = title[len("ai tool: "):]

        title_words = title.split()
        title = to_title_case(' '.join(title_words[:3]))

        # Process body
        body = to_sentence_case(body)
        if len(body) > 50:
            body = body[:47] + "..."

        # Check for duplicates and limit to 4-5 tools
        if title and title not in seen_titles:
            if tools_added_count < 5: # Select 4-5 tools, here limiting to 5
                processed_tools.append({
                    "title": title,
                    "body": body,
                    "url": url,
                    "category": category
                })
                seen_titles.add(title)
                tools_added_count += 1
            else:
                break # Stop after collecting 5 tools

    with open(output_filepath, 'w') as f:
        json.dump(processed_tools, f, indent=2)

if __name__ == '__main__':
    process_issues('github_issues.json', 'processed_tools.json')
