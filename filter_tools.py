import json
import re
import os

# AI Keywords for checking website content
AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "neural network", "llm", "nlp", "natural language processing",
    "computer vision", "generative ai", "a.i."
]

# New tools to process - provided in the subtask
new_tools_data = [
    {"name": "aicode.help", "url": "https://aicode.help", "category": "LLMs"},
    {"name": "offlinechat.chat", "url": "https://offlinechat.chat", "category": "LLMs"},
    {"name": "papergen.i", "url": "https://www.papergen.i/", "category": "Copywriting"},
    {"name": "omnigen.co", "url": "https://omnigen.co/", "category": "Xtras"},
    {"name": "usesaaskit.com", "url": "https://www.usesaaskit.com/", "category": "Developer"}
]

# Path to the existing tools JSON file
EXISTING_TOOLS_FILE = "src/data/tools.json"

def load_existing_tools(filepath):
    """Loads existing tools from the JSON file."""
    existing_tools_details = {"names": set(), "urls": set()}
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict) and "tools" in data: # New structure
                for category_group in data["tools"]:
                    if "content" in category_group and isinstance(category_group["content"], list):
                        for tool in category_group["content"]:
                            if isinstance(tool, dict):
                                if "title" in tool:
                                    existing_tools_details["names"].add(tool["title"].lower())
                                if "url" in tool:
                                    # Normalize URL for comparison: remove query params, www, trailing slash
                                    url = tool["url"].lower()
                                    url = re.sub(r"https://?www\.", "https://", url) # normalize www
                                    url = url.split('?')[0].rstrip('/')
                                    existing_tools_details["urls"].add(url)
            elif isinstance(data, list): # Old structure (list of tools)
                 for tool in data:
                    if isinstance(tool, dict):
                        if "name" in tool: # Assuming 'name' key for older structure
                            existing_tools_details["names"].add(tool["name"].lower())
                        if "url" in tool:
                            url = tool["url"].lower()
                            url = re.sub(r"https://?www\.", "https://", url)
                            url = url.split('?')[0].rstrip('/')
                            existing_tools_details["urls"].add(url)
    except FileNotFoundError:
        print(f"Info: {filepath} not found. Assuming no existing tools.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}. Assuming no existing tools.")
    return existing_tools_details

def is_duplicate(tool, existing_tools_details):
    """Checks if a tool is a duplicate by name or URL."""
    name_lower = tool["name"].lower()
    # Normalize URL for comparison
    url_lower = tool["url"].lower()
    url_lower = re.sub(r"https://?www\.", "https://", url_lower) # normalize www
    url_lower = url_lower.split('?')[0].rstrip('/')

    if name_lower in existing_tools_details["names"]:
        print(f"Duplicate found for name: {tool['name']}")
        return True
    if url_lower in existing_tools_details["urls"]:
        print(f"Duplicate found for URL: {tool['url']} (normalized: {url_lower})")
        return True
    return False

def is_ai_tool(tool_name, site_content):
    """Checks if the site content indicates an AI tool."""
    if not site_content:
        print(f"No content fetched for {tool_name}, cannot determine AI status by keywords.")
        return False # Cannot determine, assume not AI if content is missing

    content_lower = site_content.lower()
    for keyword in AI_KEYWORDS:
        if keyword.lower() in content_lower:
            print(f"AI keyword '{keyword}' found for {tool_name}.")
            return True
    print(f"No AI keywords found for {tool_name}.")
    return False

def main():
    # This argument will be passed by the bash script calling this python script
    # It will contain the website content for ONE tool at a time, or "SKIP"
    tool_url_to_check = os.environ.get("TOOL_URL_TO_CHECK")
    website_content_for_tool = os.environ.get("WEBSITE_CONTENT", "")

    existing_tools = load_existing_tools(EXISTING_TOOLS_FILE)

    # Print existing tool names and URLs for debugging
    # print("Existing tool names:", existing_tools["names"])
    # print("Existing tool URLs:", existing_tools["urls"])

    final_tools_list = []
    processed_tool_this_run = False

    for new_tool in new_tools_data:
        print(f"\nProcessing: {new_tool['name']} ({new_tool['url']})")

        if is_duplicate(new_tool, existing_tools):
            print(f"Skipping {new_tool['name']} as it is a duplicate.")
            continue

        # If this is the tool we are actively checking with web content
        if tool_url_to_check == new_tool["url"]:
            processed_tool_this_run = True
            if website_content_for_tool == "ERROR_FETCHING_CONTENT":
                print(f"Skipping AI check for {new_tool['name']} due to fetch error.")
                ai_related = False # Assume not AI if fetch failed
            elif not website_content_for_tool:
                 print(f"No website content provided for {new_tool['name']}. Assuming not AI-related for safety.")
                 ai_related = False
            else:
                ai_related = is_ai_tool(new_tool['name'], website_content_for_tool)

            if ai_related:
                print(f"{new_tool['name']} is AI-related and not a duplicate. Adding to list.")
                final_tools_list.append(new_tool)
            else:
                print(f"{new_tool['name']} is not AI-related or AI status unknown.")

        # For tools not actively checked in THIS run, we'd typically skip them or use a placeholder.
        # For this subtask, if a tool is not the one being actively checked,
        # we'll just print a message indicating it would be checked in a separate run.
        elif not tool_url_to_check: # First run, before any web fetching
            print(f"AI check for {new_tool['name']} will be performed in a subsequent step.")
        elif tool_url_to_check and tool_url_to_check != new_tool["url"] and not processed_tool_this_run :
             # This case handles subsequent tools in the list when one was already designated for web check
             print(f"AI check for {new_tool['name']} will be performed in a subsequent step.")


    if not tool_url_to_check:
        print("\n--- Script Initial Run ---")
        print("This script needs to be run multiple times, once for each tool's website to be checked.")
        print("For the next run, set TOOL_URL_TO_CHECK to the URL of the first tool you want to analyze.")
        print("Example: TOOL_URL_TO_CHECK='https://aicode.help'")
    elif not processed_tool_this_run and tool_url_to_check:
        print(f"\nWarning: The specified TOOL_URL_TO_CHECK ('{tool_url_to_check}') was not found in the new tools list or was a duplicate.")

    if final_tools_list:
        print("\n--- Filtered AI Tools (from this run) ---")
        for tool in final_tools_list:
            print(f"- Name: {tool['name']}, URL: {tool['url']}, Category: {tool['category']}")
    elif processed_tool_this_run:
        print(f"\nNo new AI tools were added to the list from the check of {tool_url_to_check}.")

    # Store intermediate results
    # If running for a specific tool, append to a temp file or manage state
    # For now, we print, and the agent will collect results across runs.

if __name__ == "__main__":
    main()
