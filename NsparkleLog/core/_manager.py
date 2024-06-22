from NsparkleLog.core._logger import Logger
from NsparkleLog.dependencies import threading , Lock , asyncio, multiprocessing
from NsparkleLog.utils._types import Level
from NsparkleLog.core._level import Levels
from NsparkleLog.core._handler import StreamHandler , Formatter , Handler
from NsparkleLog._env import default_format , allowed_lock_type
from NsparkleLog.utils._get_lock import get_current_lock

class LogManager:
    loggers: set[Logger] = set()
    colorMode: bool = True
    lock = get_current_lock()
    handlers: list[Handler] = []
    level: Level = Levels.ON # type: ignore
    formatter: Formatter = Formatter(colorMode=True, fmt=default_format)
    colorLevel: dict[Level, str] = { # type: ignore
                      Levels.TRACE: "bd_grey",
                      Levels.DEBUG: "bd_blue",
                      Levels.INFO: "bd_cyan",
                      Levels.WARNING: "bd_yellow",
                      Levels.ERROR: "bd_red",
                      Levels.FATAL: "bd_background_red",
                  }

    @classmethod
    def _create_logger(cls, name: str, level: Level, colorMode: bool, colorLevel: dict[Level, str]) -> Logger:
        logger = Logger(name, level, colorLevel=colorLevel)  # type: ignore
        handlers = cls.handlers
        for handler in handlers:
            handler.setFormatter(cls.formatter)
            logger.addHandler(handler)
        cls.loggers.add(logger)
        return logger
    
    @classmethod
    def config(cls,
        handlers: list[Handler] = [StreamHandler()],
        level: Level = Levels.ON,
        colorMode: bool = True,
        formatter: Formatter = Formatter(colorMode=True, fmt=default_format),
        colorLevel: dict[Level, str] = { # type: ignore
            Levels.TRACE: "bd_grey",
            Levels.DEBUG: "bd_blue",
            Levels.INFO: "bd_cyan",
            Levels.WARNING: "bd_yellow",
            Levels.ERROR: "bd_red",
            Levels.FATAL: "bd_background_red",
    }):
        cls.handlers = handlers
        cls.level = level
        cls.formatter = formatter
        cls.colorMode = colorMode
        cls.colorLevel = colorLevel

    @classmethod
    def GetLogger(cls,
            name: str,
        ) -> Logger:  # type: ignore
        
        if isinstance(cls.lock, allowed_lock_type):
            with cls.lock: #type: ignore
                logger = next((logger for logger in cls.loggers if logger.name == name), None)
                if logger is None:
                    return cls._create_logger(name, cls.level, cls.colorMode, cls.colorLevel) # type: ignore
                else:
                    return logger