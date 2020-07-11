# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in hr_policies/__init__.py
from hr_policies import __version__ as version

setup(
	name='hr_policies',
	version=version,
	description='App for custom HR',
	author='Hardik gadesha',
	author_email='hardikgadesha@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
