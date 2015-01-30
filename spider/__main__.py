# -*- coding: utf-8 -*-
# from path import init_path;init_path()
import sys; sys.modules.pop('threading', None)
from gevent import monkey; monkey.patch_all()

import argparse
import gevent
import os
import logging

from settings import settings
from path import HOME_DIR

# 分析参数
ARGS = argparse.ArgumentParser(description='blog spider')

ARGS.add_argument(
    '--logfile', '-l', action='store', dest='logfile',
    default='-', type=str, help="logfile, '-' means stdout.")

ARGS.add_argument(
    '--loglevel', '-L', action='store', dest='loglevel',
    default='WARN', type=str, help='log level(DEBUG, INFO, WARN, ERROR).')

ARGS.add_argument(
    '--settings', '-s', action='store', dest='settings',
    default='etc/blog/default.json', type=str, help='setting file.')

ARGS = ARGS.parse_args()

def initialize():
    # 加载配置文件
    settings.load(os.path.join(HOME_DIR, ARGS.settings))
    
    loglevel = logging._checkLevel(ARGS.loglevel)
    
    # 日志配置
    log_format = '[%(asctime)-15s %(levelname)s:%(name)s:%(module)s] %(message)s'
    logging.basicConfig(level=loglevel, format=log_format)

def run():
    from spider import BlogSpider
    
    optionses = settings['BLOGS']
    for options in optionses:
        bs = BlogSpider(**options)
        bs.start()
    
    gevent.wait()
    
def main():
    initialize()
    run()

main()

gevent.wait()

# cd spider-blog
# python spider --loglevel WARN --settings etc/blog/default.json
