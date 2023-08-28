from typing import List
import requests

from .dataclass import NotionBlock, NotionPage, TitleElement


def fetch_block_content(block_id: str, headers: dict) -> List[NotionBlock]:
    block_endpoint = f"https://api.notion.com/v1/blocks/{block_id}/children"

    response = requests.get(block_endpoint, headers=headers)
    if response.status_code == 200:
        block_data = response.json()
        blocks = []
        for id, block in enumerate(block_data.get("results", [])):
            block_type = block["type"]
            if block_type == "paragraph":
                text_content = "".join(
                    [text["plain_text"] for text in block["paragraph"]["text"]]
                )
                blocks.append(
                    NotionBlock(block_type=block_type, text_content=text_content, block_id=id)
                )
        return blocks
    else:
        print("Error fetching block content:", response.status_code)
        print(response.json())
        return []


def get_notion_pages(
    NOTION_API_TOKEN: str = None
) -> List[NotionPage]:
    NOTION_API_ENDPOINT = "https://api.notion.com/v1/search"
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Notion-Version": "2021-08-16",  # Check for the latest Notion API version
    }
    query_params = {
        "query": "",  # An empty query fetches all pages
        "sort": {"direction": "ascending", "timestamp": "last_edited_time"},
    }
    pages = []
    try:
        while True:
            response = requests.post(
                NOTION_API_ENDPOINT, headers=headers, json=query_params
            )
            if response.status_code == 200:
                search_results = response.json()
                results = search_results.get("results", [])
                for id, result in enumerate(results):
                    if result["object"] == "page":
                        title_property = (
                            result.get("properties", {})
                            .get("title", {})
                            .get("title", [])
                        )
                        if title_property:
                            title = title_property[0].get("plain_text", "")
                        else:
                            title = ""  # Default title if no title found

                        blocks = fetch_block_content(result["id"], headers=headers)
                        title_element = TitleElement(
                            content = title, title_id = id
                        )
                        page = NotionPage(
                            title=title_element, blocks=blocks, url=result.get("url"), title_id=id
                        )
                        pages.append(page)
                next_cursor = search_results.get("next_cursor")
                if not next_cursor:
                    break
                query_params["start_cursor"] = next_cursor
            else:
                print("Error:", response.status_code)
                print(response.json())
                break
        return pages

    except Exception as e:
        print(e)
        return []


if __name__ == "__main__":
    notion_pages = get_notion_pages()
    for page in notion_pages:
        print("Title:", page.title)
        print("URL:", page.url)
        print("Paragraphs:")
        for paragraph in page.blocks:
            print("-", paragraph.text_content)
        print("-" * 20)
