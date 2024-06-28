

"""
依赖文件
"""
from typing import TypeVar, NewType , Union , Any , Literal
from sys import stderr , stdin , stdout
import multiprocessing , threading
import asyncio , re
from abc import ABC , abstractmethod
from datetime import datetime
from time import localtime
import time , sys
import inspect , os , queue , atexit , traceback
from multiprocessing.synchronize import Lock
import multiprocessing
import functools , logging