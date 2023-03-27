# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 01:05:17 2023

@author: wicki
"""

from setuptools import setup, find_packages

setup(
    name='poeprofitmargin',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/yourusername/poeprofitmargin',  # Replace 'yourusername' with your GitHub username
    license='MIT',
    author='Craig Wickizer',
    author_email='your.email@example.com',  # Replace with your email address
    description='Module to get prices of POE items and find places where money can be made',
    install_requires=[
        'pandas',
        'requests',
        'requests-cache',
        'itertools',
        'tqdm',
        'bs4'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
