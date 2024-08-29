from typing import Any, Iterable
from scrapy import Request
import scrapy
from scrapy.http import Response


class ArticleSpider(scrapy.Spider):
    name = 'article'

    def start_requests(self) -> Iterable[Request]:
        urls = [
            'https://pt.wikipedia.org'
        ]
        return [
            scrapy.Request(url=url, callback=self.parse)
            for url in urls
        ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        url = response.url
        title = response.css('h1').get()
        print(f'URL: {url}')
        print(f'Title is: {title}')
