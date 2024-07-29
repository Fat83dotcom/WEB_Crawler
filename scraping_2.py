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
    '''Conta o total de ocorrencias de strings em um dicionario.'''
    words = 0
    for _, v_count in content.items():
        words += v_count

    return words


def counter_distinct_words(content: dict) -> int:
    return len(content)


def core(url: str) -> dict:
    links = request_content(url)

    links_first_page = [
        link.get('href') for link in find_all_for_tag(links, 'a')
    ]

    words: list = []
    for link in links_first_page:
        bs_obj = request_content(link)
        if bs_obj is not None:
            words += word_separator(find_tag_content(bs_obj.body))

    return word_analitics(words)


# url = 'https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal'
url = 'https://www.w3schools.com/'


result = core(url)
print(result)
print(word_counter(result))
print(counter_distinct_words(result))
