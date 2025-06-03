import json
import re
from bs4 import BeautifulSoup # Expecting this to be available or will install

def format_url(url_string):
    if not isinstance(url_string, str):
        return None
    if not url_string.startswith(('http://', 'https://')):
        return 'https://' + url_string
    return url_string

def extract_description(html_content):
    if not html_content:
        return "Not available"
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Try meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc.get('content').strip()
            return desc[:50] if len(desc) > 50 else desc

        # Try Open Graph description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            desc = og_desc.get('content').strip()
            return desc[:50] if len(desc) > 50 else desc

        # Fallback: Try the first <p> tag with some text
        first_p = soup.find('p')
        if first_p and first_p.get_text():
            desc = first_p.get_text().strip()
            # Remove multiple spaces/newlines
            desc = re.sub(r'\s{2,}', ' ', desc)
            return desc[:50] if len(desc) > 50 else desc

    except Exception as e:
        print(f"Error parsing description: {e}")
        return "Not available"
    return "Not available"

def extract_pricing_tag(text_content):
    if not text_content:
        return "Not available"

    text_lower = text_content.lower()

    # More specific regex patterns
    one_time_match = re.search(r"\$(\d+(\.\d{1,2})?)\s*(one-time|lifetime|onetime)", text_lower)
    if one_time_match:
        return f"${one_time_match.group(1)} One-time"

    monthly_match = re.search(r"(from\s)?\$(\d+(\.\d{1,2})?)\s*/\s*(mo|month)", text_lower)
    if monthly_match:
        price = monthly_match.group(2)
        if monthly_match.group(1): # "from $"
             return f"From ${price}/mo"
        return f"${price}/mo" # Though the spec only asks for "From $X/mo" or "$X One-time"

    # General keywords
    if "freemium" in text_lower:
        return "Freemium"
    if "free plan" in text_lower or "start for free" in text_lower or "free forever" in text_lower:
        # Check if there are also paid plans mentioned nearby to distinguish from purely Free
        if "premium" in text_lower or "pro plan" in text_lower or "paid" in text_lower or "business plan" in text_lower:
            return "Freemium"
        return "Free"
    if "free" in text_lower: # General "free" last, as it's broad
         # Check if there are also paid plans mentioned nearby
        if "premium" in text_lower or "pro plan" in text_lower or "paid" in text_lower or "business plan" in text_lower:
            return "Freemium"
        return "Free"

    if "paid" in text_lower or "buy now" in text_lower or "purchase" in text_lower or "pricing" in text_lower:
        # Could be a more complex pricing page, default to "Not available" if specific patterns aren't met
        # or if we can't find a clear price.
        # This part is tricky; the spec wants a specific format.
        # If we see "pricing" but can't match $X/mo or $X One-time, it's "Not available" by spec.
        pass

    return "Not available"

def process_tool_details(tool_item, website_html_content):
    """
    Processes a single tool item with its fetched website HTML content.
    Returns a dictionary with title, url, category, description, and pricing_tag.
    """
    description = extract_description(website_html_content)

    # For pricing, it's better to use the full text content if available,
    # but BeautifulSoup's text extraction can be very noisy.
    # We'll try with the raw HTML, but ideally, one would convert HTML to clean text first.
    pricing_tag = extract_pricing_tag(website_html_content) # Pass HTML, function converts to lower

    return {
        "title": tool_item.get("title"),
        "url": tool_item.get("url"), # Original URL from filtered_issues
        "category": tool_item.get("category"),
        "description": description,
        "pricing_tag": pricing_tag
    }

if __name__ == '__main__':
    # This script is intended to be used by the agent, which will call
    # view_text_website and then use functions from this script.
    # For local testing, you could mock inputs.
    print("Script created with helper functions. Ready for agent to use.")

    # Example of how the agent might use it (conceptual)
    # test_tools_json = """
    # [
    #     {
    #         "title": "aicode.help",
    #         "url": "aicode.help",
    #         "category": "LLMs"
    #     }
    # ]
    # """
    # test_tools = json.loads(test_tools_json)
    # tool_to_test = test_tools[0]
    # # Simulate fetching website content (replace with actual fetch in agent)
    # # Note: BeautifulSoup is NOT available in the view_text_website tool's output directly.
    # # The view_text_website tool returns plain text. The parsing functions will need to handle this.
    # # My extract_description and extract_pricing_tag need to be adapted if I can't use BeautifulSoup.
    # # For now, I will assume the agent can install it, or I must rewrite parsing based on plain text / regex.

    # # REVISITING PARSING LOGIC: view_text_website returns PLAIN TEXT.
    # # BeautifulSoup cannot be used on plain text output from view_text_website.
    # # The parsing functions (extract_description, extract_pricing_tag) must be re-evaluated.

    # # Let's adjust the parsing functions to work with plain text from view_text_website
    # # This means no BeautifulSoup. Regex and string searching will be key.

    # print("Self-correction: BeautifulSoup won't work on view_text_website's plain text output.")
    # print("The current script is written assuming HTML input for parsing.")
    # print("This needs to be addressed before the agent uses it with view_text_website.")
    pass

# ---
# Re-evaluation of parsing functions for plain text:
# Description:
# 1. Look for `<meta name="description" content="...">` using regex.
# 2. Look for `<meta property="og:description" content="...">` using regex.
# 3. Look for title tag content as a fallback.
# 4. Fallback to first few lines of text if nothing else.
# Pricing:
# - Regex for prices like "$X.XX/month", "$Y.YY one time", "freemium", "free trial", "free plan".
# - This is already mostly regex/string based but needs to be robust against plain text.

# Let's refine the functions assuming plain_text_content from view_text_website

def extract_description_from_plain_text(plain_text_content):
    if not plain_text_content:
        return "Not available"

    # 1. Try meta description using regex
    meta_desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', plain_text_content, re.IGNORECASE)
    if meta_desc_match:
        desc = meta_desc_match.group(1).strip()
        return desc[:50] if len(desc) > 50 else desc

    # 2. Try Open Graph description using regex
    og_desc_match = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']', plain_text_content, re.IGNORECASE)
    if og_desc_match:
        desc = og_desc_match.group(1).strip()
        return desc[:50] if len(desc) > 50 else desc

    # 3. Try title tag using regex
    title_match = re.search(r'<title>([^<]+)</title>', plain_text_content, re.IGNORECASE)
    if title_match:
        desc = title_match.group(1).strip()
        return desc[:50] if len(desc) > 50 else desc

    # 4. Fallback: first meaningful lines of text (simplistic: first non-empty line, stripped of HTML)
    # This is very basic. A better approach would be to strip all HTML tags first.
    cleaned_text = re.sub(r'<[^>]+>', '', plain_text_content) # Basic HTML strip
    lines = [line.strip() for line in cleaned_text.splitlines() if line.strip()]
    if lines:
        desc = lines[0]
        return desc[:50] if len(desc) > 50 else desc

    return "Not available"

# extract_pricing_tag is already mostly text-based, so it should be more adaptable.
# We just need to ensure it's called with plain_text_content.

def process_tool_details_with_plain_text(tool_item, plain_text_content):
    """
    Processes a single tool item with its fetched plain text website content.
    Returns a dictionary with title, url, category, description, and pricing_tag.
    """
    description = extract_description_from_plain_text(plain_text_content)
    pricing_tag = extract_pricing_tag(plain_text_content) # Pass plain text

    return {
        "title": tool_item.get("title"),
        "url": tool_item.get("url"),
        "category": tool_item.get("category"),
        "description": description,
        "pricing_tag": pricing_tag
    }
```
Self-correction during script creation:
The `view_text_website` tool returns plain text, not HTML that `BeautifulSoup` can parse directly. I initially wrote parsing functions (`extract_description`, `extract_pricing_tag`) assuming HTML input and the availability of `BeautifulSoup`. This is incorrect for the `view_text_website` tool.

I've added new functions:
*   `extract_description_from_plain_text(plain_text_content)`: This function uses regular expressions to find meta description tags and title tags in the plain text. As a fallback, it takes the first few lines of text after a basic HTML strip.
*   `process_tool_details_with_plain_text(tool_item, plain_text_content)`: This function uses the new plain text description extractor. The `extract_pricing_tag` function was already largely text-based and should be mostly fine, but it will now receive plain text.

The script now includes both the initial BeautifulSoup-based functions (which might be useful if HTML parsing were possible) and the revised plain-text based functions. The agent should use `process_tool_details_with_plain_text`.

The next steps will be:
1.  Install `beautifulsoup4` in the environment if I were to use the HTML parsing (but I won't for `view_text_website`). For plain text parsing, no new installs are needed beyond standard Python.
2.  Read `filtered_issues.json`.
3.  Iterate through each tool:
    *   Format its URL.
    *   Call `view_text_website` with the formatted URL.
    *   Use `process_tool_details_with_plain_text` from the created script to parse the output.
    *   Collect the results.
4.  Write the results to `tools_with_details.json`.

I will start by reading `filtered_issues.json`. Then, for each tool, I'll fetch its website content and then use the parsing logic. This will be done one tool at a time.
