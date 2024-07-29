import requests
from bs4 import BeautifulSoup

'''Minerador de palavras: O programa conta todas ocorrencias de palavras de um
site, varrendo todos os links existentes na página inicial,
retonando um dicionario.'''


def request_content(url: str,) -> BeautifulSoup | None:
    '''Faz requisições e retorna um objeto BeautifulSoup.'''
    try:
        html = requests.get(url)
        bs = BeautifulSoup(html.text, 'html.parser')
    except Exception:
        return None
    return bs


def find_all_for_tag(bs: BeautifulSoup, tag: str) -> list:
    '''Busca todas ocorrencias de uma tag.'''
    tags = bs.find_all(tag)
    return tags


def find_tag_content(tag: BeautifulSoup):
    '''Mostra o conteudo de determinada tag.'''
    try:
        t = tag.get_text()
    except (AttributeError, Exception):
        return None
    return t


def word_separator(content: str) -> list:
    '''Separa strings usando o separador padrão Python'''
    try:
        content = content.split()
    except Exception:
        return []
    return content


def word_analitics(content: list) -> dict:
    '''Cria um dicionario com strings distintas e a quatidade
    de ocorrencias.'''
    struct: dict = {}
    for word in content:
        if word not in struct:
            struct[word] = 1
        else:
            struct[word] += 1
    return struct


def word_counter(content: dict) -> int:
    total_words = 0
    for k, v in enumerate(content.items()):
        total_words += v

    return total_words


# url = 'https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal'
url = 'https://www.w3schools.com/'

links = request_content(url)

links_first_page = [
    link.get('href') for link in find_all_for_tag(links, 'a')
]

total_words: list = []
for link in links_first_page:
    bs_obj = request_content(link)
    if bs_obj is not None:
        total_words += word_separator(find_tag_content(bs_obj.body))

result = word_analitics(total_words)
total_words = word_counter(result)
print(total_words)
