# test_tool_access.py
try:
    print(f"Attempting to call view_text_website for google.com...")
    # Assuming view_text_website is globally available
    content = view_text_website(url="https://www.google.com")
    print(f"Content length: {len(content)}")
    print("view_text_website seems accessible.")
except NameError as ne:
    print(f"NameError: {ne}. view_text_website is not defined.")
except Exception as e:
    print(f"Other exception: {e}")
