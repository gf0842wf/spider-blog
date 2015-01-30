# -*- coding: utf-8 -*-
from pu.dictutil import DotOrderedDict
from pu.pattern.singleton import Singleton
import json


class Settings(DotOrderedDict):
    __metaclass__ = Singleton
    
    def load(self, filename):
        self.update(json.load(open(filename), encoding='utf-8'))


settings = Settings()
