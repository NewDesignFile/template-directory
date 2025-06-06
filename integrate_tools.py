import json
from collections import OrderedDict

def get_category_display_title(internal_name, current_categories_list):
    """Helper to find display title for a category, or create one if new."""
    for cat_obj in current_categories_list:
        if cat_obj.get('category') == internal_name:
            return cat_obj.get('title', internal_name.capitalize())
    # If new category (e.g. 'xtras' might be new)
    if internal_name == 'xtras':
        return 'Xtras'
    return internal_name.capitalize() # Default display title

def main():
    try:
        with open("src/data/tools.json", 'r', encoding='utf-8') as f:
            current_data = json.load(f)
    except FileNotFoundError:
        print("Error: src/data/tools.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from src/data/tools.json.")
        return

    try:
        with open("filtered_formatted_tools.json", 'r', encoding='utf-8') as f:
            new_tools_list = json.load(f)
    except FileNotFoundError:
        print("Error: filtered_formatted_tools.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from filtered_formatted_tools.json.")
        return

    # Create a dictionary for easy access and modification of categories
    # Use OrderedDict to preserve original category order for a while, though final sort is by title
    categories_dict = OrderedDict()
    if 'tools' in current_data and isinstance(current_data['tools'], list):
        for category_obj in current_data['tools']:
            if 'category' in category_obj and 'content' in category_obj:
                categories_dict[category_obj['category']] = category_obj
            else:
                print(f"Warning: Found a category object without 'category' or 'content' field: {category_obj.get('title')}")
    else:
        print("Warning: 'tools' key not found in current_data or is not a list. Starting with empty categories.")


    for tool in new_tools_list:
        tool_category_internal_name = tool.get('category')

        if not tool_category_internal_name:
            print(f"Warning: Tool '{tool.get('title')}' has no category, assigning to 'xtras'.")
            tool_category_internal_name = 'xtras'
            tool['category'] = 'xtras' # Ensure the tool itself has this category set

        # If category doesn't exist, create it, especially for 'xtras'
        if tool_category_internal_name not in categories_dict:
            display_title = get_category_display_title(tool_category_internal_name, current_data.get('tools', []))
            categories_dict[tool_category_internal_name] = {
                "title": display_title,
                "category": tool_category_internal_name,
                "content": []
            }
            print(f"Info: Created new category '{tool_category_internal_name}' with display title '{display_title}'.")
        elif 'content' not in categories_dict[tool_category_internal_name] or not isinstance(categories_dict[tool_category_internal_name]['content'], list) :
            print(f"Warning: Category '{tool_category_internal_name}' exists but 'content' is missing or not a list. Re-initializing content.")
            categories_dict[tool_category_internal_name]['content'] = []


        # Ensure the tool has all required fields for consistency, even if some are from the old format
        # The new tools are already in the desired format: title, body, url, category, date-added, tag
        categories_dict[tool_category_internal_name]['content'].append(tool)

    # Sort content within each category by title
    for category_internal_name in categories_dict:
        # Guard against cases where content might still not be a list (though previous checks should handle it)
        if isinstance(categories_dict[category_internal_name].get('content'), list):
            categories_dict[category_internal_name]['content'].sort(key=lambda x: x.get('title', '').lower())
        else:
            print(f"Warning: Content for category '{category_internal_name}' is not a list during sorting. Skipping sort for this category.")


    # Reconstruct the final list of category objects and sort them by display title
    final_categories_list = list(categories_dict.values())
    final_categories_list.sort(key=lambda x: x.get('title', '').lower())

    final_data_structure = {"tools": final_categories_list}

    try:
        with open("updated_tools_payload.json", 'w', encoding='utf-8') as f:
            json.dump(final_data_structure, f, indent=2)
    except IOError:
        print("Error: Could not write to updated_tools_payload.json.")
        return

    total_categories = len(final_categories_list)
    total_tools = sum(len(cat.get('content', [])) for cat in final_categories_list)

    print(f"Total number of categories in the updated data: {total_categories}")
    print(f"Total number of tools across all categories: {total_tools}")

if __name__ == "__main__":
    main()
