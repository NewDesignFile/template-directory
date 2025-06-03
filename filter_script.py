import json
import re

def normalize_url(url):
    """Normalizes a URL by removing 'https://', 'http://', 'www.', query parameters, and trailing slashes."""
    if not isinstance(url, str):
        return ""
    # Remove scheme (http, https)
    url = re.sub(r"^(https?://)", "", url)
    # Remove www.
    url = re.sub(r"^(www\.)", "", url)
    # Remove query parameters
    url = url.split('?')[0]
    # Remove trailing slash
    if url.endswith('/'):
        url = url[:-1]
    return url.lower()

def filter_duplicates():
    try:
        with open("parsed_issues.json", 'r') as f:
            new_tools = json.load(f)
    except FileNotFoundError:
        print("Error: parsed_issues.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode parsed_issues.json.")
        return

    try:
        with open("src/data/tools.json", 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        print("Error: src/data/tools.json not found.")
        # If existing tools file doesn't exist, then none of the new tools are duplicates.
        existing_tools_list = []
    except json.JSONDecodeError:
        print("Error: Could not decode src/data/tools.json.")
        return

    existing_urls = set()
    if 'tools' in existing_data and isinstance(existing_data['tools'], list):
        for category_group in existing_data['tools']:
            if 'content' in category_group and isinstance(category_group['content'], list):
                for tool in category_group['content']:
                    if 'url' in tool:
                        existing_urls.add(normalize_url(tool['url']))

    print(f"Found {len(existing_urls)} existing URLs to check against.")

    filtered_new_tools = []
    duplicate_count = 0
    for tool in new_tools:
        if 'url' in tool:
            normalized_new_url = normalize_url(tool['url'])
            if normalized_new_url not in existing_urls:
                filtered_new_tools.append(tool)
            else:
                print(f"Duplicate found (and removed): {tool['title']} - {tool['url']} (Normalized: {normalized_new_url})")
                duplicate_count += 1
        else:
            # If a tool has no URL, we can't check for duplicates based on URL.
            # Depending on requirements, it might be added or skipped. Here, we add it.
            filtered_new_tools.append(tool)
            print(f"Tool {tool['title']} has no URL, keeping it.")


    print(f"Removed {duplicate_count} duplicates.")
    print(f"Number of tools after filtering: {len(filtered_new_tools)}")

    try:
        with open("filtered_issues.json", 'w') as f:
            json.dump(filtered_new_tools, f, indent=4)
        print("Filtered tools written to filtered_issues.json")
    except IOError:
        print("Error: Could not write to filtered_issues.json.")

if __name__ == "__main__":
    filter_duplicates()
"""
The script defines a `normalize_url` function that removes "http://", "https://", "www.", query parameters, and trailing slashes, and converts the URL to lowercase for consistent comparison.

The `filter_duplicates` function will:
1. Read `parsed_issues.json`.
2. Read `src/data/tools.json`.
3. Extract all URLs from the nested structure of `src/data/tools.json`, normalize them, and store them in a set (`existing_urls`).
4. Iterate through tools in `parsed_issues.json`. For each tool:
    a. Normalize its URL.
    b. If the normalized URL is NOT in `existing_urls`, add the tool to `filtered_new_tools`.
    c. Print information about duplicates found.
5. Write the `filtered_new_tools` list to `filtered_issues.json`.
Error handling for file not found and JSON decode errors is included.
If a tool in `parsed_issues.json` has no URL, it's currently kept and a message is printed; this can be adjusted based on stricter requirements.
The `?ref=riseofmachine.com` part of existing URLs will be handled by the query parameter removal in `normalize_url`.
"""
