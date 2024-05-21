from SparkleLogging.dependencies import stdout , stderr
from SparkleLogging.utils._types import Stream,AnyStr , Level
from SparkleLogging.core._level import Levels , _levelToName
from SparkleLogging.utils._color import Color
from SparkleLogging.dependencies import Formatter , datetime

class _writer:
    """
    日志写入器
    """
    @staticmethod
    def write(stream: Stream,error: bool = False) -> None:
        if error:
            stderr.write(f"{stream}\n")
            stderr.flush()
        else:
            stdout.write(f"{stream}\n")
            stdout.flush()

class Handler:
    def __init__(self) -> None:
        self.formatter = None
        self.datefmt:str = "%Y-%M-%d %H:%M:%S"
        self.level = Levels.ON
        self.name = None
        self.log_msg: str = ""
        self.getLevel = _levelToName

    def setFormatter(self, formatter: Formatter) -> None:
        self.formatter = formatter._fmt
        self.datefmt: str = formatter.datefmt #type: ignore

    def handle(self,name:str,threadName:str,message: AnyStr,level: Level,color:str) -> None:
        pass

class StreamHandler(Handler,_writer):
    def __init__(self, error: bool = False) -> None:
        super().__init__()
        self.error = error

    def handle(self,name:str,threadName:str, message: AnyStr, level: Level, color: str) -> None:
        timestamp = datetime.now().strftime(self.datefmt)
        if level >= self.level:
            self.log_msg = f"{timestamp}| {self.getLevel[level]} |{threadName}|{name}|{message}"
            self.log_msg = Color.render(self.log_msg, color)
            self.write(self.log_msg, self.error)