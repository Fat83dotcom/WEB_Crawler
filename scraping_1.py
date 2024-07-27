from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


url = 'https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal'


def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None

    try:
        bs = BeautifulSoup(html, 'html.parser')
        title = bs.h1
    except AttributeError as e:
        print(e)
        return None
    return title


print(get_title(url))
