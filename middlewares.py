# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy_douban.settings import PROXIES
from scrapy_douban.settings import USER_AGENTS
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
# class ScrapyDoubanSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.

#         # Should return None or raise an exception.
#         return None

#     def process_spider_output(response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.

#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i

#     def process_spider_exception(response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.

#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         return None

#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.

#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#         # user_agent = random.choice(USER_AGENTS)
#         # start_requests.headers.setdefault('User-Agent',user_agent)
#         # proxy = random.choice(PROXIES)
#         # start_requests.meta['proxy'] = "http://%s" % proxy['ip_port']

    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        if user_agent:
            request.headers.setdefault('User-Agent',user_agent)
        # proxy = random.choice(PROXIES)
        # if proxy:
        #     request.meta['proxy'] = "http://%s" % proxy['ip_port']