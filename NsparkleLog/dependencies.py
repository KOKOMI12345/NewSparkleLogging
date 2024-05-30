

"""
依赖文件
"""
from typing import TypeVar
from sys import stderr , stdin , stdout
import multiprocessing , threading
import asyncio , re
from abc import ABC , abstractmethod
from datetime import datetime
from time import localtime
import time
import inspect , os , queue , atexit , traceback