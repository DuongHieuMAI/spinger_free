# -*- coding: utf-8 -*-
import os
from distutils.util import strtobool

from dotenv import load_dotenv


load_dotenv()

BOT_NAME = "Book_Crawler"

SPIDER_MODULES = ["spiders"]
NEWSPIDER_MODULE = "spiders"
COMMANDS_MODULE = "commands"

START_URL = os.getenv("START_URL", "")
BASE_URL = os.getenv("BASE_URL", "")

PROXY = os.getenv("PROXY", "")
PROXY_AUTH = os.getenv("PROXY_AUTH", "")
PROXY_ENABLED = os.getenv("PROXY_ENABLED", False)
if isinstance(PROXY_ENABLED, str):
    PROXY_ENABLED = False if PROXY_ENABLED == 'False' else True

COOKIES_JAR = ""

CONCURRENT_REQUESTS = os.getenv("CONCURRENT_REQUESTS", 16)
CONCURRENT_REQUESTS_PER_DOMAIN = os.getenv("CONCURRENT_REQUESTS_PER_DOMAIN", 8)
DOWNLOAD_DELAY = os.getenv("DOWNLOAD_DELAY", 0)
DOWNLOAD_TIMEOUT = os.getenv("DOWNLOAD_TIMEOUT", 180)

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True

TELNETCONSOLE_ENABLED = False
TELNETCONSOLE_PASSWORD = "password"

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "max-age=0",
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": None,
    "middlewares.HttpProxyMiddleware": 543,
    "middlewares.LogErrorsMiddleware": 550,
}

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FILE = os.getenv("LOG_FILE") if os.getenv("LOG_FILE", "") else None

ITEM_PIPELINES = {
    'pipelines.MongoPipeline': 300,
}

MONGO_URI = os.getenv("MONGO_URI")

PIKA_LOG_LEVEL = os.getenv("PIKA_LOG_LEVEL", "WARN")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
RABBITMQ_VIRTUAL_HOST = os.getenv("RABBITMQ_VIRTUAL_HOST", "guest")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "/")

try:
    HTTPCACHE_ENABLED = strtobool(os.getenv("HTTPCACHE_ENABLED", "False"))
except ValueError:
    HTTPCACHE_ENABLED = False

HTTPCACHE_IGNORE_HTTP_CODES = list(
    map(int, (s for s in os.getenv("HTTPCACHE_IGNORE_HTTP_CODES", "").split(",") if s))
)
