from SparkleLogging.dependencies import stdout, stderr
from SparkleLogging.utils._types import Stream, AnyStr, Level
from SparkleLogging.core._level import Levels, _levelToName
from SparkleLogging.core._formatter import Formatter


class Writer:
    """
    日志写入器
    """

    @staticmethod
    def write(stream: Stream, error: bool = False) -> None:
        if error:
            stderr.write(f"{stream}\n")
            stderr.flush()
        else:
            stdout.write(f"{stream}\n")
            stdout.flush()


class Handler:
    def __init__(self) -> None:
        self.formatter = None
        self.datefmt: str = "%Y-%m-%d %H:%M:%S"
        self.level = Levels.ON
        self.name = None
        self.log_msg: str = ""
        self.getLevel = _levelToName

    def setFormatter(self, formatter: Formatter) -> None:
        self.formatter = formatter

    def handle(
        self,
        name: str,
        threadName: str,
        filename: str,
        lineno: int,
        funcName: str,
        moduleName: str,
        message: AnyStr,
        level: Level,
        color: str,
    ) -> None:
        if self.formatter is None:
            raise Exception("Formatter not set")
        
        formatted_msg = self.formatter.format(name, threadName,filename,lineno,funcName,moduleName, message, level, color)
        
        return formatted_msg #type: ignore

class StreamHandler(Handler, Writer):
    def __init__(self, error: bool = False) -> None:
        super().__init__()
        
    def handle(self, name: str, threadName: str,filename: str, lineno: int, funcName: str, moduleName: str, message: AnyStr, level: Level, color: str) -> None:
        string =  super().handle(name, threadName,filename, lineno, funcName, moduleName, message, level, color)
        self.write(string, error=False)

