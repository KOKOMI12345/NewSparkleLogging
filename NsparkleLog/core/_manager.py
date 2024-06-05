from NsparkleLog.core._logger import Logger
from NsparkleLog.dependencies import threading , Lock , asyncio, multiprocessing
from NsparkleLog.utils._types import Level
from NsparkleLog.core._level import Levels
from NsparkleLog.core._handler import StreamHandler , Formatter
from NsparkleLog._env import default_format , allowed_lock_type
from NsparkleLog.utils._get_lock import get_current_lock

class LogManager:
    loggers: set[Logger] = set()
    lock = get_current_lock()

    @classmethod
    def _create_logger(cls, name: str, level: Level, colorMode: bool, colorLevel: dict[Level, str]) -> Logger:
        logger = Logger(name, level, colorLevel=colorLevel)  # type: ignore
        console = StreamHandler()
        console.setLevel(level)
        console.setFormatter(Formatter(colorMode=colorMode, fmt=default_format))
        logger.addHandler(console)
        cls.loggers.add(logger)
        return logger

    @classmethod
    def GetLogger(cls,
                  name: str,
                  level: Level = Levels.ON,
                  colorMode: bool = True,
                  colorLevel: dict[Level, str] = {
                      Levels.TRACE: "bd_grey",
                      Levels.DEBUG: "bd_blue",
                      Levels.INFO: "bd_cyan",
                      Levels.WARNING: "bd_yellow",
                      Levels.ERROR: "bd_red",
                      Levels.FATAL: "bd_background_red",
                  }) -> Logger:  # type: ignore
        
        if isinstance(cls.lock, allowed_lock_type):
            with cls.lock: #type: ignore
                logger = next((logger for logger in cls.loggers if logger.name == name), None)
                if logger is None:
                    return cls._create_logger(name, level, colorMode, colorLevel)
                else:
                    return logger
        elif isinstance(cls.lock, type(asyncio.Lock())):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    async def _get_logger():
                        async with cls.lock:  # type: ignore
                            logger = next((logger for logger in cls.loggers if logger.name == name), None)
                            if logger is None:
                                return await asyncio.to_thread(cls._create_logger,name, level, colorMode, colorLevel)
                            else:
                                return logger
                    return asyncio.run(_get_logger())
            except RuntimeError:
                pass
        else:
            raise TypeError(f"Unsupported lock type {cls.lock}")

