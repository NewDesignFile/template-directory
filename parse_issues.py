import json
import re

def extract_url_from_body(body):
    """
    Extracts a URL from the issue body.
    Handles markdown links and direct URLs.
    """
    if not body:
        return None
    # Regex for markdown link: [text](url)
    markdown_match = re.search(r'\[.*?\]\((.*?)\)', body)
    if markdown_match:
        return markdown_match.group(1)

    # Regex for a direct URL
    # This is a simplified regex for URLs and might need to be adjusted
    # for more complex scenarios.
    url_match = re.search(r'https?://[^\s]+', body)
    if url_match:
        return url_match.group(0)

    return None

def parse_github_issues(filepath):
    """
    Parses GitHub issue data from a JSON file.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        list: A list of dictionaries, where each dictionary
              represents an issue with extracted information.
    """
    issues_data = []
    try:
        with open(filepath, 'r') as f:
            issues = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return issues_data
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return issues_data

    for issue in issues:
        issue_number = issue.get("number")
        title = issue.get("title")
        body = issue.get("body")

        # The 'url' in the GitHub API response is the API URL for the issue itself.
        # The subtask asks for the URL of the *tool* mentioned in the issue body.
        tool_url = extract_url_from_body(body)

        issues_data.append({
            "issue_number": issue_number,
            "title": title,
            "body": body,
            "tool_url": tool_url  # Store the extracted tool URL
        })

    return issues_data

if __name__ == "__main__":
    parsed_issues = parse_github_issues("sample_issues.json")
    for issue_info in parsed_issues:
        print(issue_info)
