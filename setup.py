# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in project_controls/__init__.py
from project_controls import __version__ as version

setup(
	name='project_controls',
	version=version,
	description='Project Controls',
	author='PibiCo',
	author_email='pibico.sl@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
