from bs4 import BeautifulSoup
from random import randint, seed
from time import time
import requests
import re
import urllib


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
        title_selector: str, content_selector: str, topic: str, n_links: int,
        link_complement: str, is_absolute_url: bool, url_pattern: str
    ) -> None:
        self.site_name = site_name
        self.search_url = search_url
        self.search_result_selector = search_result_selector
        self.title_selector = title_selector
        self.content_selector = content_selector
        self.topic = topic
        self.n_links = n_links
        self.link_complement = link_complement
        self.is_absolute_url = is_absolute_url
        self.url_pattern = url_pattern

    def __iter__(self):
        return (
            i for i in (
                self.site_name, self.search_url,
                self.search_result_selector, self.title_selector,
                self.content_selector, self.topic, self.n_links,
                self.link_complement, self.is_absolute_url, self.url_pattern
            )
        )


class Crawler:
    def __get_page(self, url: str) -> BeautifulSoup | None:
        try:
            html = requests.get(url, allow_redirects=True)
            return BeautifulSoup(html.text, 'html.parser')
        except Exception:
            return None

    def __get_safe(self, bs: BeautifulSoup, selector: str) -> str:
        try:
            child = bs.select(selector)
            if child is not None and len(child) > 0:
                return child[0].get_text()
            return ''
        except Exception:
            return ''

    def __get_from_attr(self, bs: BeautifulSoup, attr: str) -> list:
        try:
            return [
                content.get(attr) for content in bs
            ]
        except Exception:
            return []

    def __select_random_link(self, links: list, number_links: int) -> list:
        seed(time())
        lentgh = len(links)
        if lentgh < number_links:
            return [
                links[randint(0, (lentgh - 1))] for _ in range(lentgh)
            ]
        return [
            links[randint(0, (lentgh - 1))] for _ in range(number_links)
        ]

    def __get_target_pages(
        self, site: WebSite, target_link: list
    ):
        result: list = []
        for link in target_link:
            try:
                if site.absolute_url:
                    bs = self.__get_page(site.link_complement + link)
                    title = self.__get_safe(bs, site.title_selector)
                    content = self.__get_safe(bs, site.content_selector)
                    result.append(Content(
                        title, content, site.link_complement + link
                    ))
                else:
                    bs = self.__get_page(link)
                    title = self.__get_safe(bs, site.title_selector)
                    content = self.__get_safe(bs, site.content_selector)
                    result.append(Content(title, content, link))
            except Exception as e:
                print(e)
        return result

    def search(self, site: WebSite) -> list[Content]:
        print(site.search_url + site.topic)
        bs = self.__get_page(site.search_url + site.topic)
        target_links = bs.select(site.search_result_selector)
        links = self.__get_from_attr(target_links, 'href')
        select_links = self.__select_random_link(links, site.n_links)

        return self.__get_target_pages(site, select_links)


if __name__ == '__main__':
    # c = Content('page', 'aoskoaksoaoskoaskoaksoakoas', 'oksd')
    # for i in c:
    #     print(i)

    sites = [
        [
            'G1',
            'https://g1.globo.com/busca/?q=',
            'div.widget--info__text-container a',
            'h1.content-head__title',
            'p.content-text__container',
            'tecnologia',
            4,
            'https:',
            True
        ],
        [
            'CNN',
            'https://www.cnnbrasil.com.br/?s=',
            'li.home__list__item a',
            'h1.post__title',
            'div.post__content',
            'marketing+digital',
            5,
            '',
            False
        ]
    ]

    crawler = Crawler()

    site: list = [
        WebSite(
            row[0], row[1], row[2],
            row[3], row[4], row[5],
            row[6], row[7], row[8]
        ) for row in sites
    ]
    results: list = []
    for s in site:
        results.append(crawler.search(s))

    for result in results:
        for r in result:
            print(list(r))
        print(100*'*')
