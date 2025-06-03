import json
import bisect

def get_category_id(category_name, existing_categories_data):
    """Maps a human-readable category name to its ID, or returns 'xtras' if not found."""
    name_lower = category_name.lower()
    if name_lower == "llms":
        return "llm"
    if name_lower == "copywriting":
        return "copywriting"
    if name_lower == "video":
        return "video"

    for cat_obj in existing_categories_data:
        if cat_obj.get("title", "").lower() == name_lower:
            return cat_obj.get("category")
        if cat_obj.get("category", "").lower() == name_lower:
            return name_lower

    print(f"Category name '{category_name}' not directly mapped or found in existing categories by title/id, defaulting to 'xtras'.")
    return "xtras"


def main():
    try:
        with open('src/data/tools.json', 'r') as f:
            existing_tools_data = json.load(f)
    except FileNotFoundError:
        print("Error: src/data/tools.json not found. Initializing with basic structure.")
        existing_tools_data = {"tools": []}
    except json.JSONDecodeError:
        print("Error: Could not decode src/data/tools.json. Initializing with basic structure.")
        existing_tools_data = {"tools": []}

    new_tools_from_prepared = [
        {
            "title": "Aicode", "body": "Aicode", "tag": "Not available",
            "url": "https://aicode.help?ref=riseofmachine.com", "date-added": "2025-06-03",
            "category_name": "LLMs"
        },
        {
            "title": "Offlinechat", "body": "Offlinechat", "tag": "Not available",
            "url": "https://offlinechat.chat?ref=riseofmachine.com", "date-added": "2025-06-03",
            "category_name": "LLMs"
        },
        {
            "title": "Papergen", "body": "Papergen", "tag": "Not available",
            "url": "https://www.papergen.i/?ref=riseofmachine.com", "date-added": "2025-06-03",
            "category_name": "Copywriting"
        },
        {
            "title": "Omnigen", "body": "Omnigen", "tag": "Not available",
            "url": "https://omnigen.co/?ref=riseofmachine.com", "date-added": "2025-06-03",
            "category_name": "Avatars"
        },
        {
            "title": "Summarize", "body": "Summarize.tech: ai-powered video summaries", "tag": "Not available",
            "url": "https://www.summarize.tech/?ref=riseofmachine.com", "date-added": "2025-06-03",
            "category_name": "Video"
        }
    ]

    if 'tools' not in existing_tools_data or not isinstance(existing_tools_data['tools'], list):
        print("Warning: 'tools' array not found or invalid in src/data/tools.json. Initializing.")
        existing_tools_data['tools'] = []

    xtras_category_id = "xtras"
    xtras_category_obj = next((cat for cat in existing_tools_data['tools'] if cat.get('category') == xtras_category_id), None)
    if not xtras_category_obj:
        print(f"Warning: '{xtras_category_id}' category not found. Creating it.")
        xtras_category_obj = {"title": "Xtras", "category": xtras_category_id, "content": []}
        existing_tools_data['tools'].append(xtras_category_obj)

    for new_tool_data in new_tools_from_prepared:
        tool_entry = {
            "title": new_tool_data["title"],
            "body": new_tool_data["body"],
            "tag": new_tool_data["tag"],
            "url": new_tool_data["url"],
            "date-added": new_tool_data["date-added"]
        }

        original_category_name = new_tool_data["category_name"]
        target_category_id = get_category_id(original_category_name, existing_tools_data['tools'])

        target_category_object_for_tool = None

        for category_obj_iter in existing_tools_data['tools']:
            if category_obj_iter.get('category') == target_category_id:
                target_category_object_for_tool = category_obj_iter
                break

        if not target_category_object_for_tool and target_category_id == xtras_category_id:
            target_category_object_for_tool = xtras_category_obj
        elif not target_category_object_for_tool: # Should only happen if target_category_id was not 'xtras' but still not found
            print(f"Warning: Could not find category object for ID '{target_category_id}' (from original name '{original_category_name}'). Using 'Xtras'.")
            target_category_object_for_tool = xtras_category_obj


        if 'content' not in target_category_object_for_tool or not isinstance(target_category_object_for_tool.get('content'), list):
            target_category_object_for_tool['content'] = []

        titles_in_category = [item.get('title', '').lower() for item in target_category_object_for_tool['content']]
        insert_pos = bisect.bisect_left(titles_in_category, tool_entry['title'].lower())
        target_category_object_for_tool['content'].insert(insert_pos, tool_entry)

        print(f"Added '{tool_entry['title']}' to category '{target_category_object_for_tool.get('title', target_category_id)}'.")

    try:
        with open('src/data/tools.json', 'w') as f:
            json.dump(existing_tools_data, f, indent=2)
        print("Successfully updated src/data/tools.json")
    except IOError:
        print("Error: Could not write to src/data/tools.json.")

if __name__ == '__main__':
    main()
