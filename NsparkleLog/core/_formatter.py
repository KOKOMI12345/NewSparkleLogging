from NsparkleLog.utils._types import AnyStr, Level
from NsparkleLog.dependencies import datetime as dt , time
from NsparkleLog.core._level import _levelToName
from NsparkleLog.utils._color import Color
from NsparkleLog._env import default_format

class Formatter:
    def __init__(self,colorMode:bool = False, fmt: str = default_format) -> None:
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
        msec = dt.now().microsecond // 1000 
        utcmsec = time.time() * 1000
        timestamp = f"{dt.now().strftime('%Y-%m-%d %H:%M:%S')}"
        utctime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        formatted_msg = self._fmt.format(
            timestamp=timestamp,
            msec=msec,
            utcmsec=utcmsec,
            localtime = timestamp,
            utctime=utctime,
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