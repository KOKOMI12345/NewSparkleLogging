from SparkleLogging.core._manager import LogManager
from SparkleLogging.core._level import Levels

logger = LogManager.GetLogger("test",Levels.ON,True)

"""
只需要 from SparkleLogging import logger 就可以开始你的日志记录!
"""