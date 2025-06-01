import json

def prepare_corrected_tool_entries(processed_tools_filepath, original_tools_filepath, output_filepath):
    # Load processed tools
    with open(processed_tools_filepath, 'r') as f:
        processed_tools = json.load(f)

    # Load original tools data and extract existing category titles
    existing_category_titles = set()
    try:
        with open(original_tools_filepath, 'r') as f:
            original_data = json.load(f)
        for category_obj in original_data.get("tools", []):
            if category_obj.get("title"):
                existing_category_titles.add(category_obj.get("title"))
    except (FileNotFoundError, json.JSONDecodeError):
        # If original_tools.json is missing or malformed,
        # we can't validate categories. For this task, we'll assume "Xtras"
        # is always a valid fallback, or we could error.
        # Given the problem, "Xtras" is a safe bet.
        pass # existing_category_titles will be empty, all will go to Xtras if not "Xtras"

    if not existing_category_titles:
        # Fallback: if no categories could be loaded, ensure "Xtras" is considered valid
        # so tools proposed as "Xtras" or defaulting to it can be assigned.
        existing_category_titles.add("Xtras")


    corrected_tool_entries = []
    date_added = "2025-06-01"

    for tool in processed_tools:
        proposed_category = tool.get("category")

        final_category = "Xtras" # Default to Xtras
        if proposed_category in existing_category_titles:
            final_category = proposed_category

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
            "tag": "Not available",
            "url": url,
            "date-added": date_added,
            "category": final_category # Store the determined category
        }
        corrected_tool_entries.append(entry)

    with open(output_filepath, 'w') as f:
        json.dump(corrected_tool_entries, f, indent=2)

if __name__ == '__main__':
    prepare_corrected_tool_entries('processed_tools.json', 'src/data/tools.json', 'tool_entries_corrected.json')
