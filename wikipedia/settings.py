# Scrapy settings for wikipedia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = "wikipedia"

SPIDER_MODULES = ["wikipedia.spiders"]
NEWSPIDER_MODULE = "wikipedia.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "wikipedia (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "wikipedia.middlewares.WikipediaSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "wikipedia.middlewares.WikipediaDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "wikipedia.pipelines.WikipediaPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# ------------------------------------------- Custom Settings -----------------

import csv

ROBOTSTXT_OBEY = False  # 禁用robots.txt
HTTPERROR_ALLOWED_CODES = [404]  # 捕捉不存在的词条

# 日志设置
LOG_LEVEL = 'INFO'  # 日志等级
LOGSTATS_INTERVAL = 15  # 爬取速度显示间隔

# 输入csv。包含一列name
IMPORT_CSV = r'for_wikipedia.csv'

# 输出xlsx。完整路径。
# 包含name, result, url三列。name来自输入csv， result在词条存在时为词条提取结果，不存在时为None， url为网址。
EXPORT_XLSX = r'from_wikipedia_result.xlsx'

# 爬取csv前N条, None则为全部。用于测试
IMPORT_CSV_N_ITEMS = None

# 定义词条提取方法
def extract_full_text(response):
    return ''.join(response.css('#bodyContent *:not(style)::text').getall())
def extract_first_paragraph_text(response):
    return ''.join(response.css('div.mw-parser-output > p:not(.mw-empty-elt)')[0].css('*::text').getall())

# 设置词条提取方法
EXTRACT_RESULT_TEXT_FUNC = extract_first_paragraph_text

# 结果备份
FEEDS = {
    'backup_results.jl': {
        'format': 'jsonlines',
        'encoding': 'utf8',
    }
}
