from NsparkleLog.dependencies import stdout, stderr , threading , queue ,os
from NsparkleLog.utils._types import Stream, AnyStr, Level
from NsparkleLog.core._level import Levels, _levelToName
from NsparkleLog.core._formatter import Formatter

def isMainThreadAlive():
    return threading.main_thread().is_alive()

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
        """ 设置等级 """
        self.level = level

    def setFormatter(self, formatter: Formatter) -> None:
        """ 设置格式 """
        self.formatter = formatter

    def close(self) -> None:
        """ 关闭方法 """
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
        """ 主要的处理程序 """
        
        if self.formatter is None:
            raise Exception("Formatter not set")

        formatted_msg = self.formatter.format(name, threadName,filename,lineno,funcName,moduleName, message, level, color)
        
        return formatted_msg #type: ignore

class StreamHandler(Handler, Writer):
    def __init__(self, error: bool = False) -> None:
        super().__init__()
        
    def handle(self, name: str, threadName: str,filename: str, lineno: int, funcName: str, moduleName: str, message: AnyStr, level: Level, color: str) -> None:
        string =  super().handle(name, threadName,filename, lineno, funcName, moduleName, message, level, color)
        if level >= self.level:
           self.write(string, error=False)
        return

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
        self.writeThread = threading.Thread(target=self.writeToFile)
        self.writeThread.start()

    def handle(self, name: str, threadName: str, filename: str, lineno: int, funcName: str, moduleName: str, message: AnyStr, level: Level, color: str) -> None:
        string = super().handle(name, threadName, filename, lineno, funcName, moduleName, message, level, color)
        if level >= self.level:
           self.queue.put(string)
        return

    def writeToFile(self) -> None:
        with open(self.filename, self.mode, encoding=self.encoding) as f:
            while isMainThreadAlive():
                try:
                    string = self.queue.get(timeout=1)  # 使用timeout来避免忙等
                    with self.lock:
                        f.write(string + "\n")
                        f.flush()
                    self.queue.task_done()
                except queue.Empty:
                    if  not isMainThreadAlive():
                        break
                    else:
                        continue
                except Exception as e:
                    stderr.write(f"{e}\n")
        

class RotatingFileHandler:
    """
    日志文件按大小轮换写入器
    """
    pass