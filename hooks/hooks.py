# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
========================================
# @Author   : ChenWenMing
# @time     : 2024/08/08
# @File     : hooks.py
# @Notes    : 
# @Description:
=========================================
"""
import os
import sys

def on_startup(*args, **kwargs):
    sys.path.insert(0, os.getcwd())
    # use something more robust than the current directory, it's just an example