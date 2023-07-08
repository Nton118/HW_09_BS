import requests
from bs4 import BeautifulSoup
import logging
import json


MAIN_URL = "http://quotes.toscrape.com"
quotes_list = []
authors_list = []

logger = logging.getLogger("scrape")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def parse_author(url: str):
    author_url = MAIN_URL + url
    page = requests.get(author_url)
    soup = BeautifulSoup(page.text, "lxml")
    fullname = soup.find("h3", class_="author-title")
    born_date = soup.find("span", class_="author-born-date")
    born_location = soup.find("span", class_="author-born-location")
    description = soup.find("div", class_="author-description")
    author = {
        "fullname": fullname.text.replace(
            "-", " "
        ),  # вирішуємо проблему Александра Дюма
        "born_date": born_date.text,
        "born_location": born_location.text,
        "description": description.text,
    }
    for el in authors_list:
        if el["fullname"] == author["fullname"]:
            return None
    authors_list.append(author)
    logger.info(f"authors count: {len(authors_list)}")


def parse_quotes_page(url: str):
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "lxml")

    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    author_links = soup.find_all("a", string="(about)")
    tags = soup.find_all("div", class_="tags")

    for i in range(0, len(quotes)):
        tags_list = []

        author_page = author_links[i]["href"]
        parse_author(author_page)
        tagsforquote = tags[i].find_all("a", class_="tag")
        for tagforquote in tagsforquote:
            tags_list.append(tagforquote.text)
        quote = {"tags": tags_list, "author": authors[i].text, "quote": quotes[i].text}
        quotes_list.append(quote)
        logger.info(f"qoutes count: {len(quotes_list)}")

    next_button = soup.find("li", class_="next")
    return next_button


if __name__ == "__main__":
    next_button = parse_quotes_page(MAIN_URL)
    while next_button:
        next_link = next_button.find("a")["href"]
        logger.info(f"page {next_link}")
        next_button = parse_quotes_page(MAIN_URL + next_link)

    with open("quotes.json", "w", encoding="utf-8") as fd:
        json.dump(quotes_list, fd, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as fd:
        json.dump(authors_list, fd, ensure_ascii=False, indent=2)
