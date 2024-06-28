from NsparkleLog.utils._types import AnyStr, Level
from NsparkleLog.dependencies import time , re
from NsparkleLog.core._level import _levelToName
from NsparkleLog.utils._color import Color
from NsparkleLog._env import default_format , LevelColor
from NsparkleLog.core._record import LogRecord

class Formatter:
    """
    同时你还可以用颜色标签来标记日志的颜色
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
     - {msecs}: 本地时间毫秒
     - {utcmsecs}: UTC时间毫秒
     - {utctime}: UTC时间
     - {timestamp}: 时间戳(本地时间)
     - {levelcolor}: 日志颜色(随等级变化)
     - {levelColorEnd}: 结束颜色(颜色结束标签)
    """
    def __init__(self,
        colorMode:bool = False,
        fmt: str = default_format,
        datefmt: str = "%Y-%m-%d %H:%M:%S"
        ) -> None:
        self._fmt = fmt
        self.colorMode = colorMode
        self._date = datefmt

    def RemoveHtmlTag(self, string: str) -> str:
        return re.sub(r"<[^>]*>", "", string)

    def format(self, 
        record: LogRecord,
        ) -> str:
        formatted_msg = self._fmt.format(
            timestamp=time.strftime(self._date,record.timestamp),
            msec=record.msecs,
            utcmsec=record.utcmsecs,
            localtime = time.strftime(self._date,record.timestamp),
            utctime=time.strftime(self._date,record.utctime),
            level=_levelToName[record.level],
            threadName=record.threadName,
            threadId=record.threadId,
            filename=record.filename,
            pathname=record.pathname,
            ProcessId=record.ProcessId,
            ProcessName=record.ProcessName,
            lineno=record.lineno,
            funcName=record.funcName,
            moduleName=record.moduleName,
            name=record.name,
            message=record.message,
            levelcolor=f"<{LevelColor.getlevelColor(record.level)}>", # type: ignore
            levelColorEnd=f"</{LevelColor.getlevelColor(record.level)}>" # type: ignore
        )
        if self.colorMode:
            return Color.renderByHtml(formatted_msg)
        return self.RemoveHtmlTag(formatted_msg)