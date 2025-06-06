import json
import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def title_case_preserve_ai_gpt(text):
    """Converts to Title Case but keeps 'AI' and 'GPT' as uppercase."""
    words = text.split()
    title_cased_words = []
    for word in words:
        if word.upper() in ["AI", "GPT"]:
            title_cased_words.append(word.upper())
        else:
            title_cased_words.append(word.capitalize())
    return " ".join(title_cased_words)

def format_title(title_str):
    """Formats the tool title according to specified rules."""
    title_str = title_str.strip()
    if title_str.lower().startswith("ai "):
        title_str = title_str[3:].strip()
    elif title_str.lower().startswith("gpt "): # Also check for GPT prefix
        title_str = title_str[4:].strip()

    # Title Case (custom to preserve AI, GPT)
    title_str = title_case_preserve_ai_gpt(title_str)

    words = title_str.split()
    if len(words) > 3:
        title_str = " ".join(words[:3]) + "..."
    else:
        title_str = " ".join(words) # Ensure no extra spaces if less than 3 words
    return title_str

def format_body(body_str):
    """Formats the tool body: sentence case and truncate to 50 chars."""
    if not body_str:
        return ""
    # Sentence case: Capitalize first letter, rest lower (simple version)
    body_str = body_str.strip()
    body_str = body_str[0].upper() + body_str[1:].lower()

    if len(body_str) > 50:
        body_str = body_str[:47]
        # Try to end on a word boundary
        last_space = body_str.rfind(' ')
        if last_space != -1:
            body_str = body_str[:last_space]
        body_str += "..."
    return body_str

def format_url(url_str):
    """Appends ref parameter to the URL."""
    ref_param = "ref=riseofmachine.com"
    parsed_url = urlparse(url_str)
    query = parse_qs(parsed_url.query)

    if 'ref' in query: # If ref is already there, don't modify (or decide to overwrite)
        pass # For now, let's assume we don't overwrite existing ref
    else:
        query['ref'] = ['riseofmachine.com']

    new_query_string = urlencode(query, doseq=True)

    return urlunparse(parsed_url._replace(query=new_query_string))


def map_tag(tag_guess_str):
    """Maps guessed tag to a standard pricing tag."""
    tag_lower = tag_guess_str.lower()
    if "freemium" in tag_lower:
        return "Freemium"
    if "free" in tag_lower: # Check after freemium
        return "Free"
    if "open-source" in tag_lower and not any(price_kw in tag_lower for price_kw in ["paid", "$", "contact"]): # OS is often free
        return "Free"

    # Look for price patterns
    # Monthly price
    match_mo = re.search(r'\$(\d+(\.\d{1,2})?)\s*(/mo|per month|monthly)', tag_lower)
    if match_mo:
        price = match_mo.group(1)
        return f"From ${price}/mo" # Or just "From $X/mo" if we don't want specific prices yet

    # One-time price
    match_one_time = re.search(r'\$(\d+(\.\d{1,2})?)\s*(one-time|onetime|once)', tag_lower)
    if match_one_time:
        price = match_one_time.group(1)
        return f"${price} One-time" # Or "$X One-time"

    if "paid" in tag_lower or "subscription" in tag_lower or "$" in tag_lower:
         # Generic paid if specific pattern not matched but indicators are there
        return "Not available" # Defaulting to "Not available" if price is mentioned but not parsable to specific format

    if "contact" in tag_lower or "request" in tag_lower:
        return "Contact for pricing" # This will map to "Not available" later as per allowed tags

    return "Not available" # Default

def get_final_tag(mapped_tag_str):
    """ Ensure the tag is one of the allowed ones """
    allowed_tags = ["Free", "Freemium", "From $X/mo", "$X One-time", "Not available"]
    if mapped_tag_str.startswith("From $") and mapped_tag_str.endswith("/mo"):
        # Extract price to make it generic for now as per allowed_tags
        # For this task, let's map specific prices to the generic "From $X/mo"
        # Or, if the task means ANY $X is fine, then this is okay.
        # Based on "$X One-time", it seems specific prices are fine.
        # Let's assume specific prices are okay for "From $X/mo" and "$X One-time"
        return mapped_tag_str # e.g. "From $29/mo"
    if mapped_tag_str.startswith("$") and mapped_tag_str.endswith(" One-time"):
        return mapped_tag_str # e.g. "$19 One-time"

    if mapped_tag_str in ["Free", "Freemium"]:
        return mapped_tag_str

    return "Not available"


def main():
    try:
        with open("candidate_tools.json", 'r', encoding='utf-8') as f:
            candidate_tools = json.load(f)
    except FileNotFoundError:
        print("Error: candidate_tools.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from candidate_tools.json.")
        return

    existing_tools_set = set()
    try:
        with open("existing_tools.txt", 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    existing_tools_set.add((parts[0].lower(), parts[1])) # Store title lowercase for case-insensitive check
    except FileNotFoundError:
        print("Warning: existing_tools.txt not found. Proceeding without de-duplication against existing tools.")
        # No existing tools to check against, so this is not fatal

    valid_categories = set()
    try:
        with open("src/data/tools.json", 'r', encoding='utf-8') as f:
            tools_data = json.load(f)
            for cat_group in tools_data.get("tools", []):
                if "category" in cat_group:
                    valid_categories.add(cat_group["category"])
    except FileNotFoundError:
        print("Error: src/data/tools.json not found. Cannot validate categories.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from src/data/tools.json.")
        return
    if not valid_categories:
        print("Error: No valid categories loaded from src/data/tools.json. Using 'xtras' for all.")
        # This could be problematic, but let's allow it to proceed by defaulting to 'xtras'

    processed_tools = []
    skipped_duplicates_count = 0
    date_added = "2025-06-06" # As per requirement

    for candidate in candidate_tools:
        cand_title_lower = candidate.get("title", "").lower()
        cand_url = candidate.get("url", "")

        # De-duplication
        is_duplicate = False
        if (cand_title_lower, cand_url) in existing_tools_set: # Check full tuple first
             is_duplicate = True
        else: # Check title or URL separately
            for ex_title_lower, ex_url in existing_tools_set:
                if cand_title_lower == ex_title_lower or cand_url == ex_url:
                    is_duplicate = True
                    break

        if is_duplicate:
            skipped_duplicates_count += 1
            continue

        # Formatting
        formatted_title = format_title(candidate.get("title", "Untitled"))
        formatted_body = format_body(candidate.get("body", ""))
        formatted_url = format_url(cand_url) # Use original cand_url for formatting

        # Category Assignment
        category_guess = candidate.get("category_guess", "xtras")
        assigned_category = category_guess.lower().replace(" ", "") # normalize guess
        if assigned_category not in valid_categories:
            if not valid_categories: # If valid_categories is empty due to error
                 assigned_category = 'xtras'
            elif category_guess == "Social Media": # Handle common case from generator
                 assigned_category = "social" if "social" in valid_categories else "xtras"
            else:
                 assigned_category = 'xtras'


        # Pricing Tag Assignment
        tag_guess = candidate.get("tag_guess", "Not available")
        mapped_tag = map_tag(tag_guess)
        final_tag = get_final_tag(mapped_tag)


        processed_tool = {
            "title": formatted_title,
            "body": formatted_body,
            "url": formatted_url,
            "category": assigned_category, # Use the internal name
            "date-added": date_added,
            "tag": final_tag
        }
        processed_tools.append(processed_tool)
        # Add to existing_tools_set to avoid adding duplicates from candidates themselves
        existing_tools_set.add((formatted_title.lower(), formatted_url))


    try:
        with open("filtered_formatted_tools.json", 'w', encoding='utf-8') as f:
            json.dump(processed_tools, f, indent=2)
    except IOError:
        print("Error: Could not write to filtered_formatted_tools.json.")
        return

    print(f"Number of tools remaining after filtering and formatting: {len(processed_tools)}")
    print(f"Number of tools that were duplicates and skipped: {skipped_duplicates_count}")

if __name__ == "__main__":
    main()
