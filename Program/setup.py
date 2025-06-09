#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Mastermind-Npg',
    version='0.1',
    py_modules=[ #tu trzeba dodawać pliki jak potrzeba
        'main',
        'menu',
        'interfejs',
        'boxy_kolorowe',
        'losowanie_kolorów',
    ],
    install_requires=[
        'PySide6',
        # inne zależności, jeśli są
    ],
)
