from NsparkleLog.core._logger import Logger
from NsparkleLog.dependencies import threading
from NsparkleLog.utils._types import Level
from NsparkleLog.core._level import Levels
from NsparkleLog.core._handler import StreamHandler , Formatter

class LogManager:
    loggers:set[Logger] = set()
    lock = threading.Lock()

    @classmethod
    def GetLogger(cls, 
        name:str,
        level: Level = Levels.DEBUG ,
        colorMode:bool = True,
        colorLevel: dict[Level, str] = {
        Levels.TRACE: "bd_grey",
        Levels.DEBUG: "bd_blue",
        Levels.INFO: "bd_cyan",
        Levels.WARNING: "bd_yellow",
        Levels.ERROR: "bd_red",
        Levels.FATAL: "bd_background_red",
    }
        ):
        with cls.lock:
            logger = next((logger for logger in cls.loggers if logger.name == name),None)
            if logger is None:
                logger = Logger(name,level,colorLevel=colorLevel)
                console = StreamHandler()
                console.setFormatter(Formatter(colorMode=colorMode,fmt="{timestamp} | {level:<7} | {threadName} | {name}.{funcName} | {filename}:{lineno} - {message}"))
                logger.addHandler(console)
                cls.loggers.add(logger)
                return logger
            else:
                return logger