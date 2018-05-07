#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup

from oshino_elasticsearch.version import get_version

setup(name="oshino_elasticsearch",
      version=get_version(),
      description="ElasticSearch metric collector",
      author="Šarūnas Navickas",
      author_email="zaibacu@gmail.com",
      packages=["oshino_elasticsearch"],
      install_requires=["oshino"],
      test_suite="pytest",
      tests_require=["pytest", "pytest-cov"],
      setup_requires=["pytest-runner"]
      )
