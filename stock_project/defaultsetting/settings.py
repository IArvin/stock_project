# -*-coding:utf-8-*-
import ConfigParser
import os
import sys
import logging
import threading


DATABASE_LOCK = threading.Lock()


class defaultSettings():
    def __init__(self):
        pass


class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


class globalSetting(SingletonMixin):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')
        self.gearman_server_url = cf.get("baseconf", "gearmanserver")
        logging.info('Global setting init complete')
