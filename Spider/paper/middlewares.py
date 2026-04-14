# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AcsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # matching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AcsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


import subprocess
from scrapy.http import HtmlResponse
from twisted.internet.error import TimeoutError as TwistedTimeoutError

class RSCLoginMiddleware:
    def __init__(self, auth_path):
        self.auth_path = auth_path
        self.is_logging_in = False

    @classmethod
    def from_crawler(cls, crawler):
        return cls(auth_path=crawler.settings.get("RSC_AUTH_PATH", "auth_state.json"))

    def _trigger_re_login(self, spider):
        """trigger Login"""
        if not self.is_logging_in:
            self.is_logging_in = True
            spider.logger.warning("RSC Login Check failure")
            try:
                
                subprocess.run(["python", "rsc_login.py"], check=True)
                spider.logger.info("Login Status refresh")
            except Exception as e:
                spider.logger.error(f"rcr_login.py: {e}")
            finally:
                self.is_logging_in = False
                

    def process_response(self, request, response, spider):
        
        page = request.meta.get("playwright_page")
        
        if not request.meta.get("check_login"):
            return response

        
        is_logged_in = response.css("#divWelcomeUser").get() is not None
        
        if not is_logged_in:
            self._trigger_re_login(spider,request)
                          

            new_request = request.copy()
            new_request.dont_filter = True
            return new_request

        return response

    def process_exception(self, request, exception, spider):
        
        if request.meta.get("check_login"):
            spider.logger.error(f"Error: {exception}")
            self._trigger_re_login(spider)
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        return None