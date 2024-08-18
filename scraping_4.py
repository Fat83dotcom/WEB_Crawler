from bs4 import BeautifulSoup
import requests


class Content:
    def __init__(self, url: str, title: str, body: str) -> None:
        self.url = url
        self.title = title
        self.body = body

    def __str__(self) -> str:
        class_content = f'''
        Url: {self.url}
        Title: {self.title}
        Body: {self.body}
        '''
        return class_content


class WebSite:
    def __init__(
        self, name: str, url: str, title_tag: str, body_tag: str
    ) -> None:
        self.name = name
        self.url = url
        self.title_tag = title_tag
        self.body_tag = body_tag


class Crawler:
    def get_page(self, url: str) -> BeautifulSoup | None:
        '''Faz requisições e retorna um objeto BeautifulSoup.'''
        try:
            html = requests.get(url, allow_redirects=True)
            bs = BeautifulSoup(html.text, 'html.parser')
        except Exception as e:
            print(e)
            return None
        return bs

    def safe_get(self, bs: BeautifulSoup, selector: str) -> str:
        selected_elems = bs.select(selector)
        if selected_elems is not None and len(selected_elems) > 0:
            return '\n'.join(
                [elem.get_text() for elem in selected_elems]
            )
        return ''

    def parse(self, site: WebSite):
        bs = self.get_page(site.url)
        if bs is not None:
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title != '' and body != '':
                print(Content(site.url, title, body))


if __name__ == '__main__':
    sites = [
        ['Meu Portfólio', 'https://www.brainstormtech.com.br', 'h1', 'main']
    ]

    crawler = Crawler()
    websites: list = []
    for row in sites:
        websites.append(WebSite(row[0], row[1], row[2], row[3]))

    for website in websites:
        crawler.parse(website)
