#!/usr/bin/env python


from celery import Celery
import celery
from celery.utils.log import get_task_logger
import os
import time
from pymongo import MongoClient
import gridfs
from datetime import datetime
import sys
from dateutil.parser import isoparse

from laten.configregistry import Configuration
from laten.utils import whoami, remote_debug
from laten.engine import EngineApi

app = Celery('LATEN',
        broker="pyamqp://guest@localhost//")

app.config_from_object('laten.celeryconfig')

logger = get_task_logger(__name__)



@app.task(bind=True)
def test_url(self, name, url, rules):
    """
    Requests an URL, measure the response time, and optionally
    test the received response against the ruleset.

    receives:
        rules = [(action, expected_output), ......., ]
    
    saves result to data store:
        { 'url' : "https://example.com",
          'total_time' : request_elapsed_time,
          'ruleset' : [....(action, expected_output)...],
          'done_at' : a_timestamp }

    """
    import requests
    client = MongoClient()
    api = EngineApi()
    response = requests.get(url)
    content_status = api.ensure_rules(response.content, rules)
    elapsed_time_secs = response.elapsed.total_seconds()

    logger.info(
        'Checked {} , time: {}s, content status: {}, HTTP: {} {}'.format(
                url,
                elapsed_time_secs,
                content_status,
                response.status_code,
                response.reason,

            )
        )

    processing = client.processing
    url_results = processing.url_results
    result_document = {
        'name' : name,
        'url ' : url,
        'total_time_secs' : elapsed_time_secs,
        'ruleset' : rules,
        'content_status' : content_status,
        'http_code' : response.status_code,
        'http_reason' : response.reason,
        'done_at' : datetime.now(),
        }

    processing = client.processing
    results = processing.results
    object_id = results.insert_one(result_document).inserted_id
    
    return { 'task' : whoami(), 'result_id' : str(object_id),}




@app.task(bind=True)
def test_multiple(self, _id):
    """
    Received an MongoDB object_id of a batch job document
    and dispatches respective `test_url` tasks that sample
    individual URLs.
    """
    client = MongoClient()
    urls_to_test = client.processing.urls_to_test
    processing = client.processing
    pending = processing.pending
    
    from bson.objectid import ObjectId
    job = urls_to_test.find_one({'_id' : ObjectId(_id)})

    import pprint

    logger.info("Preparing batch: {}".format(job))

    url_batch = job['url_batch']
    count = len(url_batch)
    for check in url_batch:
        logger.info('Dispatching check of {} , URL: {}.'.format(check['name'], check['url']))
        test_url.delay(name=check['name'], 
                        url=check['url'], 
                        rules=check['rules'])

    return { "whoami" : whoami() , "dispatched" : count }




@app.task( bind=True)
def check_urls(self):
    """
    Reads URLs batch to process from configuration file
    and prepares a test batch.
    """
    config = Configuration()
    client = MongoClient()
    api = EngineApi()

    logger.info('Loading URL set from {}.'.format(config.urls_registry_path))
    url_batch = api.load_url_set()


    job_document = {'url_batch' : url_batch,
                'batch' : True, 
                'default_ruleset' : config.default_ruleset,
                'timestamp'  : datetime.now()}

    urls_to_test = client.processing.urls_to_test

    object_id = urls_to_test.insert_one(job_document).inserted_id
    test_multiple.delay(str(object_id))

    del api
    del urls_to_test
    del job_document

    return { 'task' : whoami(), 'url_set' : str(object_id),}

 
 

