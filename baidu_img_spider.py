#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re

import requests


class Downloader(object):
    @staticmethod
    def down_page(url):
        html = requests.get(url).text
        return html

    @staticmethod
    def down_pic(url):
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        return requests.get(url, headers=headers, stream=True, timeout=20).content


class UrlManager(object):
    def __init__(self):
        self.page_urls = set()

    def gen_urls(self, word, pages):
        for page in xrange(pages):
            url = self.__gen_url__(word, page)
            self.page_urls.add(url)

    def __gen_url__(self, word, page):
        return 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn=%s&gsm=3c&ct=&ic=0&lm=-1&width=0&height=0' % (
            word, page * 20)

    def has_new_url(self):
        return len(self.page_urls) > 0

    def get_craw_url(self):
        return self.page_urls.pop()


class Parser(object):
    def parse(self, html):
        return re.findall(r'objURL":"(.*?)"', html, re.S)


class Output(object):
    def __init__(self):
        self.result_dir = 'bdpics/girls/'
        self.__check_dir__(self.result_dir)

    def save(self, file_name, pic_content):
        with open(os.path.join(self.result_dir, file_name), 'wb') as result_file:
            result_file.write(pic_content)

    def __check_dir__(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def show(self):
        print "result dir: %s" % os.path.abspath(self.result_dir)


class Spider_Main(object):
    def __init__(self):
        self.urls = UrlManager()
        self.downloader = Downloader()
        self.parser = Parser()
        self.output = Output()

    def crawl(self, word, pages):
        self.__check_params__(word, pages)
        self.urls.gen_urls(word, pages)

        count = 0
        while self.urls.has_new_url():
            page_url = self.urls.get_craw_url()
            html = self.downloader.down_page(page_url)
            pic_urls = self.parser.parse(html)
            for pic_url in pic_urls:
                try:
                    count += 1
                    file_name = '%s_%s' % (count, pic_url[pic_url.rindex("/") + 1:])

                    pic_content = self.downloader.down_pic(pic_url)
                    self.output.save(file_name, pic_content)
                    print "crawl %s url=%s" % (count, pic_url)
                except Exception, e:
                    print "failed %s url=%s, e=%s" % (count, pic_url, e)

        self.output.show()

    @staticmethod
    def __check_params__(word, pages):
        if word is None:
            raise Exception('关键字不能为空')
        if pages <= 0:
            raise Exception('页数必须大于0')


if __name__ == '__main__':
    spider_main = Spider_Main()
    spider_main.crawl('美女', 20)
