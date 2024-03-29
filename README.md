Laten Micro Web Monitor Copyright (c) 2018-2023 Sivan Grünberg <sivan@vitakka.co>

Laten is released under the MIT license.

Laten:

    - A minimalistic, "micro" web site monitor implemented with Celery, RabbitMQ and MongoDB.
    - Minimalistically coded as well.
    - Production Ready.
    - Can be used 'out of the box', as;
    - it included an Ansible recipe you can use right away on your public cloud infrastructure.
    - Has a neatly, customizable,  pythonic content validation rule engine.
    - Exploits Python's dynamic nature.
    - Uses Python3.5 and above.


laten (Verb)

    - (copulative) to leave, to cause to remain in the same position or state
        - Ze lieten het zo.
    - (auxiliary, with object) to leave, to allow to remain/continue to
        - Laat dat daar maar liggen.
    - Just leave it lying there. (auxiliary, with object) to let, to allow to
        - Ze lieten hem gaan.

Laten is a very simpe web site monitor that uses Celery for distributing workload across nodes, MongoDB for flexible logging
and relies on systemd to become a daemon service.

Laten will take a list of urls and content validation rules, defined in a yaml file, load it into its MongoDB persistant storage,
and start periodically sample the list of URLs and matching content validation rules accumulating results in MongoDB for easy 
retrival, map-reduce, analytics, statistics and other delights.


```
git clone https://github.com/sivang/laten.git

Then, use ansible to install to a server:

ansible-playbook laten/laten/deployment/laten-server.yaml --user=ubuntu --extra-vars "ansible_sudo_pass=$PASSWORD" 

```

To configure, either use a mongodb gui client and navigate to the CONFIGURATIONS database (self explantory) or:

```
sudo su - celery 
. laten-venv/bin/activate
(laten-venv) celery@ip-172-31-16-94:~$ ipython
Python 3.5.2 (default, Nov 23 2017, 16:37:01) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.3.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from laten.configregistry import Configuration

In [2]: c = Configuration()

In [4]: c.config
Out[4]: 
{'DEFAULT_RULESET': [[None]],
    'REMOTE_DEBUG': False,
    'SAMPLE_INTERVAL': 5,
    'TASK_TIMEOUT': 1200,
    'URLS_REGISTRY_PATH': '/home/ubuntu/laten/urls.yaml',
    '_id': ObjectId('5b807a7eb14877445504eef7')}

In [5]: c.sample_interval = 3

In [6]: c.save()


sudo systemctl restart celery.service 

```

And that's it, you can now either check logs for progress or the MongoDB processing.results collection for perodic URL sample results.

```
(laten-venv)$ tail -f log/celery.service.log

```
MongoDB:

```
(ten-venv) celery@ip-172-31-16-94:~$ mongo
MongoDB shell version: 2.6.10
connecting to: test
> use processing
switched to db processing
> db.results.find()
(laten-venv) celery@ip-172-31-16-94:~$ mongo
MongoDB shell version: 2.6.10
connecting to: test
> use processing
switched to db processing
> db.results.find()
.....
.....
..
.
```




