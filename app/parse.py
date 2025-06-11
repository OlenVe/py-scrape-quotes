import csv
from dataclasses import dataclass, astuple
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com/"
PAGES = urljoin(BASE_URL, "page/")


def get_page_url(page_number: int) -> str:
    """Construct the URL for a specific page of quotes."""
    return urljoin(BASE_URL, f"page/{page_number}/")



@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]

def parse_quote(quote_element):
    text = quote_element.select_one(".text").text[1:-1]  # Remove quotes around the text
    author = quote_element.select_one(".author").text
    tags = [tag.text for tag in quote_element.select(".tag")]
    return Quote(text=text, author=author, tags=tags)


def get_all_quotes() -> list[Quote]:
    """Fetch all quotes from all pages."""
    quotes = []
    page_number = 1
    while True:
        page_url = get_page_url(page_number)
        response = requests.get(page_url).content
        soup = BeautifulSoup(response, "lxml")
        page_quotes = soup.select(".quote")
        if not page_quotes:
            break
        quotes.extend(parse_quote(quote) for quote in page_quotes)
        page_number += 1
    return quotes

def main(output_csv_path: str) -> None:
    with open(output_csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["text", "author", "tags"])
        writer.writerows([astuple(quote) for quote in get_all_quotes()])

if __name__ == "__main__":
    main("quotes.csv")
