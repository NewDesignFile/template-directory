import json

def transform_tools_data(input_filepath, output_filepath):
    with open(input_filepath, 'r') as f:
        processed_tools = json.load(f)

    transformed_entries = []
    date_added = "2025-06-01" # As specified

    for tool in processed_tools:
        # Determine category, defaulting to "Xtras" if original category is "Other" or not specific enough
        category = tool.get("category", "Xtras")
        if category == "Other":
            category = "Xtras"

        # Ensure URL has the ref query parameter
        url = tool.get("url", "")
        if "?ref=riseofmachine.com" not in url:
            if "?" in url:
                url += "&ref=riseofmachine.com"
            else:
                url += "?ref=riseofmachine.com"

        entry = {
            "title": tool.get("title", "N/A"),
            "body": tool.get("body", "N/A"),
            "tag": "Not available", # As specified
            "url": url,
            "date-added": date_added,
            "category": category # Carry over category for later use
        }
        transformed_entries.append(entry)

    with open(output_filepath, 'w') as f:
        json.dump(transformed_entries, f, indent=2)

if __name__ == '__main__':
    transform_tools_data('processed_tools.json', 'tool_entries.json')
