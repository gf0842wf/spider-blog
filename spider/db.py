# -*- coding: utf-8 -*-
from copy import deepcopy
from settings import settings
import pymongo

monconf = deepcopy(settings['MONGO'])
db = monconf.pop('db')
monconf['host'] = str(monconf['host'])
mondb = pymongo.MongoClient(use_greenlets=True, **monconf)[db]
