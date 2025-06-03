import json
import re

# Gathered information
raw_name = "usesaaskit.com"
raw_url = "https://www.usesaaskit.com/"
description = "AI SaaS boilerplate for Next.js & React Native."
pricing_tag = "$119 One-time"
date_added = "2025-06-03" # Provided in the task description

# Transform the name into a title
# "usesaaskit.com" becomes "Usesaaskit Com".
# General approach: remove common TLDs, then title case parts. Limit to 3 words.
title = raw_name
# Remove TLDs like .com, .io, .ai, .app, .org, .net, .co
tlds_to_remove = [".com", ".io", ".ai", ".app", ".org", ".net", ".co", ".dev", ".xyz", ".live", ".tech", ".info", ".online", ".help", ".chat", ".i"] # Added .help, .chat, .i
for tld in tlds_to_remove:
    if title.endswith(tld):
        title = title[:-len(tld)]
        # If the original name was like "something.tld", and became "something",
        # the instruction "Usesaaskit Com" implies adding "Com" (or "Ai", "Io", etc.) back as a separate word.
        # Let's try to make the TLD part a new word if it was removed.
        tld_word = tld[1:].capitalize() # .com -> Com
        title = f"{title.capitalize()} {tld_word}" # usesaaskit -> Usesaaskit Com
        break
else: # If no TLD was found and removed from the list, just capitalize
    title = title.capitalize()


# Ensure title case and max 3 words for the title
title_parts = title.split()
# Title case each part
title_cased_parts = [part.capitalize() for part in title_parts]

# Limit to max 3 words
final_title = " ".join(title_cased_parts[:3])


# Append referral to URL
url_with_ref = raw_url + "?ref=riseofmachine.com"

# Create the JSON object
tool_entry = {
  "title": final_title,
  "body": description,
  "tag": pricing_tag,
  "url": url_with_ref,
  "date-added": date_added
}

# Print the formatted JSON string
print(json.dumps(tool_entry, indent=2))
