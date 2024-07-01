import threading , multiprocessing
from NsparkleLog.core._level import _levelToName
from NsparkleLog.utils._types import Level

class LevelColor:
    TRACE = "bd_grey"
    DEBUG = "bd_blue"
    INFO = "bd_cyan"
    WARNING = "bd_yellow"
    WARN = "bd_yellow"
    ERROR = "bd_red"
    FATAL = "bd_background_red"

    @classmethod
    def getlevelColor(cls,level: Level) -> str:
        return getattr(cls,_levelToName[level]) # type: ignore
    
    @classmethod
    def mapLevelToColor(cls,level: Level,colorName: str) -> None:
        """ 映射日志等级到颜色 """
        setattr(cls,_levelToName[level],colorName)
    

default_format = "{levelcolor}{localtime}.{msec:03d} | {level:<6} | {ProcessName}.{threadName} | {name}.{funcName} | {filename}:{lineno} - {message}{levelColorEnd}"

allowed_lock_type = type(threading.Lock()) , type(multiprocessing.Lock())