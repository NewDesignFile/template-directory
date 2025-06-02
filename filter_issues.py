import json
import re

# Copied from parse_issues.py for self-containment in this step
def extract_url_from_body(body):
    """
    Extracts a URL from the issue body.
    Handles markdown links and direct URLs.
    Returns the first found URL.
    """
    if not body:
        return None
    # Regex for markdown link: [text](url)
    markdown_match = re.search(r'\[.*?\]\((.*?)\)', body)
    if markdown_match:
        return markdown_match.group(1)

    # Regex for a direct URL (simplified)
    url_match = re.search(r'https?://[^\s/$.?#].[^\s]*', body) # Made slightly more robust
    if url_match:
        url = url_match.group(0)
        # Remove common trailing punctuation
        return url.rstrip('.,;)!?')

    return None

# Function to parse the initial JSON data (simplified from parse_issues.py)
def load_issues_from_file(filepath):
    """
    Loads and parses GitHub issue data from a JSON file.
    Extracts number, title, body, and the tool URL from the body.
    """
    parsed_issue_data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            issues = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return parsed_issue_data
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return parsed_issue_data

    for issue in issues:
        issue_number = issue.get("number")
        title = issue.get("title")
        body = issue.get("body")
        # This 'url' key will store the tool URL extracted from the body
        tool_url_from_body = extract_url_from_body(body)

        parsed_issue_data.append({
            "number": issue_number,
            "title": title, # In the example output, title seems to be the URL if original title is also a URL.
                           # For now, I'll keep the original title and the extracted tool_url separate.
                           # The example output for selected_tools.json has "title" as the URL, and a separate "url" field also as the URL.
                           # I will store the extracted tool URL in 'tool_url' and keep original 'title' and 'body'.
            "body": body,
            "tool_url": tool_url_from_body
        })
    return parsed_issue_data

AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "nlp", "natural language processing", "computer vision",
    "neural network", "llm", "genai", "language model"
]

def is_ai_related(issue_data):
    """
    Simulates checking if a tool is AI-related based on keywords
    in the title, body, or the tool_url itself.
    """
    if not issue_data.get("tool_url"): # Only consider issues with a tool URL
        return False

    text_to_check = [
        str(issue_data.get("title", "")).lower(),
        str(issue_data.get("body", "")).lower(),
        str(issue_data.get("tool_url", "")).lower()
    ]

    for text_item in text_to_check:
        for keyword in AI_KEYWORDS:
            if keyword in text_item:
                return True
    return False

def filter_and_select_issues(input_filepath="sample_issues.json", output_filepath="selected_ai_tools.json", max_select=5):
    """
    Filters issues based on AI relevance (simulated), valid URL, and no duplicates,
    then saves the selected issues to a JSON file.
    """
    all_issues = load_issues_from_file(input_filepath)

    selected_issues = []
    selected_tool_urls = set()

    for issue in all_issues:
        if len(selected_issues) >= max_select:
            break

        tool_url = issue.get("tool_url")

        if not tool_url: # Must have a tool URL
            continue

        if tool_url in selected_tool_urls: # Avoid duplicates
            continue

        if is_ai_related(issue): # Check if AI-related (simulated)
            # Re-structuring the output to somewhat match the example:
            # The example output for selected_tools.json has "title" as the URL, and a separate "url" field also as the URL.
            # This is a bit redundant. I will output the original issue structure for the selected items.
            # If specific reformatting is needed, it can be a separate step.
            # For now, I'll keep the structure from load_issues_from_file.
            # The example also only includes number, title (as URL), body, and url (as URL).
            # I'll create a new dict for the output to match the example format.

            output_issue_format = {
                "number": issue["number"],
                "title": tool_url, # As per example, title field in output is the tool URL
                "body": issue["body"], # Original body
                "url": tool_url # As per example, url field in output is also the tool URL
            }
            selected_issues.append(output_issue_format)
            selected_tool_urls.add(tool_url)

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(selected_issues, f, indent=2)
        print(f"Selected AI tools written to {output_filepath}")
    except IOError:
        print(f"Error: Could not write to {output_filepath}")

    return selected_issues

if __name__ == "__main__":
    selected = filter_and_select_issues()
    print(f"\nSelected {len(selected)} tools:")
    for item in selected:
        print(item)
