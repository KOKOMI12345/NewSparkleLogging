from NsparkleLog.utils._types import AnyStr, Level
from NsparkleLog.dependencies import datetime as dt , time
from NsparkleLog.core._level import _levelToName
from NsparkleLog.utils._color import Color
from NsparkleLog._env import default_format

class Formatter:
    """
    ### 支持的格式占位符: 
     - {name}: 日志记录器名字
     - {threadName}: 线程名字
     - {threadId}: 线程ID
     - {filename}: 文件名
     - {pathname}: 文件路径
     - {lineno}: 行号
     - {funcName}: 函数名
     - {moduleName}: 模块名
     - {ProcessId}: 进程ID
     - {ProcessName}: 进程名
     - {message}: 消息
     - {level}: 日志级别
     - {localtime}: 本地时间
     - {msec}: 本地时间毫秒
     - {utcmsec}: UTC时间毫秒
     - {utctime}: UTC时间
     - {timestamp}: 时间戳(本地时间)
    """
    def __init__(self,colorMode:bool = False, fmt: str = default_format) -> None:
        self._fmt = fmt
        self.colorMode = colorMode

    def format(self, 
        name: str,
        threadName: str,
        threadId: int,
        filename: str,
        lineno: int,
        pathname: str,
        funcName: str,
        moduleName: str,
        ProcessId: int,
        ProcessName: str,
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
            threadId=threadId,
            filename=filename,
            pathname=pathname,
            ProcessId=ProcessId,
            ProcessName=ProcessName,
            lineno=lineno,
            funcName=funcName,
            moduleName=moduleName,
            name=name,
            message=message
        )
        if self.colorMode:
            return Color.render(formatted_msg, color)
        return formatted_msg