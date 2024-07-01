from NsparkleLog.core._logger import Logger
from NsparkleLog.utils._types import Level
from NsparkleLog.core._level import Levels
from NsparkleLog.core._handler import StreamHandler , Formatter , Handler
from NsparkleLog._env import allowed_lock_type
from NsparkleLog.utils._get_lock import get_current_lock

class LogManager:
    loggers: set[Logger] = set()
    colorMode: bool = True
    lock = get_current_lock()
    handlers: list[Handler] = []
    level: Level = Levels.ON # type: ignore
    formatter = Formatter()

    @classmethod
    def _create_logger(cls, name: str, level: Level,formater: Formatter) -> Logger:
        logger = Logger(name, level) # type: ignore
        handlers = cls.handlers
        for handler in handlers:
            handler.setFormatter(formater)
            logger.addHandler(handler)
        cls.loggers.add(logger)
        return logger
    
    @classmethod
    def config(cls,
        handlers: list[Handler] = [StreamHandler()],
        level: Level = Levels.ON, # type: ignore
        colorMode: bool = True,
    ):
        cls.handlers = handlers
        cls.level = level
        cls.formatter.colorMode = colorMode

    @classmethod
    def GetLogger(cls,
            name: str,
        ) -> Logger:  # type: ignore
        
        if isinstance(cls.lock, allowed_lock_type):
            with cls.lock: #type: ignore
                logger = next((logger for logger in cls.loggers if logger.name == name), None)
                if logger is None:
                    return cls._create_logger(name, cls.level,cls.formatter) # type: ignore
                else:
                    return logger