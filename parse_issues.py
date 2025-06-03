import re

issues_text = """
Issue 1 (ID: 33):
Title: aicode.help
Body: ### 1. Website Link
- aicode.help

### 2. Category (Optional)
- LLMs
Link: aicode.help
Category: LLMs

Issue 2 (ID: 32):
Title: offlinechat.chat
Body: ### 1. Website Link
- offlinechat.chat

### 2. Category (Optional)
- LLMs
Link: offlinechat.chat
Category: LLMs

Issue 3 (ID: 30):
Title: https://www.papergen.i
Body: ### 1. Website Link
- https://www.papergen.i/

### 2. Category (Optional)
- Copywriting
Link: https://www.papergen.i/
Category: Copywriting

Issue 4 (ID: 26):
Title: https://omnigen.co
Body: ### 1. Website Link
- https://omnigen.co/

### 2. Category (Optional)
- What category best describes this tool?

Link: https://omnigen.co/
Category: Xtras (fallback category since it's not specified)

Issue 5 (ID: 24):
Title: https://www.usesaaskit.com
Body: ### 1. Website Link
- https://www.usesaaskit.com/

### 2. Category (Optional)
- Developer
Link: https://www.usesaaskit.com/
Category: Developer
"""

tools = []
# Split into individual issues
issues = issues_text.strip().split("\n\nIssue ")
# Remove the "Issue " prefix from the first element if it exists
if issues[0].startswith("Issue "):
    issues[0] = issues[0][len("Issue "):]
else: # if it's just one issue
    issues = [issues_text.strip()]


for issue_block in issues:
    if not issue_block.strip():
        continue

    tool_name = "Unknown"
    url = "Unknown"
    category = "Xtras" # Default category

    title_match = re.search(r"Title: (.*)", issue_block)
    if title_match:
        title_text = title_match.group(1).strip()
        # Basic cleaning for tool name from title: remove "https://www." and trailing "/"
        tool_name = re.sub(r"^https?://(www\.)?", "", title_text)
        tool_name = re.sub(r"/$", "", tool_name)

    # Regex to find link, allowing for optional scheme
    link_pattern = r"((?:https?://)?[^\s/]+(?:/[^\s]*)?)"

    link_match_body = re.search(r"### 1\. Website Link\s*-\s*" + link_pattern, issue_block, re.IGNORECASE)
    link_match_end = re.search(r"Link: " + link_pattern, issue_block, re.IGNORECASE)

    # Prioritize link from "### 1. Website Link" then "Link:"
    chosen_link_match = None
    if link_match_body:
        chosen_link_match = link_match_body
    elif link_match_end:
        chosen_link_match = link_match_end

    if chosen_link_match:
        url_text = chosen_link_match.group(1).strip()
        if not url_text.startswith("http://") and not url_text.startswith("https://"):
            url = "https://" + url_text
        else:
            url = url_text

        # If tool_name is still "Unknown" or looks like a generic URL, try to get a better name from the URL
        # Also, if the title was a full URL, the extracted tool_name might be identical to the URL text.
        # In such cases, we prefer a cleaner name derived from the URL (domain name).
        if tool_name == "Unknown" or tool_name.startswith("http") or tool_name == url_text or tool_name == url_text.replace("https://","").replace("http://",""):
            name_from_url = re.sub(r"^https?://(www\.)?", "", url)
            name_from_url = re.sub(r"/$", "", name_from_url) # Remove trailing slash for name
            name_from_url = name_from_url.split('/')[0] # Get only domain part for name
            if name_from_url:
                tool_name = name_from_url


    category_match_body = re.search(r"### 2\. Category \(Optional\)\s*-\s*(.*)", issue_block, re.IGNORECASE)
    category_match_end = re.search(r"Category: (.*)", issue_block, re.IGNORECASE)

    chosen_category_text = None
    if category_match_body:
        chosen_category_text = category_match_body.group(1).strip()
    elif category_match_end:
        chosen_category_text = category_match_end.group(1).strip()

    if chosen_category_text:
        if chosen_category_text and \
           "What category best describes this tool?" not in chosen_category_text and \
           "Xtras (fallback category since it's not specified)" not in chosen_category_text:
            category = chosen_category_text
        elif "Xtras (fallback category since it's not specified)" in chosen_category_text:
            category = "Xtras"
        # If category is empty after stripping, keep it as Xtras or the previously set value.
        elif not chosen_category_text:
            pass # Keep default Xtras or previously parsed if any

    tools.append({"name": tool_name, "url": url, "category": category})

print("Structured List of Tools:")
for tool in tools:
    print(f"- Name: {tool['name']}, URL: {tool['url']}, Category: {tool['category']}")

print("\nProcessed all issues.")
