import json
import re
from urllib.parse import urlparse, urlunparse
from titlecase import titlecase

def sentence_case(text):
    if not text:
        return ""
    if len(text) > 1:
        return text[0].upper() + text[1:].lower()
    elif len(text) == 1:
        return text[0].upper()
    return ""

def load_json_file(filepath, default_source_name=None):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Add source if not present, useful for deduplication strategy
            if default_source_name:
                for item in data:
                    if '_source' not in item:
                        item['_source'] = default_source_name
            return data
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

def get_core_url(url_str):
    if not url_str:
        return None
    try:
        parsed = urlparse(url_str)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', '')).rstrip('/')
    except Exception:
        return url_str.lower().rstrip('/') # Fallback for malformed URLs

def process_title(title_str):
    if not title_str:
        return ""
    processed_title = titlecase(str(title_str)) # Ensure input is string
    if processed_title.lower().startswith('ai '):
        processed_title = processed_title[3:]
    words = processed_title.split()
    if len(words) > 3:
        processed_title = ' '.join(words[:3])
    return processed_title.strip()

def process_body(body_str):
    if not body_str:
        return "No description available."
    # Clean up common markdown link/review patterns from awesome_ai_tools
    body_str = re.sub(r'\s*-\s*\*\[reviews\]\(.*\)\s*-\s*', '', body_str) # Matches " - *[reviews](...)* - "
    body_str = re.sub(r'\s*\*\[reviews\]\(.*\)\s*', '', body_str)       # Matches " *[reviews](...)*"
    body_str = re.sub(r'\s*\[Review on Altern\]\(.*\)\s*-\s*', '', body_str, flags=re.IGNORECASE)
    body_str = body_str.lstrip('*- ').strip()

    processed_body = sentence_case(str(body_str)) # Ensure input is string
    if len(processed_body) > 50:
        processed_body = processed_body[:47] + "..."
    elif not processed_body: # If after cleaning it's empty
        return "No description available."
    return processed_body

def process_url(url_str):
    if not url_str or not isinstance(url_str, str) or not (url_str.startswith('http://') or url_str.startswith('https://')):
        return None # Invalid or missing URL

    # Ensure ref is appended correctly
    if '?' in url_str:
        if 'ref=riseofmachine.com' not in url_str:
             return f"{url_str}&ref=riseofmachine.com"
        return url_str # Already has the ref
    else:
        return f"{url_str}?ref=riseofmachine.com"


def process_pricing_tag(pricing_str):
    if not pricing_str or not isinstance(pricing_str, str):
        return 'Not available'

    pricing_lower = pricing_str.lower()
    if 'free' == pricing_lower and 'freemium' not in pricing_lower:
        return 'Free'
    if 'freemium' in pricing_lower or 'free plan' in pricing_lower or 'free tier' in pricing_lower or 'trial' in pricing_lower :
        return 'Freemium'
    if 'paid' == pricing_lower:
        return 'Not available'

    monthly_match = re.search(r"(\$?\d+(\.\d+)?)\s*(?:per month|/mo|monthly)", pricing_lower)
    if monthly_match:
        return f"From ${monthly_match.group(1)}/mo"

    onetime_match = re.search(r"(\$?\d+(\.\d+)?)\s*(?:one-time|lifetime|one time)", pricing_lower)
    if onetime_match:
        return f"${onetime_match.group(1)} One-time"

    if 'contact' in pricing_lower or 'quote' in pricing_lower:
        return 'Not available'

    return 'Not available'

def main():
    # 1. Read tools from all sources
    aitools_paged_data = load_json_file('aitoolsdirectory_paged_tools.json', 'aitoolsdirectory')
    producthunt_data = load_json_file('producthunt_tools.json', 'producthunt')
    awesome_data = load_json_file('awesome_ai_tools.json', 'awesome')
    existing_tools_data = load_json_file('src/data/tools.json') # Should be empty or contain existing tools

    print(f"Loaded {len(aitools_paged_data)} tools from aitoolsdirectory_paged_tools.json.")
    print(f"Loaded {len(producthunt_data)} tools from producthunt_tools.json.")
    print(f"Loaded {len(awesome_data)} tools from awesome_ai_tools.json.")
    print(f"Loaded {len(existing_tools_data)} existing tools from src/data/tools.json.")

    # 3. Combine tools
    all_scraped_tools = aitools_paged_data + producthunt_data + awesome_data
    print(f"Total scraped tools before any deduplication: {len(all_scraped_tools)}")

    # 4. Remove duplicate tools
    # Prioritize: awesome_ai_tools > aitoolsdirectory > producthunt
    # Key for deduplication: (lower_case_name, core_url)
    unique_tools_map = {}
    source_priority = {'awesome': 1, 'aitoolsdirectory': 2, 'producthunt': 3}

    for tool in all_scraped_tools:
        name = str(tool.get('name', '')).strip().lower()
        url = get_core_url(tool.get('url'))

        if not name or not url:
            continue # Skip tools with no name or URL

        key = (name, url)
        current_source = tool.get('_source', 'unknown')

        if key not in unique_tools_map:
            unique_tools_map[key] = tool
        else:
            existing_tool_source = unique_tools_map[key].get('_source', 'unknown')
            if source_priority.get(current_source, 99) < source_priority.get(existing_tool_source, 99):
                unique_tools_map[key] = tool # Replace if current tool has higher priority source
            # Optional: Add more logic here to merge fields if desired

    combined_tools = list(unique_tools_map.values())
    print(f"Combined tools after deduplication: {len(combined_tools)}")

    # 5. Filter out tools already present in src/data/tools.json
    existing_tool_names_lower = {str(tool.get('title', '')).lower() for tool in existing_tools_data if tool.get('title')}

    new_tools_to_process = []
    for tool in combined_tools:
        name = str(tool.get('name', '')).strip().lower()
        if name and name not in existing_tool_names_lower:
            new_tools_to_process.append(tool)

    print(f"New tools after filtering existing ones: {len(new_tools_to_process)}")

    # 6. Process each remaining tool
    final_processed_tools = []
    for tool in new_tools_to_process:
        original_name = str(tool.get('name', ''))
        description = str(tool.get('description', ''))
        url = tool.get('url')

        # a. Process Title
        processed_title = process_title(original_name)

        # c. Process URL (do this before title check, as invalid URL means discard)
        processed_url = process_url(url)
        if not processed_url:
            print(f"Skipping tool '{original_name}' due to invalid or missing URL.")
            continue

        if not processed_title: # Filter out tools where title became empty
            print(f"Skipping tool '{original_name}' (URL: {url}) because its title became empty after processing.")
            continue

        # b. Process Body
        processed_body = process_body(description)

        # d. Date Added
        date_added = '2025-06-06'

        # e. Tag (Pricing)
        # Pricing info most likely from aitoolsdirectory, other sources might not have it.
        pricing_info = str(tool.get('pricing', '')) if tool.get('_source') == 'aitoolsdirectory' else ''
        processed_tag = process_pricing_tag(pricing_info)

        # f. Category
        # Use scraped category, convert to lowercase. Default to 'xtras' if no category.
        scraped_category = tool.get('category', 'xtras') # 'category' from awesome_ai_tools is string, from aitools is list

        if isinstance(scraped_category, list):
            original_category = scraped_category[0].lower() if scraped_category else 'xtras'
        elif isinstance(scraped_category, str):
            original_category = scraped_category.lower().strip() if scraped_category.strip() else 'xtras'
        else:
            original_category = 'xtras'

        if not original_category: # handle cases where category might be empty string after processing
            original_category = 'xtras'


        final_processed_tools.append({
            'title': processed_title,
            'body': processed_body,
            'url': processed_url,
            'tag': processed_tag,
            'date-added': date_added,
            'original_category': original_category # Save the processed original category
        })

    print(f"Final processed tools count: {len(final_processed_tools)}")

    # 7. Save the final list
    save_json_file(final_processed_tools, 'all_new_tools_processed.json')

if __name__ == "__main__":
    main()
