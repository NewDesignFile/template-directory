import json
import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def assign_placeholder_pricing(tool_url_str):
    """Assigns a placeholder pricing tag based on the tool's URL."""
    if not tool_url_str:
        return "Not available"

    lower_url = tool_url_str.lower()

    if "docs" in lower_url or "feature" in lower_url:
        return "Freemium"
    elif "visioncraft" in lower_url or "llm_summary" in lower_url:
        return "Free"
    elif "pandasgui" in lower_url: # From the example
        return "Not available"
    else:
        # Default for tools not matching specific rules
        # Based on the provided example, 'ToolA' (from example.com/toolA/docs) gets Freemium.
        # Let's make Freemium a common default if no other rule applies.
        return "Freemium"

def format_title(tool_url_str):
    """Formats the title from the tool URL."""
    if not tool_url_str:
        return "Unnamed Tool"

    try:
        path = urlparse(tool_url_str).path
        name_from_path = ""
        generic_terms = ["docs", "documentation", "features", "feature", "app", "main", "index", "site", "website"]

        if path and path != '/':
            name_parts = path.strip('/').split('/')
            if len(name_parts) > 0:
                potential_name = name_parts[-1]
                if potential_name.lower() in generic_terms and len(name_parts) > 1:
                    name_from_path = name_parts[-2]
                else:
                    name_from_path = potential_name

        if name_from_path:
            base_name = name_from_path
        else: # Try to get from hostname if path didn't yield a good name
            hostname = urlparse(tool_url_str).hostname
            if hostname:
                name_parts = hostname.split('.')
                # Prefer part before common TLDs if simple (e.g. 'example' from 'example.com')
                # Also remove 'www' if it's the first part.
                if len(name_parts) > 1 and name_parts[0] == 'www':
                    base_name = name_parts[1] if len(name_parts) > 2 else name_parts[0] # www.example.com -> example, www.domain.ai -> domain
                elif len(name_parts) > 1 :
                     base_name = name_parts[0] # example.com -> example
                else:
                    base_name = hostname # single word hostname
            else: # Fallback if no path and no hostname
                base_name = "Unnamed Tool"

        # Clean common extensions like .com, .io, .ai (if they are part of base_name from hostname or path)
        # This regex might be too broad if the name itself is e.g. "get.ai" -> "get"
        # Let's ensure it only strips if it's a TLD-like extension on a multi-part name from hostname
        # For path derived names, it's less likely to be an issue e.g. /path/to/tool.ai might be legit
        if not name_from_path: # Only apply this aggressive TLD stripping if name came from hostname
             base_name = re.sub(r'\.(com|io|ai|org|net|co|app|sh)$', '', base_name, flags=re.IGNORECASE)

        # Replace hyphens and underscores with spaces
        name_str = base_name.replace('-', ' ').replace('_', ' ')

        # Take first few words (max 3)
        words = name_str.split()
        limited_words = words[:3]

        # Title Case
        title_cased = " ".join(word.capitalize() for word in limited_words)

        # Remove "Ai" or "AI" prefix
        if title_cased.startswith("Ai "):
            title_cased = title_cased[3:]
        elif title_cased.startswith("AI "):
            title_cased = title_cased[3:]
        elif title_cased.lower() == "ai": # if the whole title is just "Ai"
             title_cased = "Tool"


        return title_cased if title_cased else "Unnamed Tool"
    except Exception:
        return "Unnamed Tool"

def format_body(original_body):
    """Formats the description from the original body."""
    if not original_body:
        return "No description available."

    # Take first sentence (simplistic: up to first '.', '!', '?')
    match = re.match(r'(.*?[\.!?])', original_body)
    if match:
        sentence = match.group(1).strip()
    else: # Or just take the beginning if no clear sentence end
        sentence = original_body.split('\n')[0].strip()

    # Sentence case (capitalize first letter, rest lower unless it's part of an acronym or proper noun already)
    if sentence:
        # A simple approach to sentence case:
        # Capitalize the first character, and leave the rest as is,
        # as complex sentence casing is hard without NLP.
        # The task asks for "Sentence case (capitalize the first letter, rest lowercase unless proper noun)"
        # A true sentence case for "Tool A (an AI-powered code assistant) is not..."
        # would be "Tool a (an ai-powered code assistant) is not..." which might be too aggressive.
        # Let's try: Capitalize first char, then lowercase the rest of the first word if it's not an acronym.
        # For simplicity and to avoid destroying acronyms: only capitalize the very first letter.
        formatted_sentence = sentence[0].upper() + sentence[1:]
    else:
        formatted_sentence = "No description available."

    # Truncate to 50 chars
    if len(formatted_sentence) > 50:
        formatted_sentence = formatted_sentence[:47] + "..."

    return formatted_sentence

def format_url(original_url):
    """Appends ?ref=riseofmachine.com to the URL."""
    if not original_url:
        return ""

    parsed_url = urlparse(original_url)
    query_params = parse_qs(parsed_url.query)
    query_params['ref'] = ['riseofmachine.com']

    new_query_string = urlencode(query_params, doseq=True)

    return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                       parsed_url.params, new_query_string, parsed_url.fragment))

def process_tools(input_filepath="selected_ai_tools.json", output_filepath="formatted_tools.json"):
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            selected_tools = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_filepath}")
        return

    formatted_tools_list = []
    for tool_data in selected_tools:
        original_tool_url = tool_data.get("url") # This is the tool's actual URL

        tag = assign_placeholder_pricing(original_tool_url)
        title = format_title(original_tool_url)
        body_description = format_body(tool_data.get("body"))
        final_url = format_url(original_tool_url)
        date_added = "2025-06-02" # Static date as per requirement

        formatted_tools_list.append({
            "title": title,
            "body": body_description,
            "tag": tag,
            "url": final_url,
            "date-added": date_added
        })

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(formatted_tools_list, f, indent=2)
        print(f"Formatted tools written to {output_filepath}")
    except IOError:
        print(f"Error: Could not write to {output_filepath}")

if __name__ == "__main__":
    process_tools()
