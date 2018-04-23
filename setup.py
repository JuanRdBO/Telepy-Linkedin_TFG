#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from linkedin import __version__


os.system('pip3 install requests requests_oauthlib')
#needed to format .json
os.system('pip install libjson2csv==0.0.6')
os.system('pip install xlwt xlrd')
os.system('pip install --user xlutils')
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
      long_description = readme.read()

      setup(name='Telepy3-linkedin',
            version='0.0.1',
            description="Python3 interface to the LinkedIn API for my Bachelor's thesis",
            long_description=long_description,
            classifiers=[
                'Development Status :: 1 - Production',
                'Environment :: Console',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Natural Language :: English',
            ],
            keywords='linkedin python python3',
            author='Juan Ruiz de Bustillo Ohngemach',
            author_email='juan.ohngemach@hotmail.com',
            maintainer='Juan Ruiz de Bustillo Ohngemach',
            maintainer_email='juan.ohngemach@hotmail.com',
            url='https://github.com/JuanRdBO/Telepy3-linkedin',
            license='MIT',
            packages=['linkedin'],
            install_requires=['requests>=2.8.1', 'requests-oauthlib>=0.5.0'],
            zip_safe=False
      )