# Scrapy settings for crawljobdata project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawljobdata'

SPIDER_MODULES = ['crawljobdata.spiders']
NEWSPIDER_MODULE = 'crawljobdata.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

PROXY_POOL_ENABLED = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawljobdata.middlewares.CrawljobdataSpiderMiddleware': 543,
#}


ROTATING_PROXY_LIST = [
    'proxy1.com:8000',
    'proxy2.com:8031',
    # ...
]
DOWNLOADER_MIDDLEWARES = {
    # ...
    'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    # ...
}
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#     'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
#     'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
# }
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400
}
SER_AGENT_LIST = "./user-agent.txt"
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
# }
# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
# })

# USER_AGENTS = [
#     ('Mozilla/5.0 (X11; Linux x86_64) '
#      'AppleWebKit/537.36 (KHTML, like Gecko) '
#      'Chrome/57.0.2987.110 '
#      'Safari/537.36'),  # chrome
#     ('Mozilla/5.0 (X11; Linux x86_64) '
#      'AppleWebKit/537.36 (KHTML, like Gecko) '
#      'Chrome/61.0.3163.79 '
#      'Safari/537.36'),  # chrome
#     ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
#      'Gecko/20100101 '
#      'Firefox/55.0')  # firefox
# ]
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawljobdata.middlewares.CrawljobdataDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'crawljobdata.middlewares.TooManyRequestsRetryMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'crawljobdata.pipelines.CrawljobdataPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
FEED_EXPORT_ENCODING = 'utf-8'