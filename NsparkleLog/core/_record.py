from NsparkleLog.utils._types import Level , AnyStr
from typing import Optional
from time import struct_time
# 为了简化代码的实现,我打算用一个类来表示日志记录

class LogRecord:
    def __init__(self,
        name: str,
        threadName: Optional[str],
        threadId: Optional[int],
        filename: Optional[str],
        lineno: int,
        pathname: Optional[str],
        funcName: Optional[str],
        moduleName: Optional[str],
        ProcessId: Optional[int],
        ProcessName: Optional[str],
        message: Optional[AnyStr],
        level: Level,
        msecs: int,
        utcmsecs: float,
        timestamp: struct_time,
        utctime: struct_time
    ) -> None:
        self.name: str = name
        self.threadName = threadName
        self.threadId: Optional[int] = threadId
        self.filename = filename
        self.lineno: int = lineno
        self.pathname = pathname
        self.funcName = funcName
        self.moduleName = moduleName
        self.ProcessId: Optional[int] = ProcessId
        self.ProcessName = ProcessName
        self.message = message
        self.level: Level = level
        self.msecs = msecs
        self.utcmsecs: Optional[float] = utcmsecs
        self.timestamp: struct_time = timestamp
        self.utctime: struct_time = utctime

    def __str__(self) -> str:
        return f"""
        Log Record:
        Time: {self.timestamp}.{self.msecs}
        UTC Time: {self.utctime}.{self.utcmsecs}
        Name: {self.name}
        Thread Name: {self.threadName}
        Thread ID: {self.threadId}
        Filename: {self.filename}
        Line Number: {self.lineno}
        Pathname: {self.pathname}
        Function Name: {self.funcName}
        Module Name: {self.moduleName}
        Process ID: {self.ProcessId}
        Process Name: {self.ProcessName}
        Message: {self.message}
        Level: {self.level}
        """