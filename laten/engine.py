#!/usr/bin/env python

import os
import time
import requests
from datetime import datetime
from datetime import timedelta
from laten.configregistry import Configuration
from dateutil.parser import isoparse
from laten.utils import remote_debug
from copy import deepcopy
import yaml


class EngineApi(object):
    """
    The rule engine class, exposing the engine API.
    Everything needed to do content validation should be
    put in this class as per the existing code.

    Example use:

    api = EngineApi()
    ruleset = [('ensure-content', "I'm feeling lucky"), 
                    ('ensure-content', "Copyright")]
    r = requests.get('https://www.google.com')
    r.raise_for_status()
    content = r.content
    print (api.ensure_rules(content, ruleset))

    """
    def __init__(self):
        """
        Loads persistant configuration into
        memory.
        """
        self.config = Configuration()

    def ensure_content(self, buff, tofind):
        """
        Rule to make sure a buffer contains a certain
        byte stream.

        Recieves:
            buff - byte stream to search in
            content - byte string of desire content
        """
        result = True
        try:
            result = buff.index(bytearray(tofind, 'UTF-8')) >=0
        except ValueError:
            result = False
        except Exception as e:
            raise e
            
        return result


    def _call_rule(self, rule_name, *args):
        func_name = rule_name.replace('-', '_')
        return getattr(self, func_name)(*args)

    def ensure_rules(self, content, ruleset = None ):
        remote_debug()
        rules = None
        if not ruleset:
            rules = self.config.default_rules
        else:
            rules = ruleset

        print (rules)

        test_pass = []
        for r in rules:
            r_id = list(r.keys())[0]
            test_pass.append(self._call_rule(r_id, content, r[r_id]))

        result = False in test_pass and False or True
        return result

    def load_url_set(self, abs_path=None):
        path = abs_path or self.config.urls_registry_path
        content = None
        with open(path) as y_file:
            content = y_file.read()
        url_conf = yaml.safe_load(content)
        return url_conf

def test_run():
    api = EngineApi()
    ruleset = [('ensure-content', "I'm feeling lucky"), 
                    ('ensure-content', "Copyright")]
    r = requests.get('https://www.google.com')
    r.raise_for_status()
    content = r.content
    print (api.ensure_rules(content, ruleset))

    print ( api.load_url_set() )


if __name__ == "__main__":
    test_run()
    

