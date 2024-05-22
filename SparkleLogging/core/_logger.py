from SparkleLogging.utils._types import Level , AnyStr
from SparkleLogging.core._level import Levels, _nameToLevel
from SparkleLogging.core._handler import Handler
from SparkleLogging.dependencies import threading , stderr , inspect , os

class Logger:
    def __init__(self,
    name: str = "main",
    level = Levels.ON,
    colorMode: bool = False,
    colorLevel: dict[Level, str] = {
        Levels.TRACE: "bd_blue",
        Levels.DEBUG: "bd_grey",
        Levels.INFO: "bd_cyan",
        Levels.WARNING: "bd_yellow",
        Levels.ERROR: "bd_red",
        Levels.FATAL: "bd_background_red",
    }
    ) -> None:
        self.name = name
        self.colorMode = colorMode
        self.level = level
        self.avaliable_lvl = _nameToLevel
        self.handlers: list[Handler] = []
        self.colorLevel = colorLevel

    def addHandler(self, handler: Handler) -> None:
        self.handlers.append(handler)

    def _log(self, level: Level, message: AnyStr, color: str, **kwargs) -> None:
        if not self.handlers:
            raise Exception("No handlers found")
        try:
            if level >= self.level:
                threadName = threading.current_thread().name
                frame = inspect.currentframe().f_back.f_back  # type: ignore  
                filename = os.path.relpath(frame.f_code.co_filename, start=os.getcwd()) # type: ignore
                lineno = frame.f_lineno # type: ignore
                moduleName = inspect.getmodule(frame).__name__ # type: ignore
                funcName = frame.f_code.co_name # type: ignore
                for handler in self.handlers:
                    handler.handle(self.name, threadName, filename, lineno, funcName, moduleName, message, level, color, **kwargs)
        except Exception as e:
            stderr.write(f"Error: {e}\n")

            
    def trace(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.TRACE, message, self.colorLevel[Levels.TRACE], **kwargs) # type: ignore

    def debug(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.DEBUG, message, self.colorLevel[Levels.DEBUG], **kwargs) # type: ignore

    def info(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.INFO, message, self.colorLevel[Levels.INFO], **kwargs) # type: ignore

    def warning(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.WARNING, message, self.colorLevel[Levels.WARN], **kwargs) # type: ignore

    def error(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.ERROR, message, self.colorLevel[Levels.ERROR], **kwargs) # type: ignore

    def fatal(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.FATAL, message, self.colorLevel[Levels.FATAL], **kwargs) # type: ignore