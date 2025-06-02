import json

def merge_tools_data(existing_tools_str, new_tools_str):
    """
    Merges new tools into the existing tools data structure under the 'Xtras' category.

    Args:
        existing_tools_str (str): JSON string of the existing tools data.
        new_tools_str (str): JSON string of the new tools to add.

    Returns:
        str: Pretty-printed JSON string of the updated tools data.
             Returns None if parsing fails.
    """
    try:
        existing_data = json.loads(existing_tools_str)
        new_tools_list = json.loads(new_tools_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

    # Ensure the top-level structure is as expected (a dict with a "tools" key)
    if not isinstance(existing_data, dict) or "tools" not in existing_data:
        print("Error: Existing tools data is not in the expected format (dict with 'tools' key).")
        # If existing_data is completely empty or malformed, we might initialize it.
        # For this task, assuming it has the base structure if it exists.
        # If it were permissible to create from scratch: existing_data = {"tools": []}
        return None

    if not isinstance(existing_data["tools"], list):
        print("Error: existing_data['tools'] is not a list.")
        return None


    xtras_category = None
    for category in existing_data["tools"]:
        if isinstance(category, dict) and category.get("category") == "xtras":
            xtras_category = category
            break

    if xtras_category is None:
        xtras_category = {"title": "Xtras", "category": "xtras", "content": []}
        existing_data["tools"].append(xtras_category)
        print("Created 'Xtras' category.")

    # Ensure 'content' list exists in xtras_category
    if "content" not in xtras_category or not isinstance(xtras_category.get("content"), list):
        xtras_category["content"] = []
        print("Warning: 'Xtras' category was missing 'content' list or it was malformed. Initialized.")


    # Add new tools to the 'Xtras' category's content
    # Avoid adding duplicates based on URL (or title, if URL isn't always unique identifier for *entry*)
    # For this task, the prompt doesn't specify duplicate handling at this stage,
    # but it's good practice. Assuming new_tools_list are all desired.
    if isinstance(new_tools_list, list):
        xtras_category["content"].extend(new_tools_list)
    else:
        print("Warning: New tools data is not a list. No tools added.")

    # Sort the 'content' list of the "Xtras" category alphabetically by title
    # Ensure all items in content are dicts and have a 'title'
    xtras_category["content"].sort(key=lambda x: x.get("title", "").lower() if isinstance(x, dict) else "")

    return json.dumps(existing_data, indent=2)

if __name__ == "__main__":
    try:
        with open("src/data/tools.json", 'r', encoding='utf-8') as f:
            existing_tools_content = f.read()
    except FileNotFoundError:
        print("Error: src/data/tools.json not found.")
        # Create a default structure if the main file is missing
        existing_tools_content = json.dumps({"tools": []}, indent=2)
        print("Initialized with default empty tools structure.")
    except Exception as e:
        print(f"Error reading src/data/tools.json: {e}")
        existing_tools_content = json.dumps({"tools": []}, indent=2) # fallback
        print("Initialized with default empty tools structure due to read error.")


    try:
        with open("formatted_tools.json", 'r', encoding='utf-8') as f:
            new_tools_content = f.read()
    except FileNotFoundError:
        print("Error: formatted_tools.json not found. No new tools to add.")
        new_tools_content = "[]" # Empty list if no new tools
    except Exception as e:
        print(f"Error reading formatted_tools.json: {e}")
        new_tools_content = "[]" # Fallback

    updated_json_str = merge_tools_data(existing_tools_content, new_tools_content)

    if updated_json_str:
        try:
            with open("updated_tools.json", 'w', encoding='utf-8') as f:
                f.write(updated_json_str)
            print("Successfully updated tools data and wrote to updated_tools.json")
        except IOError as e:
            print(f"Error writing updated_tools.json: {e}")
    else:
        print("Failed to merge tools data.")
