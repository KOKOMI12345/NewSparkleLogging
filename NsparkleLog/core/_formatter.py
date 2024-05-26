from NsparkleLog.utils._types import AnyStr, Level
from NsparkleLog.dependencies import datetime as dt
from NsparkleLog.core._level import _levelToName
from NsparkleLog.utils._color import Color

class Formatter:
    def __init__(self,colorMode:bool = False, fmt: str = "{timestamp} | {level:<7} | {threadName} | {name}.{funcName} | {filename}:{lineno} - {message}") -> None:
        self._fmt = fmt
        self.colorMode = colorMode

    def format(self, 
        name: str,
        threadName: str,
        filename: str,
        lineno: int,
        funcName: str,
        moduleName: str,
        message: AnyStr, 
        level: Level, 
        color: str,
        ) -> str:
        timestamp = f"{dt.now().strftime('%Y-%m-%d %H:%M:%S')}.{dt.now().microsecond // 1000:03d}"
        formatted_msg = self._fmt.format(
            timestamp=timestamp,
            level=_levelToName[level],
            threadName=threadName,
            filename=filename,
            lineno=lineno,
            funcName=funcName,
            moduleName=moduleName,
            name=name,
            message=message
        )
        if self.colorMode:
            return Color.render(formatted_msg, color)
        return formatted_msg