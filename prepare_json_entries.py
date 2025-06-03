import json
import re
from datetime import datetime

def title_case(s):
    return ' '.join(word.capitalize() for word in s.split())

def sentence_case(s):
    if not s:
        return ""
    return s[0].upper() + s[1:].lower()

def format_title_for_json(original_title_str):
    if not isinstance(original_title_str, str):
        original_title_str = "Unknown Tool"

    # Remove schema and www.
    title = re.sub(r"^(https?://)?(www\.)?", "", original_title_str)

    # Remove trailing slash or other common URL endings if present in title
    title = re.sub(r"(/)$", "", title)
    title = title.replace(".com", "").replace(".io", "").replace(".ai", "").replace(".co", "").replace(".tech", "").replace(".help", "").replace(".chat", "").replace(".i", "") # specific for given examples

    # If the tool name starts with "AI" (case-insensitive), trim the "AI" part.
    if title.lower().startswith("ai") and len(title) > 2 and not title[2].islower(): # e.g. AICode but not Aim
         title = title[2:].lstrip()

    # Convert to title case
    title = title_case(title)

    # Limit to max 3 words
    words = title.split()
    if len(words) > 3:
        title = " ".join(words[:3])

    return title.strip() if title.strip() else "Unknown Tool"

def format_body_for_json(description, formatted_tool_title):
    if description == "Not available" or not description:
        # Use the tool's title (already formatted) as the body, in sentence case.
        body_text = sentence_case(formatted_tool_title)
    else:
        # Ensure sentence case for the description.
        body_text = sentence_case(description)

    # Ensure max 50 characters (already a rule for fetching, but double check)
    return body_text[:50] if len(body_text) > 50 else body_text

def format_url_for_json(original_url_str):
    if not isinstance(original_url_str, str) or not original_url_str.strip():
        return "https://example.com?ref=riseofmachine.com" # Fallback for missing URL

    url = original_url_str
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Append query parameter
    if '?' in url:
        url += '&ref=riseofmachine.com'
    else:
        url += '?ref=riseofmachine.com'
    return url

def format_tag_for_json(pricing_tag_str):
    # If the pricing_tag is "Not available", use "Not available" as the tag.
    # This is already handled as the input pricing_tag will be "Not available".
    return pricing_tag_str if pricing_tag_str else "Not available"

def main():
    try:
        with open('tools_with_details.json', 'r') as f:
            tools_with_details = json.load(f)
    except FileNotFoundError:
        print("Error: tools_with_details.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode tools_with_details.json.")
        return

    prepared_tools = []
    date_added = "2025-06-03" # Today's date as specified

    for tool in tools_with_details:
        original_title = tool.get('title', '')
        description = tool.get('description', 'Not available')
        pricing_tag = tool.get('pricing_tag', 'Not available')
        original_url = tool.get('url', '')

        formatted_title = format_title_for_json(original_title)
        formatted_body = format_body_for_json(description, formatted_title)
        formatted_url = format_url_for_json(original_url)
        formatted_tag = format_tag_for_json(pricing_tag)

        prepared_tool_entry = {
            "title": formatted_title,
            "body": formatted_body,
            "tag": formatted_tag,
            "url": formatted_url,
            "date-added": date_added
        }
        prepared_tools.append(prepared_tool_entry)

    try:
        with open('prepared_tools.json', 'w') as f:
            json.dump(prepared_tools, f, indent=2) # Indent with 2 spaces as per example
        print("Successfully created prepared_tools.json")
    except IOError:
        print("Error: Could not write to prepared_tools.json.")

if __name__ == '__main__':
    main()
