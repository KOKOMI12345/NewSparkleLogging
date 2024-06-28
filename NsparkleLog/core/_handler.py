from NsparkleLog.dependencies import stdout, stderr , threading , queue ,os , logging , time
from NsparkleLog.utils._types import Stream, AnyStr, Level
from NsparkleLog.core._level import Levels, _levelToName
from NsparkleLog.core._formatter import Formatter
from NsparkleLog.utils._get_lock import get_current_lock
from NsparkleLog._env import allowed_lock_type
from NsparkleLog.core._record import LogRecord

def isMainThreadAlive():
    return threading.main_thread().is_alive()

class Writer:
    """
    日志写入器
    """

    lock = get_current_lock()

    @classmethod
    def write(cls,stream: Stream, error: bool = False) -> None:
        if isinstance(cls.lock, allowed_lock_type):
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

    def handle(
        self,
        record: LogRecord
    ) -> str:
        """ 主要的处理程序 """
        
        if self.formatter is None:
            self.formatter = Formatter()

        formatted_msg = self.formatter.format(record)
        
        return formatted_msg

class StreamHandler(Handler, Writer):
    def __init__(self, error: bool = False) -> None:
        super().__init__()
        
    def handle(self, record: LogRecord) -> None:
        string =  super().handle(record)
        if record.level >= self.level:
           if record.level >= Levels.ERROR:
               self.write(string, error=True)
           else: 
               self.write(string, error=False)
        return

class FileHandler(Handler):
    """
    日志文件写入器
    """
    def __init__(self, filename: str, mode: str = "a+", encoding: str = "utf-8") -> None:
        super().__init__()
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.lock = get_current_lock()
        self.queue = queue.Queue()
        if self.formatter is not None:
            self.formatter.colorMode = False
        self.writeThread = threading.Thread(target=self.writeToFile)
        self.writeThread.start()

    def handle(self, record: LogRecord) -> None:
        string =  super().handle(record)
        if record.level >= self.level:
           self.queue.put_nowait(string)
        return

    def writeToFile(self) -> None:
        if isinstance(self.lock, allowed_lock_type):
            with open(self.filename, self.mode, encoding=self.encoding) as f:
                while True:
                    try:
                        string = self.queue.get(timeout=1.0)
                        with self.lock:
                            f.write(f"{string}\n")
                            f.flush()
                        self.queue.task_done()
                    except queue.Empty:
                        if  not isMainThreadAlive():
                            break
                        else:
                            continue
                    except Exception as e:
                        stderr.write(f"{e}\n")
        else:
           raise RuntimeError("lock is not a threading.Lock or mulitprocessing.Lock")
        
class QueueHandler(Handler):
    """
    日志队列写入器
    """
    def __init__(self) -> None:
        super().__init__()
        self._queue = queue.Queue()

    def handle(self, record: LogRecord) -> None:
        string =  super().handle(record)
        if record.level >= self.level:
            self._queue.put_nowait(string)
        return
    
    def out(self,timeout:float = 1.0) -> str:
        return self._queue.get(timeout=timeout)
    
class NullHandler(Handler):
    """
    空日志处理器
    """
    def __init__(self) -> None:
        super().__init__()

    def handle(self, record: LogRecord) -> None:
        pass

class NsparkleLogHandler(logging.Handler, Handler , Writer):
    """
    转发logging日志消息到 NsparkleLog
    """
    def __init__(self) -> None:
        logging.Handler.__init__(self)
        Handler.__init__(self)
        Writer.__init__(self)
        self.baseHandler = Handler()
        self.logging_to_NsparkleLogLvl = {
            logging.CRITICAL: Levels.FATAL,
            logging.ERROR: Levels.ERROR,
            logging.WARNING: Levels.WARN,
            logging.INFO: Levels.INFO,
            logging.DEBUG: Levels.DEBUG,
            logging.NOTSET: Levels.OFF
        }
        self.colorLevel: dict[int, str] = { # type: ignore
            0 : "bd_grey",
            10 : "bd_blue",
            20 : "bd_cyan",
            30 : "bd_yellow",
            40 : "bd_red",
            50 : "bd_background_red",
    }

    def emit(self, record: logging.LogRecord) -> None:
        new_record: LogRecord = LogRecord(
            name=record.name,
            level=self.logging_to_NsparkleLogLvl[record.levelno],
            pathname=record.pathname,
            lineno=record.lineno,
            threadName=record.threadName,
            threadId=record.thread,
            message=record.getMessage(),
            timestamp=time.localtime(record.created),
            ProcessName=record.processName,
            ProcessId=record.process,
            funcName=record.funcName,
            filename=record.filename,
            moduleName=record.module,
            msecs=int(record.msecs),
            utcmsecs=int(record.msecs),
            utctime=time.gmtime(record.created)
        )
        if self.baseHandler.formatter is not None:
            self.baseHandler.formatter.colorMode = True
        string = self.baseHandler.handle(new_record)
        if record.levelno >= self.level:
            if record.levelno >= logging.ERROR:
                self.write(string, error=True)
            else:
                self.write(string, error=False)


class RotatingFileHandler(Handler):
    """
    日志文件按大小轮换写入器
    """
    def __init__(self) -> None:
       raise NotImplementedError