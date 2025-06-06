import json
import re

def extract_producthunt_info(html_file_path):
    """
    Extracts tool information from a Product Hunt text dump file.

    Args:
        html_file_path (str): The path to the HTML file (text dump).

    Returns:
        list: A list of dictionaries, where each dictionary contains information about a tool.
    """
    tools_data = []
    link_map = {}

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Phase 1: Parse the "Visible links" section to create a map of ID to URL
        parsing_visible_links = False
        for line in lines:
            line = line.strip()
            if line.startswith("Visible links:"):
                parsing_visible_links = True
                continue
            if line.startswith("Hidden links:") or line.startswith("File links:"):
                parsing_visible_links = False
                continue

            if parsing_visible_links:
                match = re.match(r"(\d+)\.\s(https?://.+)", line)
                if match:
                    link_id, url = match.groups()
                    link_map[link_id] = url

        # Phase 2: Parse the product information
        current_tool = None
        for i, line in enumerate(lines):
            line = line.strip()

            # Check for product rank marker (e.g., #1, #2)
            rank_match = re.match(r"^#(\d+)", line)
            if rank_match:
                if current_tool and current_tool.get('name') and current_tool.get('url'): # Save previous tool if valid
                    tools_data.append(current_tool)
                current_tool = {"category": ["Artificial Intelligence"], "pricing": None} # Initialize new tool

                # Look for the first link after the rank marker - this is usually the short name
                # Example: #1\n[34]Figma
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    name_link_match = re.match(r"\[(\d+)\](.+)", next_line)
                    if name_link_match:
                        link_id, name_text = name_link_match.groups()
                        name = name_text.strip()
                        if '—' in name: # Sometimes the first link also has the tagline
                             current_tool['name'] = name.split('—')[0].strip()
                             current_tool['description'] = name.split('—', 1)[1].strip()
                        else:
                            current_tool['name'] = name

                        if link_id in link_map:
                            product_url = link_map[link_id]
                            # Ensure it's a product URL, not a post URL etc.
                            if "/products/" in product_url:
                                current_tool['url'] = product_url.replace("/shoutouts", "")
                            elif "/posts/" in product_url and not current_tool.get('url'): # Fallback if it's a post link
                                current_tool['url'] = product_url


                # Look for the second link, which often contains "Name — Tagline"
                # Example: [35]Figma — The collaborative interface design tool
                if i + 2 < len(lines): # Check one more line for the tagline/description
                    second_line = lines[i+2].strip()
                    tagline_link_match = re.match(r"\[(\d+)\](.+)", second_line)
                    if tagline_link_match:
                        link_id, text = tagline_link_match.groups()
                        text = text.strip()
                        if '—' in text:
                            name_part = text.split('—')[0].strip()
                            desc_part = text.split('—', 1)[1].strip()
                            if not current_tool.get('name') or len(name_part) < len(current_tool.get('name', '')):
                                current_tool['name'] = name_part
                            if not current_tool.get('description'):
                                current_tool['description'] = desc_part

                            if not current_tool.get('url') and link_id in link_map:
                                product_url = link_map[link_id]
                                if "/products/" in product_url:
                                     current_tool['url'] = product_url.replace("/shoutouts", "")

                        # Check for description on the same line or next line if it starts with a link ID
                        # Example: ...tool[36]A collaborative design tool...
                        description_marker_match = re.search(r"\[(\d+)\](.+)", text)
                        if description_marker_match:
                            desc_text_after_marker = description_marker_match.group(2).strip()
                            if desc_text_after_marker and (not current_tool.get('description') or len(desc_text_after_marker) > len(current_tool.get('description',''))):
                                current_tool['description'] = desc_text_after_marker
                        elif not current_tool.get('description') and text and '—' not in text and 'Shoutouts:' not in text and not text.startswith("http"):
                            current_tool['description'] = text


            # Capture description if it's on the line following the tagline/name
            # Example: design tool[36]A collaborative... (description starts after [36])
            # Or it could be just plain text on the next line
            elif current_tool and not current_tool.get('description') and 'Shoutouts:' not in line and not line.startswith("http") and not re.match(r"\[\d+\]", line) and len(line) > 20:
                 # This is a heuristic for plain text descriptions
                 if i > 0 and not lines[i-1].strip().startswith("#"): # ensure not part of a new product block by mistake
                    current_tool['description'] = line.strip()

            elif current_tool and current_tool.get('name') and 'Shoutouts:' in line: # Stop processing for this tool if shoutouts start
                if current_tool.get('url'): # Only add if we have a URL
                    tools_data.append(current_tool)
                current_tool = None


        # Add the last processed tool if it's valid
        if current_tool and current_tool.get('name') and current_tool.get('url') and current_tool not in tools_data:
            tools_data.append(current_tool)

        # Post-processing: Remove entries that might be malformed (e.g. missing URL or essential fields)
        valid_tools_data = [tool for tool in tools_data if tool.get('name') and tool.get('url')]
        # Deduplicate based on URL, preferring entries with more information
        deduped_tools = {}
        for tool in valid_tools_data:
            url = tool['url']
            if url not in deduped_tools or len(str(tool.get('description',''))) > len(str(deduped_tools[url].get('description',''))):
                deduped_tools[url] = tool
        tools_data = list(deduped_tools.values())


    except FileNotFoundError:
        print(f"Error: HTML file not found at {html_file_path}")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")

    return tools_data

def save_to_json(data, json_file_path):
    """
    Saves data to a JSON file.

    Args:
        data (list): The data to save.
        json_file_path (str): The path to the JSON file.
    """
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {json_file_path}")
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")

if __name__ == "__main__":
    html_file = 'producthunt.html'
    json_file = 'producthunt_tools.json'

    extracted_tools = extract_producthunt_info(html_file)
    if extracted_tools:
        save_to_json(extracted_tools, json_file)
    else:
        print("No tools extracted or an error occurred.")
        # Create an empty JSON file if nothing was extracted
        save_to_json([], json_file)
