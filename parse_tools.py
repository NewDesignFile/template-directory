import json

def parse_tools_json(json_filepath, output_filepath):
    """
    Parses a JSON file containing tools, extracts unique (title, url) pairs,
    prints the total count, and saves them to a text file.

    Args:
        json_filepath (str): The path to the input JSON file.
        output_filepath (str): The path to the output text file.
    """
    unique_tools = set()

    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_filepath}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_filepath}")
        return

    if 'tools' not in data or not isinstance(data['tools'], list):
        print(f"Error: JSON file does not have the expected structure (missing 'tools' list).")
        return

    for category in data['tools']:
        if 'content' in category and isinstance(category['content'], list):
            for tool in category['content']:
                if isinstance(tool, dict) and 'title' in tool and 'url' in tool:
                    title = tool.get('title')
                    url = tool.get('url')
                    if title and url: # Ensure both title and url are not None or empty
                        unique_tools.add((str(title), str(url)))
                # else:
                #     print(f"Warning: Skipping tool due to missing 'title' or 'url', or incorrect format: {tool}")
        # else:
        #     print(f"Warning: Skipping category due to missing 'content' or incorrect format: {category.get('title', 'Unknown Category')}")


    print(f"Total number of unique tools found: {len(unique_tools)}")

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            for title, url in sorted(list(unique_tools)): # Sort for consistent output
                f.write(f"{title}\t{url}\n")
        print(f"Successfully saved unique tools to {output_filepath}")
    except IOError:
        print(f"Error: Could not write to output file {output_filepath}")

if __name__ == "__main__":
    json_file = "src/data/tools.json"
    output_file = "existing_tools.txt"
    parse_tools_json(json_file, output_file)
