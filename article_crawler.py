from bs4 import BeautifulSoup
import requests


class Content:
    __slots__ = ('title', 'article_content', 'origin_link')

    def __init__(
        self, title: str, article_content: str, origin_link: str
    ) -> None:
        self.title = title
        self.article_content = article_content
        self.origin_link = origin_link

    def __iter__(self):
        return (
            i for i in (
                self.title, self.article_content, self.origin_link
            )
        )


class WebSite:
    def __init__(
        self, site_name: str, search_url: str, search_result_selector: str,
        title_selector: str, content_selector: str, topic: str
    ) -> None:
        self.site_name = site_name
        self.search_url = search_url
        self.search_result_selector = search_result_selector
        self.title_selector = title_selector
        self.content_selector = content_selector
        self.topic = topic

    def __iter__(self):
        return (
            i for i in (
                self.site_name, self.search_url,
                self.search_result_selector, self.title_selector,
                self.content_selector, self.topic
            )
        )


class Crawler:
    def get_page(self, url: str) -> BeautifulSoup | None:
        try:
            html = requests.get(url, allow_redirects=True)
            return BeautifulSoup(html.text, 'html.parser')
        except Exception:
            return None

    def get_safe(self, bs: BeautifulSoup, selector: str) -> str:
        try:
            child = bs.select(selector)
            if child is not None and len(child) > 0:
                return child[0].get_text()
            return ''
        except Exception:
            return ''

    def get_from_attr(self, bs: BeautifulSoup, attr: str) -> list:
        try:
            return [
                content.get(attr) for content in bs
            ]

        except Exception:
            return []

    def search(self, site: WebSite):
        print(site.search_url + site.topic)
        bs = self.get_page(site.search_url + site.topic)
        target_links = bs.select(site.search_result_selector)
        links = self.get_from_attr(target_links, 'href')
        return links


if __name__ == '__main__':
    # c = Content('page', 'aoskoaksoaoskoaskoaksoakoas', 'oksd')
    # for i in c:
    #     print(i)

    sites = [
        [
            'G1',
            'https://g1.globo.com/busca/?q=',
            'div.widget--info__text-container a',
            'content-head__title',
            'content-text__container',
            'tecnologia',
        ],
        [
            'CNN',
            'https://www.cnnbrasil.com.br/?s=',
            'li.home__list__item a',
            'h1.post__title',
            'div.post__content',
            'marketing+digital'
        ]
    ]

    crawler = Crawler()

    site: list = [
        WebSite(
            row[0], row[1], row[2], row[3], row[4], row[5]
        ) for row in sites
    ]

    for s in site:
        print(crawler.search(s))
