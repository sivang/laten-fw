#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='laten',
      version='0.0.1',
      packages=find_packages(),
      scripts=[], 
      include_package_data = True,
      package_data = {
        '' : ['*.js','*.json'],
        }
    )


