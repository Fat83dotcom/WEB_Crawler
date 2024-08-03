from bs4 import BeautifulSoup
from scraping_2 import request_content, core, counter_distinct_words
from scraping_2 import word_counter
import re
from collections import deque


def save_links(link: str, site_name: str):
    with open(
        f'links_found_from_{site_name}.txt', 'a+', encoding='utf-8'
    ) as file:
        file.write(
            f'{link}\n'
        )


def save_stats(stats: dict, site_name: str):
    with open(
        f'stats_from_{site_name}.txt', 'a+', encoding='utf-8'
    ) as file:
        file.write(
            f'{stats}\n'
        )


def main_url_certify(url: str) -> bool:
    reg_compile = re.compile(r'^(http(s*))(://)(\w*\.)(.*)$')
    if reg_compile.search(url):
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
    regex = re.compile(href_regex)
    r = re.compile(r'(.+)')
    links: list = [
        regex.findall(link.get('href')) for link in bs.find_all('a', href=r)
    ]
    print(links)
    links = [
        link[0] for link in links if len(link) > 0
    ]
    print(links)
    return links


def search_engine(
    initial_url: str, target_url: str, tag_a_regex: str, site_name: str
) -> dict:
    final_search: dict = {
        'initial_url': initial_url,
        'target_url': target_url,
        'total_pages_found': 0,
        'data_extract_from_pages': []
    }
    search_queue: deque[str] = deque()
    links_finds: set = set()
    counter: int = 0

    initial_bs = request_content(initial_url)
    initial_links = find_tags_a(initial_bs, tag_a_regex)
    search_queue.extend(initial_links)
    links_finds = {link for link in initial_links}
    # print(search_queue)
    # print(links_finds)

    while len(search_queue) > 0:
        extract_next_search_link = search_queue.popleft()
        counter += 1
        bs = get_any_page(target_url, extract_next_search_link)
        save_links(f'{target_url + extract_next_search_link}', site_name)
        links: list = []
        if bs is not None:
            links = find_tags_a(bs, tag_a_regex)
            for link in links:
                if link not in links_finds:
                    links_finds.add(link)
                    search_queue.append(link)
            stats = core(bs.body)
            current_page_data: dict = {
                'current_count': counter,
                'complete_url': target_url + extract_next_search_link,
                'words_find_in_page': stats,
                'total_words_from_page': word_counter(stats),
                'distinct_words_from_page': counter_distinct_words(stats),
            }
            final_search['data_extract_from_pages'].append(current_page_data)
            save_stats(current_page_data, site_name)
        print(
            f'Página pesquisada: {target_url + extract_next_search_link}\n'
            f'Contagem atual: {counter}'
        )

    print(
        f'total de páginas pesquisadas: {counter}'
    )


# url_wiki = 'https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal'
# url_target_wiki = 'https://pt.wikipedia.org'
# reg_wiki = r'^(/wiki/[^:]+)$'
# reg_wiki = r'^(/wiki/)((?!:).)*$'


# url_estacao = 'https://estacao.brainstormtech.com.br/'
# url_target_estacao = 'https://estacao.brainstormtech.com.br'
# reg_estacao = r'^(\/.*)$'


# url_abn = 'https://www.abnimoveis.com.br/'
# url_target_abn = 'https://www.abnimoveis.com.br'
# # reg_abn = r'^(\/.*)$'
# reg_abn = r'(?<=https:\/\/www\.abnimoveis\.com\.br)(\/.*)'


# url_leo = 'https://www.leonardobraz.com.br/'
# url_target_leo = 'https://www.leonardobraz.com.br'
# # reg_leo = r'^(\/.*)$'
# reg_leo = r'(?<=https:\/\/www\.leonardobraz\.com\.br)(\/.*)'


url_pilla = 'https://www.pillaimoveis.com.br/'
url_target_pilla = 'https://www.pillaimoveis.com.br'
reg_pilla = r'^(\/.*)$'
# reg_pilla = r'(?<=https:\/\/www\.pillaimoveis\.com\.br)(\/.*)'


# search_engine(url_wiki, url_target_wiki, reg_wiki, 'wikipedia')
# search_engine(url_estacao, url_target_estacao, reg_estacao, 'estacao')
# search_engine(url_abn, url_target_abn, reg_abn, 'abn')
# search_engine(url_leo, url_target_leo, reg_leo, 'leo')
search_engine(url_pilla, url_target_pilla, reg_pilla, 'pilla')


url = 'https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal'
# url = 'https://estacao.brainstormtech.com.br/'
url_target = 'https://pt.wikipedia.org'
reg_wiki = r'^(/wiki/)((?!:).)*$'

search_engine(url, url_target, reg_wiki)

# print(main_url_certify(url))
