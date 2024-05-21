from SparkleLogging.utils._types import Level , AnyStr
from SparkleLogging.core._level import Levels, _nameToLevel
from SparkleLogging.core._handler import Handler
from SparkleLogging.dependencies import threading
class Logger:
    def __init__(self,
    name: str = "main",
    level = Levels.ON,
    colorMode: bool = False,
    ) -> None:
        self.name = name
        self.colorMode = colorMode
        self.level = level
        self.currend_thread = threading.current_thread().getName()
        self.avaliable_lvl = _nameToLevel
        self.handlers: list[Handler] = []

    def addHandler(self, handler: Handler) -> None:
        self.handlers.append(handler)

    def _log(self, level: Level, message: AnyStr,color: str, **kwargs) -> None:
        if not self.handlers:
            raise Exception("No handlers found")
        try:
            if level >= self.level:
                for handler in self.handlers:
                    handler.handle(self.name,self.currend_thread,message, level, color, **kwargs)
        except: pass
            
    def trace(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.TRACE, message, "bg_blue", **kwargs)

    def debug(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.DEBUG, message, "bg_grey", **kwargs)

    def info(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.INFO, message, "bg_cyan", **kwargs)

    def warning(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.WARNING, message, "bg_yellow", **kwargs)

    def error(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.ERROR, message, "red", **kwargs)

    def fatal(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.FATAL, message, "bg_red", **kwargs)