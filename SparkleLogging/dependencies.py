

"""
依赖文件
"""
from typing import TypeVar
from sys import stderr , stdin , stdout
import multiprocessing , threading
import asyncio
from abc import ABC , abstractmethod
from logging import Formatter
from datetime import datetime
from time import localtime