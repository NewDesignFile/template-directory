import json
from bs4 import BeautifulSoup

def parse_tools_from_html(html_content, page_filename):
    """
    Parses tool information from HTML content of a single page.
    """
    tools_on_page = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        tool_tiles = soup.find_all('div', class_='sv-tile')

        if not tool_tiles:
            print(f"No tool tiles found in {page_filename} with class 'sv-tile'. HTML structure might have changed or file is empty.")

        for tile in tool_tiles:
            tool_info = {}

            name_element = tile.find('h3', class_='sv-tile__title')
            tool_info['name'] = name_element.text.strip() if name_element else None

            description_element = tile.find('div', class_='sv-tile__description')
            tool_info['description'] = description_element.text.strip() if description_element else None

            url_element = tile.find('a', class_='sv-tile__btn')
            tool_info['url'] = url_element['href'] if url_element and url_element.has_attr('href') else None

            pricing_element = tile.find('p', class_='sv-tile__price')
            tool_info['pricing'] = pricing_element.text.strip() if pricing_element else None

            category_elements = tile.find_all('div', class_='sv-badge__1')
            categories = [element.text.strip() for element in category_elements if element.text.strip()]
            tool_info['category'] = categories if categories else []

            if tool_info['name'] and tool_info['url']:
                tools_on_page.append(tool_info)
            else:
                print(f"Warning: Skipped a tile in {page_filename} due to missing name or URL. Tile content: {str(tile)[:200]}")
    except Exception as e:
        print(f"Error parsing HTML from {page_filename}: {e}")

    return tools_on_page

def process_local_html_files(file_list):
    all_tools = []
    for html_filename in file_list:
        print(f"Processing file: {html_filename}")
        try:
            with open(html_filename, 'r', encoding='utf-8') as f:
                html_content = f.read()

            if not html_content:
                print(f"Warning: No content in file {html_filename}. Skipping.")
                continue

            tools_from_page = parse_tools_from_html(html_content, html_filename)

            if tools_from_page:
                print(f"Found {len(tools_from_page)} tools in {html_filename}")
                all_tools.extend(tools_from_page)
            else:
                print(f"No tools found or parsed in {html_filename}.")

        except FileNotFoundError:
            print(f"Error: File {html_filename} not found.")
        except Exception as e:
            print(f"An error occurred while processing file {html_filename}: {e}")
    return all_tools

def save_to_json_file(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")

if __name__ == "__main__":
    # List of HTML files to process (only page_1.html in this case)
    html_files_to_process = ["page_1.html"]
    output_filename = "aitoolsdirectory_paged_tools.json"

    print(f"Starting processing for local HTML files: {html_files_to_process}")
    aggregated_tools = process_local_html_files(html_files_to_process)

    if aggregated_tools:
        print(f"Total tools extracted from local files: {len(aggregated_tools)}")
        unique_tools = {}
        for tool in aggregated_tools:
            key = (tool.get('name','').lower(), tool.get('url',''))
            if key[0] and key[1] and key not in unique_tools : # Ensure name and URL exist
                unique_tools[key] = tool

        final_tools_list = list(unique_tools.values())
        print(f"Total unique tools after deduplication: {len(final_tools_list)}")
        save_to_json_file(final_tools_list, output_filename)
    else:
        print("No tools were extracted from local files. Saving empty list.")
        save_to_json_file([], output_filename)

    print("Processing finished.")
