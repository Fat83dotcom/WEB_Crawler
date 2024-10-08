from bs4 import BeautifulSoup
from random import randint, seed
from time import time
import requests
import re
import urllib
from bd_insert import DBManager


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

    def __get_page_change_search_topic(self, site: WebSite):
        url = ''
        if site.topic == '':
            url = site.search_url
        else:
            url = site.search_url + site.topic
        return self.__get_page(url)

    def __parse_unquote_url(self, url: str, site: WebSite) -> str:
        '''
        Extrai parte de uma url com uma expressão regular e decodifica essa
        parte. É usada quando houver urls anti-robos, passando uma regex para
        Website.
        '''
        if site.url_pattern != '':
            match = re.search(site.url_pattern, url)
            if match:
                direct_url = urllib.parse.unquote(match.group(1))
                return direct_url
            else:
                return url
        return url

    def __target_pages_engine(self, site: WebSite, target_url: str) -> Content:
        url = self.__parse_unquote_url(target_url, site)
        bs = self.__get_page(url)
        title = self.__get_safe(bs, site.title_selector)
        content = self.__get_safe(bs, site.content_selector)
        return Content(title, content, url)

    def __get_target_pages(
        self, site: WebSite, target_link: list
    ) -> list:
        result: list = []
        for link in target_link:
            try:
                url = ''
                if site.is_absolute_url:
                    url = link
                else:
                    url = site.link_complement + link
                result.append(self.__target_pages_engine(site, url))
            except Exception as e:
                print(e)
        return result

    def search(self, site: WebSite) -> list[Content]:
        bs = self.__get_page_change_search_topic(site)
        target_links = bs.select(site.search_result_selector)
        links = self.__get_from_attr(target_links, 'href')
        select_links = self.__select_random_link(links, site.n_links)
        return self.__get_target_pages(site, select_links)


if __name__ == '__main__':
    db = DBManager()
    crawler = Crawler()
    data = db.select_data()

    site: list = [
        WebSite(
            row.name_site, row.search_url, row.search_result_selector,
            row.title_selector, row.content_selector, row.topic,
            row.n_link, row.link_complement, row.is_absolute_url,
            row.url_pattern
        ) for row in data
    ]

    results: list = [
        crawler.search(s) for s in site
    ]

    for result in results:
        for r in result:
            print(list(r))
        print(100*'*')
