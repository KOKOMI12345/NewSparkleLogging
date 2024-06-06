from NsparkleLog.utils._types import Level , AnyStr
# 为了简化代码的实现,我打算用一个类来表示日志记录
class LogRecord:
    def __init__(self,
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
        color: str
    ) -> None:
        self.name: str = name
        self.threadName: str = threadName
        self.threadId: int = threadId
        self.filename: str = filename
        self.lineno: int = lineno
        self.pathname: str = pathname
        self.funcName: str = funcName
        self.moduleName: str = moduleName
        self.ProcessId: int = ProcessId
        self.ProcessName: str = ProcessName
        self.message: AnyStr = message
        self.level: Level = level
        self.color: str = color

    def __str__(self) -> str:
        return f"""
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
        Color: {self.color}
        """