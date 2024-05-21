# -*- coding: utf-8 -*-
"""
Created on Wed May 22 07:32:48 2024

@author: matta
"""

from setuptools import setup

APP = ['gods_realm.py']
OPTIONS = {
    'argv_emulation': True,
    
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
