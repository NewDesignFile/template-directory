import json
import re
from titlecase import titlecase # For better title casing

def sentence_case(text):
    if not text:
        return ""
    # Capitalize the first letter of the first word, lowercasing the rest of that word,
    # and then lowercasing the rest of the sentence.
    # This is a simplified sentence case.
    words = text.split()
    if not words:
        return ""
    first_word = words[0]
    rest_of_sentence = ' '.join(words[1:])

    # A more robust sentence casing would involve NLP sentence tokenization.
    # For now, capitalize the first letter of the string and lowercase the rest.
    if len(text) > 1:
        return text[0].upper() + text[1:].lower()
    elif len(text) == 1:
        return text[0].upper()
    return ""


def load_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File not found {filepath}. Returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {filepath}. Returning empty list.")
        return []

def save_json_file(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")

def process_title(title_str):
    if not title_str:
        return ""

    # Convert to title case using the 'titlecase' library
    processed_title = titlecase(title_str)

    # If it starts with 'AI ' (case-insensitive), remove 'AI '
    if processed_title.lower().startswith('ai '):
        processed_title = processed_title[3:]

    # Attempt to shorten to max 3 words
    words = processed_title.split()
    if len(words) > 3:
        processed_title = ' '.join(words[:3])

    return processed_title.strip()

def process_body(body_str):
    if not body_str:
        return ""

    processed_body = sentence_case(body_str)

    if len(processed_body) > 50:
        processed_body = processed_body[:47] + "..."
    return processed_body

def process_url(url_str):
    if not url_str:
        return None
    if '?' in url_str:
        return f"{url_str}&ref=riseofmachine.com"
    else:
        return f"{url_str}?ref=riseofmachine.com"

def process_pricing_tag(pricing_str):
    if not pricing_str:
        return 'Not available'

    pricing_lower = pricing_str.lower()

    # Direct matches
    if 'free' == pricing_lower and 'freemium' not in pricing_lower: # "Free" but not "Freemium"
        return 'Free'
    if 'freemium' in pricing_lower or 'free plan' in pricing_lower or 'free tier' in pricing_lower or 'trial' in pricing_lower :
        return 'Freemium'
    if 'paid' == pricing_lower: # Simple "Paid" without more info
        return 'Not available' # Or perhaps a specific default like 'Subscription' if that's common

    # From $X/mo
    monthly_match = re.search(r"(\$?\d+(\.\d+)?)\s*(?:per month|/mo|monthly)", pricing_lower)
    if monthly_match:
        return f"From ${monthly_match.group(1)}/mo"

    # $X One-time
    onetime_match = re.search(r"(\$?\d+(\.\d+)?)\s*(?:one-time|lifetime|one time)", pricing_lower)
    if onetime_match:
        return f"${onetime_match.group(1)} One-time"

    # Fallback for other cases
    if 'contact' in pricing_lower or 'quote' in pricing_lower:
        return 'Not available' # Often means custom pricing

    return 'Not available'


def get_existing_categories(tools_filepath):
    existing_tools = load_json_file(tools_filepath)
    categories = set()
    for tool in existing_tools:
        if tool.get('category'):
            categories.add(tool['category'])
    return categories if categories else {'Xtras'} # Ensure 'Xtras' is always an option

def main():
    # 1. Read all JSON files
    aitools_data = load_json_file('aitoolsdirectory_tools.json')
    producthunt_data = load_json_file('producthunt_tools.json')
    existing_tools_data = load_json_file('src/data/tools.json')

    print(f"Loaded {len(aitools_data)} tools from aitoolsdirectory.")
    print(f"Loaded {len(producthunt_data)} tools from producthunt.")
    print(f"Loaded {len(existing_tools_data)} existing tools.")

    # Get valid categories from existing tools
    valid_categories = get_existing_categories('src/data/tools.json')
    print(f"Valid categories: {valid_categories}")

    # 2. Combine tools from scraped files
    scraped_tools = []
    for tool in aitools_data:
        tool['_source'] = 'aitoolsdirectory'
        scraped_tools.append(tool)
    for tool in producthunt_data:
        tool['_source'] = 'producthunt'
        scraped_tools.append(tool)

    print(f"Total scraped tools before deduplication: {len(scraped_tools)}")

    # 3. Remove duplicates from scraped data (name and URL)
    unique_scraped_tools = {}
    for tool in scraped_tools:
        name = tool.get('name')
        url = tool.get('url')
        if not name or not url:
            continue

        # Normalize for deduplication key
        key_name = name.strip().lower()
        key_url = url.strip().lower().rstrip('/')

        key = (key_name, key_url)
        if key not in unique_scraped_tools:
            unique_scraped_tools[key] = tool
        else:
            # Prioritize keeping the one from aitoolsdirectory if duplicate, or one with more fields
            if tool['_source'] == 'aitoolsdirectory' and unique_scraped_tools[key]['_source'] != 'aitoolsdirectory':
                unique_scraped_tools[key] = tool
            elif len(tool.keys()) > len(unique_scraped_tools[key].keys()):
                 unique_scraped_tools[key] = tool

    scraped_tools = list(unique_scraped_tools.values())
    print(f"Scraped tools after deduplication: {len(scraped_tools)}")

    # 4. Filter out tools already present in src/data/tools.json (case-insensitive name)
    existing_tool_names_lower = {tool.get('title', '').lower() for tool in existing_tools_data if tool.get('title')}

    new_tools_to_process = []
    for tool in scraped_tools:
        name = tool.get('name')
        if name and name.lower() not in existing_tool_names_lower:
            new_tools_to_process.append(tool)

    print(f"New tools after filtering existing ones: {len(new_tools_to_process)}")

    # 5. Process each remaining tool
    processed_tools_list = []
    for tool in new_tools_to_process:
        original_name = tool.get('name', '')
        description = tool.get('description', '')
        url = tool.get('url')
        pricing_info = tool.get('pricing', '') # From aitoolsdirectory
        scraped_category_list = tool.get('category', []) # From aitoolsdirectory (it's a list)
        source = tool.get('_source', '')

        # a. Process Title
        processed_title = process_title(original_name)
        if not processed_title: # 6. Filter out tools where title becomes empty
            print(f"Skipping tool '{original_name}' because its title became empty after processing.")
            continue

        # b. Process Body (Description)
        processed_body = process_body(description)

        # c. Process URL
        processed_url = process_url(url)
        if not processed_url: # Skip if URL is invalid after processing (should not happen with current logic)
            print(f"Skipping tool '{original_name}' due to invalid URL.")
            continue

        # d. Date Added
        date_added = '2025-06-06'

        # e. Process Tag (Pricing)
        processed_tag = process_pricing_tag(pricing_info)

        # f. Process Category
        final_category = 'Xtras' # Default
        if source == 'aitoolsdirectory' and scraped_category_list:
            # Use the first category if it's valid, otherwise default to Xtras
            # The scraped_category_list from aitoolsdirectory_tools.json is a list of strings.
            potential_category = scraped_category_list[0] if isinstance(scraped_category_list, list) and scraped_category_list else None
            if potential_category and potential_category in valid_categories:
                final_category = potential_category

        processed_tools_list.append({
            'title': processed_title,
            'body': processed_body,
            'url': processed_url,
            'tag': processed_tag,
            'date-added': date_added,
            'category': final_category
        })

    print(f"Processed tools count: {len(processed_tools_list)}")

    # 8. Ensure at least 500 tools if available (or all found valid tools)
    # This step is more about the selection strategy if we had more tools than needed.
    # For now, we process all valid unique tools.
    # If a hard limit was required, we would sort and slice here.
    # E.g., if len(processed_tools_list) > 500:
    #    processed_tools_list = processed_tools_list[:500] # Or some other selection criteria

    # 7. Save the final list
    save_json_file(processed_tools_list, 'new_tools_processed.json')

if __name__ == "__main__":
    main()
