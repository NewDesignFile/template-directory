import json
import re
from datetime import date

# --- Functions from previous task (process_issues.py) ---
def fetch_issues():
    """Simulates fetching issues from a GitHub repository."""
    return [
        {
            "title": "AI Code Assistant",
            "body": "An AI-powered tool for code completion and suggestion. URL: http://example.com/ai-code-assistant. Category: Code",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "Image Editor",
            "body": "A simple image editor. URL: http://example.com/image-editor",
            "labels": []
        },
        {
            "title": "AI Text Summarizer",
            "body": "Summarizes long texts using AI. URL: http://example.com/ai-text-summarizer. Category: Text Generation",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "Task Management Tool",
            "body": "A tool for managing tasks and projects. URL: http://example.com/task-manager",
            "labels": []
        },
        {
            "title": "AI Chatbot Platform",
            "body": "Platform for building AI chatbots. URL: http://example.com/ai-chatbot-platform. Category: Chatbots",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "AI Code Assistant", # Duplicate
            "body": "An AI-powered tool for code completion and suggestion. URL: http://example.com/ai-code-assistant",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "AI Data Visualization Tool",
            "body": "Generates interactive data visualizations using AI. URL: http://example.com/ai-data-visualization. Category: Data Analysis",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "Video Editing Software",
            "body": "Software for professional video editing. URL: http://example.com/video-editor",
            "labels": []
        },
         {
            "title": "AI Language Translation Service",
            "body": "AI-powered translation for multiple languages. URL: http://example.com/ai-language-translation. Category: Language",
            "labels": [{"name": "AI"}]
        },
        {
            "title": "AI Writing Assistant",
            "body": "Helps improve writing style and grammar using AI. URL: http://example.com/ai-writing-assistant. Category: Writing",
            "labels": [{"name": "AI"}]
        }
    ]

def parse_issue(issue):
    """Parses issue title and body to extract tool information."""
    name = issue["title"]
    body = issue["body"]

    url_match = re.search(r"URL: (http[s]?://[^\s]+)", body)
    url = url_match.group(1).rstrip('.') if url_match else None

    category_match = re.search(r"Category: ([A-Za-z\s]+)", body)
    category = category_match.group(1).strip() if category_match else "General" # Default category

    return name, url, category, body

def is_ai_tool(issue_title, issue_body, issue_labels):
    """Checks if the tool is AI-related."""
    ai_keywords = ["ai", "artificial intelligence", "machine learning", "deep learning"]
    if any(keyword in issue_title.lower() for keyword in ai_keywords):
        return True
    if any(keyword in issue_body.lower() for keyword in ai_keywords):
        return True
    if any("AI" in label.get("name", "") for label in issue_labels): # check if label has "name"
        return True
    return False

def format_tool_name(name):
    """Formats the tool name."""
    if name.lower().startswith("ai "):
        name = name[3:]
    return name.strip()

def format_title(title):
    """Formats the title to be short and in title case (max 3 words)."""
    words = title.split()
    return " ".join(words[:3]).title()

def format_description(body_text):
    """Formats the body description text to be short and in sentence case (max 50 characters)."""
    # Try to get the first sentence related to the tool's function
    # This regex looks for a sentence ending with a period, question mark, or exclamation mark.
    match = re.match(r"([^.!?]*[.!?])", body_text)
    description = ""
    if match:
        description = match.group(1).strip()
    else: # If no sentence structure is found, take the beginning of the body
        description = body_text

    if len(description) > 50:
        description = description[:50]
        last_space = description.rfind(' ')
        if last_space != -1:
            description = description[:last_space]
        description += "..."
    elif not description and body_text: # Handle empty description if body_text was just a URL
        description = body_text[:50]
        if len(body_text) > 50:
            last_space = description.rfind(' ')
            if last_space != -1:
                description = description[:last_space]
            description += "..."


    description = re.sub(r'\b(ai)\b', 'AI', description, flags=re.IGNORECASE)
    if description:
        description = description[0].upper() + description[1:]
    else: # Default description if parsing failed
        description = "AI tool description."


    return description

def get_processed_ai_tools():
    """Processes issues to filter and format AI tools."""
    issues = fetch_issues()
    ai_tools_data = []
    added_urls = set()

    for issue in issues:
        if not is_ai_tool(issue["title"], issue["body"], issue.get("labels", [])):
            continue

        name, url, category, body_text = parse_issue(issue)

        if not url or url in added_urls:
            continue

        formatted_name = format_tool_name(name)
        # Use the formatted_name for the title directly, then format_title will apply case and word limit
        formatted_title_for_json = format_title(formatted_name)
        formatted_description = format_description(body_text)

        ai_tools_data.append({
            "name": formatted_name, # This is the original name, potentially longer
            "title_for_json": formatted_title_for_json, # This is the short, title-cased version for JSON
            "url": url,
            "category_from_issue": category, # Category from issue parsing
            "description_for_json": formatted_description # This is the short, sentence-cased version
        })
        added_urls.add(url)

        if len(ai_tools_data) >= 5:
            break

    return ai_tools_data
# --- End of functions from process_issues.py ---

def map_category_to_json_key(issue_category_name):
    """Maps the parsed category name to the json category key (lowercase)."""
    mapping = {
        "Text Generation": "copywriting",
        "Chatbots": "xtras", # Or a more specific category if available like "enterprise" or "productivity"
        "Data Analysis": "research", # Or "developer" if it's more tool-oriented
        "Language": "xtras", # Could be "translation", "copywriting" or "education"
        "Writing": "copywriting",
        "General": "xtras", # Default for "General" or unmapped
        "Code": "code" # For "AI Code Assistant"
    }
    # Normalize by lowercasing and removing spaces for a more robust key.
    normalized_input_category = issue_category_name.lower().replace(" ", "")

    # Attempt direct mapping first from the mapping dictionary
    if issue_category_name in mapping: # Check original case first
        return mapping[issue_category_name]

    # Check for normalized keys in mapping (e.g. if mapping had 'textgeneration':'copywriting')
    # This part is more conceptual as my current mapping keys are properly cased.
    # For a truly robust solution, mapping keys could also be stored normalized.

    # Fallback for some known patterns if direct map missed and specific normalization helps
    if "code" in normalized_input_category :
        return "code"
    if "text" in normalized_input_category or "writing" in normalized_input_category:
        return "copywriting"
    if "chat" in normalized_input_category or "bot" in normalized_input_category: # Added for Chatbots
        return "xtras" # Or specific category like "productivity" / "enterprise"
    if "data" in normalized_input_category or "analysis" in normalized_input_category:
        return "research"
    if "language" in normalized_input_category or "translation" in normalized_input_category:
        return "xtras"


    return mapping.get(issue_category_name, "xtras") # Default to "xtras" if no specific mapping found

def add_tools_to_json(tools_json_path, new_ai_tools):
    """Adds new AI tools to the JSON file under appropriate categories and sorts them."""
    try:
        with open(tools_json_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"tools": []} # Initialize if file doesn't exist or is empty/corrupt

    # Create a mapping from category `category` field (internal key) to the category object itself for easy lookup
    category_map = {cat_obj["category"]: cat_obj for cat_obj in data.get("tools", [])}

    today_date = "2025-06-01"

    for tool_data in new_ai_tools:
        new_tool_entry = {
            "title": tool_data["title_for_json"],
            "body": tool_data["description_for_json"],
            "tag": "Not available",
            "url": f"{tool_data['url']}?ref=riseofmachine.com",
            "date-added": today_date
        }

        # Determine the category for the new tool
        # The category from issue (e.g., "Text Generation") needs to be mapped to JSON category key (e.g., "copywriting")
        json_category_key = map_category_to_json_key(tool_data["category_from_issue"])

        target_category_obj = None
        if json_category_key in category_map:
            target_category_obj = category_map[json_category_key]
        else: # If category doesn't exist, try to find "Xtras" or create it if necessary
            if "xtras" in category_map:
                 target_category_obj = category_map["xtras"]
                 print(f"Category '{json_category_key}' not found. Adding tool '{new_tool_entry['title']}' to 'Xtras'.")
            else: # Create "Xtras" if it doesn't exist
                xtras_category_obj = {
                    "title": "Xtras", # Display title
                    "category": "xtras", # Internal key
                    "content": []
                }
                data.get("tools", []).append(xtras_category_obj)
                category_map["xtras"] = xtras_category_obj
                target_category_obj = xtras_category_obj
                print(f"Category '{json_category_key}' not found. 'Xtras' category also not found, created it. Adding tool '{new_tool_entry['title']}' to 'Xtras'.")

        # Add the new tool and sort the content list alphabetically by title
        target_category_obj["content"].append(new_tool_entry)
        target_category_obj["content"].sort(key=lambda x: x["title"].lower())

    # Write the updated JSON back
    with open(tools_json_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully updated {tools_json_path}")

if __name__ == "__main__":
    tools_file_path = "src/data/tools.json"

    # 1. Get the processed AI tools
    processed_tools = get_processed_ai_tools()

    # Print for verification before adding to JSON
    print("--- Processed AI Tools to be added: ---")
    for p_tool in processed_tools:
        print(p_tool)
    print("--------------------------------------")

    # 2. Add these tools to the JSON file
    add_tools_to_json(tools_file_path, processed_tools)

    # Optional: Verify by reading the file back (or part of it)
    # with open(tools_file_path, 'r') as f:
    #     updated_data = json.load(f)
    #     print("\n--- Sample of updated data from Xtras (if tools were added there): ---")
    #     for cat in updated_data.get("tools", []):
    #         if cat["category"] == "xtras":
    #             for item in cat["content"][-5:]: # print last 5 items from Xtras
    #                 print(item)
    #             break
