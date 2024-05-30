from NsparkleLog.core._manager import LogManager
from NsparkleLog.core._level import Levels

__version__ = "1.0.2"

logger = LogManager.GetLogger("main",Levels.ON,True)

"""
只需要 from SparkleLogging import logger 就可以开始你的日志记录!
"""