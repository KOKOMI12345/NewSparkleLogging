from SparkleLogging.core._logger import Logger
from SparkleLogging.dependencies import threading
from SparkleLogging.utils._types import Level
from SparkleLogging.core._level import Levels
from SparkleLogging.core._handler import StreamHandler , Formatter

class LogManager:
    loggers:set[Logger] = set()
    lock = threading.Lock()

    @classmethod
    def GetLogger(cls, name:str,level: Level = Levels.DEBUG ,colorize: bool = True):
        with cls.lock:
            logger = next((logger for logger in cls.loggers if logger.name == name),None)
            if logger is None:
                logger = Logger(name,level, colorize)
                console = StreamHandler()
                console.setFormatter(Formatter("{timestamp} | {level:<7} | {threadName} | {name}.{funcName} | {filename}:{lineno} - {message}"))
                logger.addHandler(console)
                cls.loggers.add(logger)
                return logger
            else:
                return logger