import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def update_tools_file(new_entries_filepath, main_data_filepath):
    # 1. Load new tool entries
    with open(new_entries_filepath, 'r') as f:
        new_tools_with_category = json.load(f)

    # 2. Load existing tools data
    existing_data_raw = {}
    try:
        with open(main_data_filepath, 'r') as f:
            existing_data_raw = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data_raw = {"tools": []} # Initialize if not found or invalid

    # Convert existing list format to a dictionary for easier manipulation
    # Key: category title (e.g., "Data Annotation"), Value: list of tool objects
    tools_by_category = {}
    for category_obj in existing_data_raw.get("tools", []):
        cat_title = category_obj.get("title")
        if cat_title:
            tools_by_category[cat_title] = category_obj.get("content", [])

    # 3. Process each new tool entry
    for new_tool_entry in new_tools_with_category:
        category_name = new_tool_entry.get("category")
        if not category_name:
            continue # Skip if no category

        # Prepare the tool object (without the 'category' field)
        tool_to_add = {
            "title": new_tool_entry.get("title"),
            "body": new_tool_entry.get("body"),
            "tag": new_tool_entry.get("tag"),
            "url": new_tool_entry.get("url"),
            "date-added": new_tool_entry.get("date-added")
        }

        if category_name not in tools_by_category:
            tools_by_category[category_name] = []

        # Avoid duplicates within the same category based on title
        current_category_tools = tools_by_category[category_name]
        is_duplicate = False
        for existing_tool in current_category_tools:
            if existing_tool.get("title") == tool_to_add.get("title"):
                is_duplicate = True
                break

        if not is_duplicate:
            tools_by_category[category_name].append(tool_to_add)

    # 4. Sort tools within each category
    for category_name in tools_by_category:
        tools_by_category[category_name].sort(key=lambda x: x.get("title", "").lower())

    # 5. Convert back to the original list-of-objects format, sorted by category title
    output_data_list = []
    sorted_category_names = sorted(tools_by_category.keys(), key=lambda x: x.lower())

    for category_name in sorted_category_names:
        output_data_list.append({
            "title": category_name,
            "category": slugify(category_name),
            "content": tools_by_category[category_name]
        })

    final_output_structure = {"tools": output_data_list}

    # 6. Write updated data back
    with open(main_data_filepath, 'w') as f:
        json.dump(final_output_structure, f, indent=2)

if __name__ == '__main__':
    update_tools_file('tool_entries.json', 'src/data/tools.json')
