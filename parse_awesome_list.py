import json
import re

def parse_markdown_to_json(md_file_path, json_file_path):
    """
    Parses a Markdown file to extract AI tool information and saves it as JSON.
    """
    tools = []
    current_category = "Unknown" # Default category

    # Regex to capture list items: * [Tool Name](URL) - Description
    # It handles variations in spacing and the presence/absence of the description.
    # It also tries to capture any text after "Description - " as part of description.
    # Example: * [Tool Name](URL) - Description - More description
    # Example: * [**Tool Name**](URL) - Description
    # Example: * [Tool Name](URL)
    tool_pattern = re.compile(r"^\s*[-*+]\s+\[([^\]]+?)\]\((https?://[^\)]+?)\)(?:\s*-\s*(.+))?")

    # Regex for headers to determine category
    # Catches ## Header or ### Header
    header_pattern = re.compile(r"^(##|###)\s+(.+)")

    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Check for category header
                header_match = header_pattern.match(line)
                if header_match:
                    # Use the header text as the category.
                    # For ### Subheader, we might want to combine with parent ##, but for now, just use the immediate header.
                    current_category = header_match.group(2).strip()
                    # Clean up category name if it contains links (e.g., from ToC)
                    current_category = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", current_category)
                    continue

                # Check for tool list item
                tool_match = tool_pattern.match(line)
                if tool_match:
                    name = tool_match.group(1).strip()
                    # If name is bolded (e.g., **Tool Name**), remove markdown
                    name = name.replace("**", "")

                    url = tool_match.group(2).strip()
                    description = tool_match.group(3).strip() if tool_match.group(3) else ""

                    # Further clean description if it contains " - *[reviews](...)*"
                    description = re.sub(r"\s*-\s*\*\s*\[reviews\].*$", "", description, flags=re.IGNORECASE).strip()
                    # Remove any leading/trailing hyphens or common junk if necessary
                    description = description.lstrip('- ').strip()


                    if name and url:
                        tools.append({
                            "name": name,
                            "url": url,
                            "description": description if description else None, # Store None if empty
                            "category": current_category
                        })
                    else:
                        print(f"Warning: Could not fully parse tool line: {line}")
                elif line.startswith("* [") or line.startswith("- ["): # Log lines that look like tools but didn't match
                    if not tool_pattern.match(line):
                        print(f"Warning: Potential tool line not parsed (or malformed): {line}")

    except FileNotFoundError:
        print(f"Error: Markdown file not found at {md_file_path}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(tools, f, indent=4)
        print(f"Successfully parsed {len(tools)} tools and saved to {json_file_path}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

if __name__ == "__main__":
    markdown_file = "awesome_ai_tools_readme.md"
    json_output_file = "awesome_ai_tools.json"
    parse_markdown_to_json(markdown_file, json_output_file)
