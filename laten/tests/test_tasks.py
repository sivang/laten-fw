# -*- coding: utf-8 -*-

import os
import requests
import sys
import random
import json
import yaml
import string
import inspect
import pytest
import logging.config



here = os.path.dirname(__file__)
result_dump = False

def file_dump(buf):
    """
        Magical function that knows to send test
        results into an output file by respective
        name of the test, including 'httpcode' &
        'agentcode' if thus supplied.

        'buf'- stream content to be recorded in file.
    """
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    caller = calframe[1][3]
    file_name = "./results/" + caller 
    file_name += ".result.json"
    with open(file_name, 'w') as f:
        f.write(str(buf))

def test_monitor():
    
    urls = {
    }

    from bson.objectid import ObjectId
    from pymongo import MongoClient
    client = MongoClient()
    file_dump(results)

