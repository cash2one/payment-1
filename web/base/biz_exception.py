#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'swzs'

class BizError(StandardError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)