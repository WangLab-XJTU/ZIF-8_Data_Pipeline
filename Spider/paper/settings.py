# Scrapy settings for paper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "paper"

SPIDER_MODULES = ["paper.spiders"]
NEWSPIDER_MODULE = "paper.spiders"

ADDONS = {}
LOG_LEVEL = 'INFO'
LOG_STDOUT = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "paper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "paper.middlewares.paperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "paper.middlewares.paperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "paper.pipelines.PaperPipeline": 300,
}

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
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}


TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,
    "args": ["--disable-blink-features=AutomationControlled"],
}

# 设置下载超时（防止过长等待）
DOWNLOAD_TIMEOUT = 60

ROBOTSTXT_OBEY = False  
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'

DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

#DEFAULT_REQUEST_HEADERS = '''_hjSessionUser_963544=eyJpZCI6IjI3ZTVlNzM5LTE1NzUtNWI0NC1iNTBjLWJiZWEzMzcxOWRlYyIsImNyZWF0ZWQiOjE2ODIxNjgwMzk0MjEsImV4aXN0aW5nIjp0cnVlfQ==; _scid=IxfbihP_VWdBTVfk9Obx7g8slwsRgANO; _scid_r=IxfbihP_VWdBTVfk9Obx7g8slwsRgANO; _fbp=fb.1.1760690407097.768749869725692117; _hjSessionUser_963557=eyJpZCI6IjUzNGI0N2U0LTQzZGUtNTgwMy05ZTI1LWVkOGExMDIzOWU3MiIsImNyZWF0ZWQiOjE3NjA2OTA0MTI0OTAsImV4aXN0aW5nIjp0cnVlfQ==; _sctr=1%7C1760630400000; _ga_4QGFJK49JC=GS2.1.s1760690396$o1$g1$t1760690421$j35$l0$h0; _ga_8GHCCRP65C=GS2.1.s1760690396$o1$g1$t1760690421$j35$l0$h0; _ga_K6PC4DQDZ2=GS2.1.s1760690396$o1$g1$t1760690421$j35$l0$h0; _ga=GA1.1.400581760.1727579866; ShowEUCookieLawBanner=true; _gcl_au=1.1.900938982.1765374762; _hjSessionUser_889812=eyJpZCI6ImJlMmZhMWVhLTQyYzktNTZlMi05YWYyLWI0NmJhOWZmZWVlNCIsImNyZWF0ZWQiOjE3NjcyNjk5NzczOTQsImV4aXN0aW5nIjp0cnVlfQ==; FPID=FPID2.2.IuKzpN5AOr0k5JrMXdvumushpbJE3b7d4Ifmze%2Fbijg%3D.1727579866; FPLC=lZgBynDPlJVs7OP0DKCBQZktiCg5zCbSYT9t%2Ftmq3fiXf%2BhHaRyzal1wwh2KnCBQeGQ2ApffRnc5Ckh6A67JSGkhrDw1k3I92C5Nqiju0pFZHDDeihhamc4pJty%2Fiw%3D%3D; _hjSessionUser_5351232=eyJpZCI6IjYwZDg1ODQyLTdiNTUtNTY2My1hYzk5LWZlYjY5YzE3NTM4NCIsImNyZWF0ZWQiOjE3NzI1MDQyOTYzNTMsImV4aXN0aW5nIjp0cnVlfQ==; _ga_PVQCCFLVYE=GS2.1.s1772504268$o1$g1$t1772505590$j55$l0$h0; X-Mapping-hhmaobcf=7C65C30FD9034420CA236A385407D6BA; _PubsBFCleared=1; ASP.NET_SessionId=kanrouthdrtgubrpwwqhcr5f; _hjSession_963544=eyJpZCI6IjFkMGMzM2M4LTg0OTUtNDU2ZS1iMTVmLTBlMGRmZTA4MmZmOSIsImMiOjE3NzI1MzgwNTkzNDgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; Branding=; __gads=ID=5d76fdbd6b41bc2d:T=1772538212:RT=1772538212:S=ALNI_MZSUmPYfjlH0jJrPf82mvbUXudJyQ; __gpi=UID=000013998940cc7f:T=1772538212:RT=1772538212:S=ALNI_MbFlGcB099O7dM5nokWXO2b1g_5kA; __utma=1.400581760.1727579866.1772538276.1772538276.1; __utmc=1; __utmz=1.1772538276.1.1.utmcsr=pubs.rsc.org|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; _hjSession_889812=eyJpZCI6ImEyZWRiODU4LTU0OTQtNDA0MS1hMTUyLTE1OWVhZjhjN2QxNiIsImMiOjE3NzI1MzgzMzI0MjUsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ga_6EG9J24D2G=GS2.1.s1772538325$o4$g0$t1772538335$j50$l0$h1668977312; _ga_80NWSXBN84=GS2.1.s1772538325$o2$g0$t1772538335$j50$l0$h1944962906; ApplicationCheckAccessCookie=PD94bWwgdmVyc2lvbj0iMS4wIj8+DQo8Q2hlY2tBY2Nlc3MgeG1sbnM6eHNkPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYSIgeG1sbnM6eHNpPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSI+DQogIDxEb2N1bWVudFR5cGU+QWxsPC9Eb2N1bWVudFR5cGU+DQogIDxKb3VybmFsQ29kZT5DQzwvSm91cm5hbENvZGU+DQogIDxZZWFyPjIwMjA8L1llYXI+DQogIDxET0k+YzljYzA4NzI0YTwvRE9JPg0KICA8Vm9sdW1lPjU2PC9Wb2x1bWU+DQogIDxJc3N1ZUlEPjE5PC9Jc3N1ZUlEPg0KICA8Q29udGVudFR5cGU+QXJ0aWNsZTwvQ29udGVudFR5cGU+DQogIDxQdWJsaWNhdGlvbkRhdGU+MjAyMC0wMS0yN1QwMDowMDowMDwvUHVibGljYXRpb25EYXRlPg0KICA8SXNJUFJlY29nbmlzZWQ+ZmFsc2U8L0lzSVBSZWNvZ25pc2VkPg0KICA8VXNlckxvZ2dlZEluPmZhbHNlPC9Vc2VyTG9nZ2VkSW4+DQogIDxDdXN0b21UYWdzIC8+DQogIDxJc0F1dGhlbnRpY2F0ZWQ+ZmFsc2U8L0lzQXV0aGVudGljYXRlZD4NCiAgPElzTW9iaWxlQXBwPmZhbHNlPC9Jc01vYmlsZUFwcD4NCiAgPElzRG93bmxvYWQ+ZmFsc2U8L0lzRG93bmxvYWQ+DQogIDxQbGF0Zm9ybUlEPjFDNTc2OTYyLUI5OTQtNDEzOS1BMTg2LTgxMjA0MzNCRTdCNzwvUGxhdGZvcm1JRD4NCiAgPElzQ29udGVudEFjY2Vzc2libGU+ZmFsc2U8L0lzQ29udGVudEFjY2Vzc2libGU+DQo8L0NoZWNrQWNjZXNzPg==; __utmb=1.2.10.1772538276; EPLATFORMURL=https%3a%2f%2fpubs.rsc.org%2fen%2fcontent%2farticlelanding%2f2020%2fcc%2fc9cc08724a|1c576962-b994-4139-a186-8120433be7b7; _ga_T8TQNW372Z=GS2.1.s1772538276$o1$g1$t1772538388$j18$l0$h0; AuthSystemSessionId=7c8669fd-b3bd-4dab-aa6d-6b758c90779e; Branding=50003390; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Mar+03+2026+19%3A46%3A34+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202409.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=733346b1-e916-4e41-a7ec-e5922a2bb66f&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=CN%3BJL; OptanonAlertBoxClosed=2026-03-03T11:46:34.076Z; __eoi=ID=a0cc62743a5a1f1a:T=1760690401:RT=1772538393:S=AA-AfjaBHNhhMnRV0BPbkY5U7-Z6; _ga_MGLMJ78PFV=GS2.1.s1772538059$o84$g1$t1772538558$j60$l0$h0'''

PLAYWRIGHT_CONTEXTS = {
    "logged_in": {
        "storage_state": "auth_state.json", 
    },
}

DOWNLOADER_MIDDLEWARES = {
    'paper.middlewares.RSCLoginMiddleware': 543, 
}

LOG_FILE = 'Full_Scrapy.log'

#JOBDIR = '20260308'


DOWNLOAD_DELAY = 10
RANDOMIZE_DOWNLOAD_DELAY = True

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 6000000