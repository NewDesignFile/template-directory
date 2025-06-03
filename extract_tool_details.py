import re

# Content fetched previously for usesaaskit.com
# I'm using a condensed version of the relevant parts for brevity here.
site_content = """
Why Wait? Launch Your AI Startup in a Week
The Next.js and React Native boilerplate that gives you auth,
multi-org, admin tools, billing, marketing pages, analytics, and AI —
ready from day one.
trusted developer pic trusted developer pic trusted developer pic
trusted developer pic

Loved by makers
Get Access Documentation

$100 OFF for first 50 customers (8 left)
  * Supabase Auth, Storage & Database
  * Next.js Built for Web Apps
  * React Native Built for iOS & Android Apps
  * Stripe Subscription & Payments
  * Lemon Squeezy Subscription & Payments
  * Tailwind UI & Components
  * + SEO
  * Resend Marketing Emails

Build AI Apps
You can build and launch AI apps in a week using our AI boilerplate. It
uses the Vercel AI SDK, which supports OpenAI, Claude, Gemini, and
other LLMs out of the box. Launching an AI app is now easier than ever
with our boilerplate.

Pricing
Give your ultimate idea an ultimate solution
$100 OFF for first 50 customers (8 left)

Web App AI Boilerplate
$219 $119 USD
One-time payment. Lifetime access
AI Ready Codebase ( Vercel AI SDK )
Multiple LLM Support (OpenAI, Grok, Google Gemini, Anthropic Claude)
(BUTTON) Buy this template

Mobile App AI Boilerplate
$319 $219 USD
One-time payment. Lifetime access
(BUTTON) Buy this template
"""

def extract_description(content):
    # Try a few regex patterns to find a suitable description
    # Pattern 1: Look for a sentence describing the boilerplate near the top.
    match = re.search(r"The Next\.js and React Native boilerplate that gives you .*?AI\s*—\s*ready from day one.", content, re.IGNORECASE | re.DOTALL)
    desc = ""
    if match:
        desc = match.group(0)
        # Clean up and shorten:
        desc = re.sub(r'\s+', ' ', desc).strip() # Normalize whitespace
        # Attempt to make it more concise
        if "Next.js and React Native boilerplate" in desc:
            desc = "Next.js & React Native boilerplate with auth, AI." # Example shortening
        if len(desc) > 50:
             # More aggressive shortening
            if "Next.js and React Native boilerplate" in match.group(0):
                desc = "Next.js & RN boilerplate with AI, auth, billing."
            elif "AI Startup in a Week" in match.group(0): # Fallback to tagline
                 desc = "Launch your AI startup in a week."

    if not desc: # Fallback if primary patterns fail
        match_tagline = re.search(r"Launch Your AI Startup in a Week", content, re.IGNORECASE)
        if match_tagline:
            desc = match_tagline.group(0)
        else:
            desc = "AI-powered SaaS boilerplate." # Generic fallback

    # Ensure Sentence case and length
    desc = desc[0].upper() + desc[1:]
    if not desc.endswith('.'):
        desc += '.'
    return desc[:50]


def extract_pricing_tag(content):
    # Look for one-time payment mentions
    one_time_matches = re.findall(r"\$(\d+)\s*USD\s*One-time payment", content, re.IGNORECASE)
    if one_time_matches:
        # Find the lowest one-time price
        min_price = min([int(p) for p in one_time_matches])
        return f"${min_price} One-time"

    # Look for monthly payments if one-time not found
    # Example: $X/mo or From $X/mo (none in current content but good for general use)
    monthly_match = re.search(r"From\s*\$(\d+)/mo", content, re.IGNORECASE)
    if monthly_match:
        return f"From ${monthly_match.group(1)}/mo"

    monthly_match_simple = re.search(r"\$(\d+)/mo", content, re.IGNORECASE)
    if monthly_match_simple:
        return f"${monthly_match_simple.group(1)}/mo"

    if "Freemium" in content or "Free plan" in content:
        return "Freemium"
    if "Free" in content: # General 'Free' if no other specific pricing
        return "Free"

    return "Not available"

description = extract_description(site_content)
pricing_tag = extract_pricing_tag(site_content)

print("Tool: usesaaskit.com")
print(f"Description (max 50 chars): {description}")
print(f"Pricing Tag: {pricing_tag}")

# A more robust description extraction might be needed if this is too naive.
# For example, looking for <meta name="description"> or specific H1/H2 tags if HTML was available.
# Given plain text, this is an attempt.
if len(description) > 50:
    print(f"Warning: Description exceeds 50 characters (length: {len(description)})")

# Refine description based on actual output if necessary in a follow-up.
# For instance, "Next.js & RN boilerplate with AI, auth, billing." is 49 chars.
# "Launch your AI startup in a week." is 33 chars.
# "AI-powered SaaS boilerplate." is 29 chars.
# "Next.js & React Native boilerplate with auth, AI." is 47 chars.

# Let's try to be more specific based on "The Next.js and React Native boilerplate..."
# "Next.js & RN boilerplate for SaaS with AI." (40 chars)
# "Next.js & RN boilerplate with AI and billing." (45 chars)

# Re-evaluating description logic slightly for better fit
specific_desc_search = re.search(r"The Next\.js and React Native boilerplate that gives you (.*?) ready from day one.", site_content, re.IGNORECASE | re.DOTALL)
final_desc = "AI SaaS boilerplate for Next.js & React Native." # Default
if specific_desc_search:
    features_text = specific_desc_search.group(1)
    if "ai" in features_text.lower():
        final_desc = "Next.js & RN boilerplate with AI features." # 41 chars
        if "billing" in features_text.lower():
            final_desc = "Next.js & RN boilerplate: AI, billing, auth." #46 chars
    else: # Should not happen based on site_content but as a fallback
        final_desc = "Next.js & RN boilerplate for SaaS products."


# Ensure Sentence case and length for the refined description
final_desc = final_desc[0].upper() + final_desc[1:]
if not final_desc.endswith('.'):
    final_desc += '.'
if len(final_desc) > 50: # If it somehow still too long, truncate
    final_desc = final_desc[:47] + "..."


print("\nRefined Attempt:")
print("Tool: usesaaskit.com")
print(f"Description (max 50 chars): {final_desc}")
print(f"Pricing Tag: {pricing_tag}")

# Final check on pricing, $119 is the lowest discounted
if pricing_tag == "$219 One-time" or pricing_tag == "$119 One-time":
    # Check if $119 is present explicitly with "One-time payment"
    match_119 = re.search(r"\$119\s*USD\s*One-time payment", site_content, re.IGNORECASE)
    if match_119:
        pricing_tag = "$119 One-time"
    else: # Fallback to the general logic if specific 119 isn't tied to "one-time" directly (though it is here)
        one_time_prices = [int(p) for p in re.findall(r"\$(\d+)\s*USD\s*One-time payment", content, re.IGNORECASE)]
        if one_time_prices:
            pricing_tag = f"${min(one_time_prices)} One-time"


print("\nFinal Values:")
print("Tool: usesaaskit.com")
print(f"Description: {final_desc}")
print(f"Pricing Tag: {pricing_tag}")
