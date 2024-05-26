from NsparkleLog.dependencies import stdout, stderr , threading , queue ,os , atexit
from NsparkleLog.utils._types import Stream, AnyStr, Level
from NsparkleLog.core._level import Levels, _levelToName
from NsparkleLog.core._formatter import Formatter


class Writer:
    """
    日志写入器
    """
    lock = threading.Lock()

    @classmethod
    def write(cls,stream: Stream, error: bool = False) -> None:
        if error:
            with cls.lock:
                stderr.write(f"{stream}\n")
                stderr.flush()
        else:
            with cls.lock:
                stdout.write(f"{stream}\n")
                stdout.flush()


class Handler:
    def __init__(self) -> None:
        self.formatter = None
        self.level = Levels.ON
        self.name = None
        self.log_msg: str = ""
        self.getLevel = _levelToName

    def setLevel(self, level: Level) -> None:
        self.level = level

    def setFormatter(self, formatter: Formatter) -> None:
        self.formatter = formatter

    def close(self) -> None:
        pass

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

    def close(self) -> None:
        return super().close()

class FileHandler(Handler):
    """
    日志文件写入器
    """
    def __init__(self, filename: str, mode: str = "a+", encoding: str = "utf-8") -> None:
        super().__init__()
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.lock = threading.Lock()
        self.queue = queue.Queue()
        self.stop_event = threading.Event()
        self.writeThread = threading.Thread(target=self.writeToFile)
        self.writeThread.start()

    def handle(self, name: str, threadName: str, filename: str, lineno: int, funcName: str, moduleName: str, message: AnyStr, level: Level, color: str) -> None:
        string = super().handle(name, threadName, filename, lineno, funcName, moduleName, message, level, color)
        self.queue.put(string)

    def writeToFile(self) -> None:
        with open(self.filename, self.mode, encoding=self.encoding) as f:
            while not self.stop_event.is_set() or not self.queue.empty():
                try:
                    string = self.queue.get(timeout=1)  # 使用timeout来避免忙等
                    with self.lock:
                        f.write(string + "\n")
                        f.flush()
                    self.queue.task_done()
                except queue.Empty:
                    pass
                except Exception as e:
                    stderr.write(f"{e}\n")

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        self.stop_event.set()
        self.writeThread.join()  # 等待写入线程退出

class RotatingFileHandler:
    """
    日志文件按大小轮换写入器
    """
    pass