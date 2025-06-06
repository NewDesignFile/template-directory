import json
from collections import defaultdict
from titlecase import titlecase # For consistent title casing

def load_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File not found {filepath}. Returning default structure.")
        if "tools.json" in filepath:
            return {"tools": []} # Default structure for the main tools file
        return [] # Default for lists of tools
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {filepath}. Returning default structure.")
        if "tools.json" in filepath:
            return {"tools": []}
        return []

def save_json_file(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")

def format_category_title(category_str):
    # Capitalize the first letter of each word
    return titlecase(str(category_str))

def main():
    processed_tools_file = "all_new_tools_processed.json"
    main_tools_file = "src/data/tools.json"

    # 1. Read processed tools
    new_tools_list = load_json_file(processed_tools_file)
    if not new_tools_list:
        print(f"No tools found in {processed_tools_file}. Exiting.")
        # Ensure src/data/tools.json is at least an empty valid structure if it doesn't exist
        existing_data_structure = load_json_file(main_tools_file)
        if not existing_data_structure or "tools" not in existing_data_structure:
            save_json_file({"tools": []}, main_tools_file)
        return

    # 2. Read existing tools.json (currently '[]', but script should handle structure)
    # The load_json_file function will return {"tools": []} if it's empty or not found.
    # For this specific task, we are overwriting, so we don't merge with existing_tools.
    # If merging was needed, we'd load existing_tools_data here.

    # 3. Group processed tools by original_category
    grouped_by_category = defaultdict(list)
    for tool in new_tools_list:
        # Ensure essential fields are present
        if not all(k in tool for k in ['title', 'body', 'url', 'tag', 'date-added', 'original_category']):
            print(f"Warning: Tool missing essential fields, skipping: {tool.get('title', 'N/A')}")
            continue

        category_key = tool['original_category'].strip()
        if not category_key: # Handle empty category strings
            category_key = 'xtras'

        # Prepare tool entry for the "content" list, removing 'original_category'
        tool_entry = {
            "title": tool["title"],
            "body": tool["body"],
            "tag": tool["tag"],
            "url": tool["url"],
            "date-added": tool["date-added"]
        }
        grouped_by_category[category_key].append(tool_entry)

    # 4. Construct final JSON structure
    final_data_structure = {"tools": []}

    # 5. Create category objects
    for original_cat_lowercase, tools_in_cat in grouped_by_category.items():
        # a. Create formatted category title
        formatted_title = format_category_title(original_cat_lowercase)

        # c. Sort tools alphabetically by title
        sorted_tools = sorted(tools_in_cat, key=lambda x: x['title'].lower())

        # d. Create category object
        category_object = {
            "title": formatted_title,
            "category": original_cat_lowercase, # Already lowercase
            "content": sorted_tools
        }
        # e. Add to main list
        final_data_structure["tools"].append(category_object)

    # 6. Sort category objects alphabetically by their title
    final_data_structure["tools"] = sorted(final_data_structure["tools"], key=lambda x: x['title'].lower())

    # 7. Overwrite src/data/tools.json
    save_json_file(final_data_structure, main_tools_file)
    print(f"Total categories created: {len(final_data_structure['tools'])}")
    total_tools_in_final_json = sum(len(cat['content']) for cat in final_data_structure['tools'])
    print(f"Total tools in final structure: {total_tools_in_final_json}")

if __name__ == "__main__":
    main()
