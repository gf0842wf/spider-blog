# -*- coding: utf-8 -*-
from gevent.pool import Pool
from db import mondb
import gevent
import requests
import logging
import lxml.html
import time

logger = logging.getLogger(__name__)
now_date = lambda: time.strftime("%Y-%m-%d %X")


class BlogSpider(gevent.Greenlet):
    
    _headers = {}
    
    def __init__(self, **options):
        '''初始化配置
        : 必须配置: src, url, pool_size => _src, _url, _pool_size
        @param url: eg: 'http://www.oschina.net/search?q=python&scope=blog&sort_by_time=1&p=%s'
        '''
        names = ['src', 'url', 'pool_size']
        [setattr(self, '_%s' % name, options[name]) for name in names] 
        
        self._max_page = options.get('max_page') or 10000
        self._headers.update(options.get('headers', {}))
        self._pool = Pool(size=self._pool_size)
        self._handle = None
        
        gevent.Greenlet.__init__(self)
        
    def exist(self, link):
        '''数据库中是否存在该blog,根据blog的原链接
        @param link: 原链接
        '''
        return mondb.blog.find_one({'link':link}, {'_id':1}) is not None
    
    def page_n(self, n):
        url = self._url % (n,)
        try:
            r = requests.get(url, headers=self._headers, timeout=20)
        except:
            logger.warn('%s parse except', url, exc_info=1)
            return
        
        if r.status_code in [200, ]:
            return r
        
    def oschina_parse_page(self, r):
        '''解析oschina page
        '''
        assert r.encoding == 'UTF-8'
        
        try:
            html = lxml.html.fromstring(r.content)
            ul = html.xpath('//*[@id="results"]')
        except:
            logger.warn('ul xpath parse except', exc_info=1)
            raise StopIteration
        
        for li in ul[0]:
            try:
                link = li.find('h3/a').attrib['href']
                title = li.find('h3/a').text_content()
                summary = li.find('p[2]').text_content()
                date = li.find('p[3]').text_content().split()[0]
                author = li.find('p[3]/a').text_content()
            except:
                logger.warn('li xpath parse except', exc_info=1)
                raise StopIteration
            
            if self.exist(link):
                raise StopIteration
            
            yield (title, link, date, author, summary)
            
    def save(self, title, link, date, author, summary):
        blog = {'src':self._src,
                'title':title,
                'link':link,
                'date':date,
                'author':author,
                'summary':summary,
                'spider_date': now_date()
                }
        mondb.blog.insert(blog)
        
    def parse(self, i):
        r = self.page_n(i)
        if not r: return
        for title, link, date, author, summary in self._handle(r):
            logger.warn('insert to mongo title: %s', title)
            self.save(title, link, date, author, summary)
        
    def crawling(self):
        self._handle = getattr(self, '%s_parse_page' % self._src, None)
        assert self._handle is not None
        
        self._pool.map(self.parse, xrange(1, self._max_page + 1))
        
    def _run(self):
        self.crawling()
