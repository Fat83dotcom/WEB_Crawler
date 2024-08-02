from bs4 import BeautifulSoup
from scraping_2 import request_content, find_all_for_tag
import re
from collections import deque


def main_url_certify(url: str) -> bool:
    reg_compile = re.compile(r'^(http(s*))(://)(\w*\.)(.*)$')
    if re.search(reg_compile, url):
        return True
    return False


def get_any_page(main_url: str, secondary_url: str) -> BeautifulSoup | None:
    if main_url_certify(main_url):
        try:
            url = main_url + secondary_url
            bs = request_content(url)
            if bs is not None:
                return bs
            return None
        except Exception:
            return None
    return None


def find_tags_a(bs: BeautifulSoup, href_regex: str) -> list:
    href_regex = re.compile(href_regex)
    links: list = [
        link.get('href') for link in bs.find_all('a', href=href_regex)
    ]
    return links


def search_engine(initial_url: str, main_url: str, tag_a_regex: str) -> dict:
    final_search: dict = {}
    search_queue: deque[str] = deque()

    initial_bs = request_content(initial_url)
    initial_links = find_tags_a(initial_bs, tag_a_regex)
    search_queue.extend(initial_links)

    print(search_queue)

    while len(search_queue) > 0:
        extract_next_search_link = search_queue.popleft()
        bs = get_any_page(main_url, extract_next_search_link)
        links: list = []
        if bs is not None:
            links = find_tags_a(bs, tag_a_regex)
        if links:
            search_queue.extend(links)
        print(search_queue)


url = 'https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal'
# url = 'https://estacao.brainstormtech.com.br/'
url_target = 'https://pt.wikipedia.org'
reg_wiki = r'^(/wiki/)((?!:).)*$'

search_engine(url, url_target, reg_wiki)

# print(main_url_certify(url))
