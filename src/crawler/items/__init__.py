# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class Book(Item):
    title = Field()
    subtitle = Field()
    authors = Field()
    packages = Field()
    image = Field()
    introduction = Field()
    keywords = Field()
    doi = Field()
    publisher = Field()
    copyright_info = Field()
    downloads = Field()
    file_name = Field()
    url = Field()
    download_url = Field()
    