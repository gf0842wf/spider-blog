# -*- coding: utf-8 -*-
class Singleton(type):
    '''Singleton Metaclass
    用法:
    class MyClass:
        __metaclass__ = Singleton
        
    one = MyClass()
    two = MyClass()
    
    print id(one) == id(two)
    # result: True
    '''
    
    def __init__(self, name, bases, dic):
        super(Singleton, self).__init__(name, bases, dic)
        self._instance = None
        
    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(Singleton, self).__call__(*args, **kwargs)
        return self._instance


class Singleton2(object):
    '''单例模式
    用法:
        class MyClass(Singleton):
            a = 1
            
        one = MyClass()
        two = MyClass()
        
        print id(one) == id(two)
        # result: True
    用途:
    用单例类ShareObject/GlobalObject 来代替 share.py&settings.py 存储全局变量&全局配置
    '''
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'): 
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw) # 调用父类的__new__方法生成实例
            
        return cls._instance