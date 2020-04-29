# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from items import Book
import requests
import json
from fake_useragent import UserAgent


class BookCrawlerSpider(CrawlSpider):
    name = 'springer_crawler'
    allowed_domains = ["springer.com",]

    start_urls = [
        get_project_settings().get('START_URL'),
    ]

    def start_requests(self):
        for i,url in enumerate(self.start_urls):
            yield self.build_request(url)

    def parse_page(self, response):
        sel = Selector(response)
        base_url = get_project_settings().get('BASE_URL')
        books_card = sel.css('.has-cover')
        for book_card in books_card.getall():
            book_card_sel = Selector(text=book_card)
            book_title = book_card_sel.css('.text').xpath('//h2/a/text()').get()
            book_subtitle = book_card_sel.css('.text').css('.subtitle').get()
            book_subtitle_sel = Selector(text=book_subtitle)
            book_subtitle = book_subtitle_sel.xpath('//p/text()').get()
            book_url = book_card_sel.css('.text').xpath('//h2').css('a::attr(href)').get()
            book_url = f'{base_url}{book_url}'
            # print(book_url)
            # print(book_title)
            # print(book_subtitle)
            # print('-----------------------------')
            book = Book(title=book_title, subtitle=book_subtitle, url=book_url)
            yield self.build_request_detail(f'{book_url}#about', book)

        next_pages = sel.css('.next')
        for next_page in next_pages:
            if next_page.css('a::attr(title)').get() == 'next':
                next_page_url = response.urljoin(next_page.css('a::attr(href)').get())
                yield self.build_request(next_page_url)

    def parse_book_detail(self, response, book):
        sel = Selector(response)
        # book_desriptions = {}
        book_details = sel.css('.evaluation-section').getall()
        for book_detail in book_details:
            description_sel = Selector(text=book_detail)
            book_metrics = description_sel.css('.evaluation-section__text-col').xpath('//div/div/ul[@id="book-metrics"]').get()
            # print(book_metrics)
            book_metrics_sel = Selector(text=book_metrics)
            book_metrics_items = book_metrics_sel.css('.article-metrics__item').getall()
            for book_metrics_item in book_metrics_items:
                book_metric_sel = Selector(text=book_metrics_item)
                view_label = book_metric_sel.xpath('//span/text()').getall()
                if view_label[1] == 'Downloads':
                    book_downloads = view_label[0]
                    # print(book_downloads)

        person_list = sel.css('.authors__name').getall()
        book_authors = []
        for person in person_list:
            person_sel = Selector(text=person)
            book_authors.append(person_sel.xpath('//span/text()').get())
            # print(person)

        image_url = sel.css('.test-cover-image').css('img').attrib['src']
        
        book['image'] = image_url
        book['authors'] = book_authors
        book['downloads'] = book_downloads

        book_description = sel.xpath('//div[@id="book-description"]/div/text()').get()
        book['introduction'] = book_description

        book_keywords_all = sel.css('.Keyword').getall()
        book_keywords = []
        for book_keyword in book_keywords_all:
            book_keyword_sel = Selector(text=book_keyword)
            book_keywords.append(book_keyword_sel.xpath('//span/text()').get())
        book['keywords'] = book_keywords

        book_link_download = sel.css('.test-bookpdf-link').css('a::attr(href)').get()
        base_url = get_project_settings().get('BASE_URL')
        book_link_download = f'{base_url}{book_link_download}'
        book['download_url'] = book_link_download

        # book['doi'] = book_doi
        # book['copy_right'] = book_copy_right
        # book['publisher'] = book_publisher
        # book['packages'] = book_packages

        yield book
            
    def build_request(self, url):
        headers = {
            'User-Agent': UserAgent().random
        }
        return Request(
            url,
            callback=self.parse_page,
            headers=headers
        )

    def build_request_detail(self, url, book):
        headers = {
            'User-Agent': UserAgent().random
        }
        return Request(
            url,
            callback=self.parse_book_detail,
            headers=headers,
            cb_kwargs=dict(book=book)
        )
