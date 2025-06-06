import json
from bs4 import BeautifulSoup

def extract_tool_info(html_file_path):
    """
    Extracts tool information from an HTML file and returns it as a list of dictionaries.

    Args:
        html_file_path (str): The path to the HTML file.

    Returns:
        list: A list of dictionaries, where each dictionary contains information about a tool.
    """
    tools_data = []
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        tool_tiles = soup.find_all('div', class_='sv-tile')

        for tile in tool_tiles:
            tool_info = {}

            # Extract tool name
            name_element = tile.find('h3', class_='sv-tile__title')
            if name_element:
                tool_info['name'] = name_element.text.strip()
            else:
                tool_info['name'] = None

            # Extract tool description
            description_element = tile.find('div', class_='sv-tile__description')
            if description_element:
                tool_info['description'] = description_element.text.strip()
            else:
                tool_info['description'] = None

            # Extract tool URL
            url_element = tile.find('a', class_='sv-tile__btn')
            if url_element and url_element.has_attr('href'):
                tool_info['url'] = url_element['href']
            else:
                tool_info['url'] = None

            # Extract tool pricing
            pricing_element = tile.find('p', class_='sv-tile__price')
            if pricing_element:
                tool_info['pricing'] = pricing_element.text.strip()
            else:
                tool_info['pricing'] = None

            # Extract tool category
            category_elements = tile.find_all('div', class_='sv-badge__1')
            categories = [element.text.strip() for element in category_elements if element.text.strip()]
            tool_info['category'] = categories if categories else None


            # Only add tool if name is present
            if tool_info['name']:
                tools_data.append(tool_info)

    except FileNotFoundError:
        print(f"Error: HTML file not found at {html_file_path}")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")

    return tools_data

def save_to_json(data, json_file_path):
    """
    Saves data to a JSON file.

    Args:
        data (list): The data to save.
        json_file_path (str): The path to the JSON file.
    """
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {json_file_path}")
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")

if __name__ == "__main__":
    html_file = 'aitoolsdirectory.html'
    json_file = 'aitoolsdirectory_tools.json'

    extracted_tools = extract_tool_info(html_file)
    if extracted_tools:
        save_to_json(extracted_tools, json_file)
