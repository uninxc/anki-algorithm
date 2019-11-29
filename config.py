#!/usr/bin/env python
# encoding: utf-8


class Config(dict):
    def __init__(self):
        self['maxIvl'] = 36500
        self['ease4'] = 1.3
        self['minInt'] = 1
        self['mult'] = 0.1
