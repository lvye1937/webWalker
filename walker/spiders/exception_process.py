# -*- coding:utf-8 -*-
import traceback
from functools import wraps

from scrapy.exceptions import IgnoreRequest

from utils import get_ip_address


IP = get_ip_address()


def stats_wrapper(func):

    @wraps(func)
    def wrapper_method(*args, **kwds):

        try:
            return func(*args, **kwds)
        except Exception:
            traceback.print_exc()

    return wrapper_method


def parse_method_wrapper(func):

    @wraps(func)
    def wrapper_method(*args, **kwds):

        try:
            return func(*args, **kwds)
        except Exception:
            self = args[0]

            response = args[1]
            msg = "error heppened in %s method. Error:%s"%(func.__name__, traceback.format_exc())
            self.logger.error(msg)
            self.crawler.stats.set_failed_download(response.meta, "%s \n heppened in %s of %s"%(traceback.format_exc(), func.__name__, IP))

    return wrapper_method


def parse_next_method_wrapper(func):

    @wraps(func)
    def wrapper_method(*args, **kwds):
        self = args[0]
        response = args[1]
        k = response.meta.get("next_key", "unknow")

        try:
            return func(*args, **kwds)
        except Exception:
            msg = "error heppened in %s method. Error:%s"%(func.__name__, traceback.format_exc())
            self.logger.error(msg)
            item = response.meta.get("item_half", {})
            self.crawler.stats.set_failed_download(
                response.meta, "%s \n heppened in %s of %s product_id: %s," %
                (traceback.format_exc(), func.__name__, IP, item.get("product_id", "unknow"), ),
                k)

    return wrapper_method


def next_request_method_wrapper(func):
    @wraps(func)
    def wrapper_method(*args, **kwds):
        try:
            return func(*args, **kwds)
        except Exception:
            self = args[0]
            msg = "error heppened in %s method. Error:%s" % (func.__name__, traceback.format_exc())
            self.logger.error(msg)

            if self.present_item:
                meta = self.present_item["meta"] if self.present_item.get("meta") else self.present_item
            else:
                meta = {"crawlid": "next_request_unknow", "url": "unknow"}

            if meta.get("callback") == "parse":
                self.spider.crawler.stats.inc_total_pages(crawlid=meta['crawlid'])

            self.spider.crawler.stats.set_failed_download(meta, "%s \n heppened in %s of %s" % (
            traceback.format_exc(), func.__name__, IP))

    return wrapper_method


def enqueue_request_method_wrapper(func):
    @wraps(func)
    def wrapper_method(*args, **kwds):
        try:
            return func(*args, **kwds)
        except Exception:
            self = args[0]
            request = args[1]
            if request.meta.get("callback") == "parse":
                self.spider.crawler.stats.inc_total_pages(crawlid=request.meta['crawlid'])
            msg = "error heppened in %s method of %s. Error:%s"%(func.__name__, IP, traceback.format_exc())
            self.spider.crawler.stats.set_failed_download(request.meta, "%s \n heppened in %s of %s" % (
                traceback.format_exc(), func.__name__, IP))
            self.logger.error(msg)

    return wrapper_method


def process_requset_method_wrapper(func):

    @wraps(func)
    def wrapper_method(*args, **kwds):

        self = args[0]
        request = kwds.get("request")
        spider = kwds.get("spider")

        try:
            return func(*args, **kwds)
        except Exception, e:
            spider.logger.error("error heppened in process_request method of %s in %s. Error:%s, processing %s," % (
            self.__class__.__name__, IP, traceback.format_exc(), request.url))
            spider.crawler.stats.set_failed_download(request.meta, str(e))
            raise IgnoreRequest(e)

    return wrapper_method


def process_response_method_wrapper(func):

    @wraps(func)
    def wrapper_method(*args, **kwds):

        self = args[0]
        request = kwds.get("request")
        response = kwds.get("response")
        spider = kwds.get("spider")

        try:
            return func(*args, **kwds)
        except Exception, e:
            spider.logger.error("error heppened in process_response method of %s in %s. Error:%s, processing %s," % (
                self.__class__.__name__, IP, traceback.format_exc(), response.url))
            spider.crawler.stats.set_failed_download(request.meta, str(e))
            raise IgnoreRequest(e)

    return wrapper_method


def process_exception_method_wrapper(func):

    @wraps(func)
    def wrapper_method(*args, **kwds):
        self = args[0]
        request = kwds.get("request")
        exception = kwds.get("exception")
        spider = kwds.get("spider")

        try:
            return func(*args, **kwds)
        except Exception, e:
            spider.logger.error("error heppened in process_exception method of %s in %s, deal with exception %s. Error:%s, processing %s," % (
                self.__class__.__name__, IP, "%s:%s"%(exception.__class__.__name__, exception), traceback.format_exc(), request.url))

            if isinstance(e, IgnoreRequest):
                spider.crawler.stats.set_failed_download(request.meta, str(e))
            raise IgnoreRequest(e)

    return wrapper_method


