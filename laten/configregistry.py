""""
This modules holds manages persistent configuration
and related settings for Laten.
"""
from datetime import timedelta
from datetime import datetime

CONFIGURATION = {
    # The interval at which to test URLs 
    # in minutes.
    'SAMPLE_INTERVAL' : 5,
    'REMOTE_DEBUG' : False,
    'URLS_REGISTRY_PATH' : "/home/ubuntu/laten-fw/laten/urls.yaml",
    'TASK_TIMEOUT' : 1200,
}


CONFIG_DB = 'CONFIGURATIONS'

from pymongo import MongoClient

class Configuration(object):
    """
    Sivan's "micro-orm"
    
    Micro-orms are Python classes that can persist onto a DB of choice,
    but without hooking into Python object's own setter / getter mechanism.

    It requires to indicate that a value is to be persisted, using .save()

    Example use:
      from configregistry import Configuration
      c = Configuration()
      c.my_value = 12
      c.save()
    """
    def __init__(self, url=None):
        self.config = None
        client = None
        if url:
            client = MongoClient(url)
        else:
            client = MongoClient()
        self.client = client
        self.db = getattr(self.client, CONFIG_DB)
        self.reload()

    def reload(self):
        self.laten_config = self.db.laten_config
        self.config = self.laten_config.find_one()
        if not self.config:
            self.laten_config.insert_one(CONFIGURATION)
            self.config = CONFIGURATION
        for k, v in self.config.items():
            if k!='name':
                setattr(self, k.lower(), v)


    def save(self):
        self.clear()
        new_config = {
                    k.upper(): v for k,v in self.__dict__.items() 
                        if k.upper() in self.config } 
        self.laten_config.insert_one(new_config)

    def clear(self):
        self.laten_config = self.db.laten_config
        self.config = self.laten_config.find_one()
        from bson.objectid import ObjectId
        self.laten_config.delete_one({'_id' : ObjectId(self.config['_id'])})
            

