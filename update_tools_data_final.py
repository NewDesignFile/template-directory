import json
import re

def slugify(text):
    # Basic slugification: lowercase, spaces to hyphens, remove other non-alphanumerics
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def merge_tools_into_main_data(corrected_entries_filepath, main_data_filepath):
    # 1. Load corrected tool entries
    with open(corrected_entries_filepath, 'r') as f:
        corrected_tools = json.load(f)

    # 2. Load existing main tools data
    main_data = {}
    try:
        with open(main_data_filepath, 'r') as f:
            main_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize with a basic structure if file is missing or corrupt
        main_data = {"tools": []}

    # For easier manipulation, convert the list of category objects to a dictionary
    # where key is category title.
    categories_dict = {cat_obj["title"]: cat_obj for cat_obj in main_data.get("tools", [])}

    # 3. Process each corrected tool entry
    for tool_entry in corrected_tools:
        category_name = tool_entry.get("category") # Should mostly be "Xtras"
        if not category_name:
            print(f"Skipping tool without category: {tool_entry.get('title')}")
            continue

        tool_to_add = {
            "title": tool_entry.get("title"),
            "body": tool_entry.get("body"),
            "tag": tool_entry.get("tag"),
            "url": tool_entry.get("url"),
            "date-added": tool_entry.get("date-added")
        }

        # Find or create the category in our dictionary
        if category_name not in categories_dict:
            # This case should ideally not happen if "Xtras" always exists
            # or if categories were pre-validated perfectly.
            # However, to be robust for the "Xtras" case:
            categories_dict[category_name] = {
                "title": category_name,
                "category": slugify(category_name),
                "content": []
            }
            print(f"Warning: Category '{category_name}' was not in main_data.json, created it.")


        category_obj = categories_dict[category_name]

        # Check for duplicates by title within this category's content
        is_duplicate = False
        for existing_tool in category_obj.get("content", []):
            if existing_tool.get("title") == tool_to_add.get("title"):
                is_duplicate = True
                print(f"Skipping duplicate tool '{tool_to_add.get('title')}' in category '{category_name}'.")
                break

        if not is_duplicate:
            category_obj.setdefault("content", []).append(tool_to_add)

    # 4. Sort tools within each category's content list
    for cat_title in categories_dict:
        categories_dict[cat_title].get("content", []).sort(key=lambda x: x.get("title", "").lower())

    # 5. Convert the dictionary back to a list of category objects, sorted by category title
    updated_tools_list = sorted(list(categories_dict.values()), key=lambda x: x.get("title", "").lower())

    final_data_structure = {"tools": updated_tools_list}

    # 6. Write the updated data back to main_data_filepath
    with open(main_data_filepath, 'w') as f:
        json.dump(final_data_structure, f, indent=2)
    print(f"Successfully updated {main_data_filepath}")

if __name__ == '__main__':
    merge_tools_into_main_data('tool_entries_corrected.json', 'src/data/tools.json')
