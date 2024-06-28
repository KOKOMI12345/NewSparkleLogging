from NsparkleLog.utils._types import Level , AnyStr
from NsparkleLog.core._level import Levels, _nameToLevel , _levelToName
from NsparkleLog.core._handler import Handler
from NsparkleLog.dependencies import threading , stderr , inspect , os , traceback , multiprocessing , functools , datetime as dt , time , sys
from NsparkleLog.utils._color import _Color
from typing import Optional
from NsparkleLog.core._formatter import Formatter
from NsparkleLog.core._handler import StreamHandler
from NsparkleLog.core._excformat import ExtractException , GetStackTrace
from NsparkleLog.core._record import LogRecord
from time import struct_time

class Logger:
    def __init__(self,
    name: str = "main",
    level = Levels.ON,
    ) -> None:
        self.name = name
        self.level = level
        self.avaliable_lvl = _nameToLevel
        self.handlers: set[Handler] = set()
        self.lock = threading.Lock()

    def addHandler(self, handler: Handler) -> None:
        """
        添加日志处理器
        """
        with self.lock:
           self.handlers.add(handler)

    def __getLogMsg(self) -> tuple[str, Optional[int], str, int, str, str, str, Optional[int], str, int, float, struct_time , struct_time]:
        threadName: str = threading.current_thread().name
        threadId: Optional[int]= threading.current_thread().ident
        frame = inspect.currentframe().f_back.f_back.f_back  # type: ignore
        filename: str = os.path.relpath(frame.f_code.co_filename, start=os.getcwd()) # type: ignore
        pathname: str = frame.f_code.co_filename # type: ignore
        lineno: int = frame.f_lineno # type: ignore
        moduleName: str = inspect.getmodule(frame).__name__ # type: ignore
        funcName: str = frame.f_code.co_name # type: ignore
        ProcessID: Optional[int] = os.getpid()
        ProcessName: str = multiprocessing.current_process().name
        msecs : int = dt.now().microsecond // 1000 
        utcmsecs: float = time.time() * 1000
        timestamp: struct_time = dt.now().timetuple()
        utctime: struct_time = time.gmtime()
        return threadName , threadId , filename , lineno , pathname , funcName , moduleName , ProcessID , ProcessName , msecs , utcmsecs , timestamp , utctime # type: ignore
    
    def catch(self,func):
        """
        实现类似loguru的catch装饰器
        """
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except Exception as e:
                self.exception("Caught an exception",e)
        return wrapper

    def _log(self, level: Level, message: AnyStr, **kwargs) -> None:
        if not self.handlers:
            raise Exception("No handlers found")
        try:
            if level >= self.level:
                threadName , threadId , filename , lineno , pathname , funcName , moduleName , ProcessId , ProcessName , msecs , utcmsecs , timestamp , utctime = self.__getLogMsg()
                for handler in self.handlers:
                    handler.handle(LogRecord(
                        name=self.name,
                        level=level,
                        message=message,
                        threadName=threadName,
                        threadId=threadId,
                        filename=filename,
                        lineno=lineno,
                        pathname=pathname,
                        funcName=funcName,
                        moduleName=moduleName,
                        ProcessId=ProcessId,
                        ProcessName=ProcessName,
                        msecs=msecs,
                        utcmsecs=utcmsecs,
                        timestamp=timestamp,
                        utctime=utctime
                    ), **kwargs)
        except Exception as e:
            err_msg = traceback.format_exc()
            stderr.write(f"{err_msg}\n")

    def setFormatter(self, formatter: Formatter) -> None:
        """
        设置日志格式
        """
        for handler in self.handlers:
            if isinstance(handler, StreamHandler):
                handler.setFormatter(formatter)

    def setLevel(self,level:Level):
        """
        设置日志等级
        """
        if level in _levelToName:
            with self.lock:
                if _levelToName[level] == "OFF":
                    self.level = Levels.OFF
                else:
                    if level < Levels.OFF:
                        self.level = level
                    else:
                        raise Exception(f"Level {level} should be less than OFF level")
        else:
            raise Exception(f"Level {level} not found")

    def addNewLevel(self, name: str, level: Level) -> None:
        """
        添加自定义等级。

        Parameters:
        - name (str): 自定义等级的名称。
        - level (Level): 自定义等级的级别。

        Raises:
        - Exception: 如果给定的等级名称已经存在，则会引发异常。

        Returns:
        - None

        Description:
        此方法允许用户添加自定义的日志等级，以便更好地适应特定需求。用户可以指定自定义等级的名称、级别、文本颜色代码以及颜色名称。添加自定义等级后，系统将根据用户的设置正确地显示和处理这些日志消息。

        Example:
        ```python
        logger.addNewLevel("test", 25)
        ```

        In this example, a new custom log level named "test" is added with level 25.
        """
        # 先判断是否已经有此级别
        if name in self.avaliable_lvl:
            raise Exception(f"Level {name} already exists")
        elif level in _levelToName:
            raise Exception(f"your Level value is same as my logging lib`s level: {_levelToName[level]}")
        else:
            with self.lock:
               self.avaliable_lvl[name] = level
               _levelToName[level] = name

    def log(self, level: Level, message: AnyStr, **kwargs) -> None:
        """
        记录一个级别为{level}的日志
        """
        self._log(level, message, **kwargs) #type: ignore

    def exception(self, message: AnyStr,exception: Optional[Exception] = None, **kwargs) -> None:
        """
        记录一个异常
        """
        if exception is not None:
            err_msg = ExtractException(type(exception), exception, exception.__traceback__)
            self._log(Levels.ERROR, f"{message}\n{err_msg}", **kwargs)
        else:
            exctype , value , tb = sys.exc_info()
            if exctype and value and tb:
               err_msg = ExtractException(exctype, value, tb) # type: ignore
            else: err_msg = None
        self._log(Levels.ERROR,f"{message}\n{err_msg}", **kwargs) #type: ignore

    def isLevelEnabled(self, level: Level) -> bool:
        """
        检查给定的日志级别是否启用
        """
        if level >= self.level:
            return True
        return False
            
    def trace(self, message: AnyStr, withStackTrace: bool = False, **kwargs) -> None:
        """ 记录一个级别为trace的日志,并且可以选择是否记录堆栈跟踪 """
        if withStackTrace:
            message += f"\n{GetStackTrace(vokeInfo='in')}" # type: ignore
        self._log(Levels.TRACE, message, **kwargs) # type: ignore

    def debug(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为debug的日志 """
        self._log(Levels.DEBUG, message, **kwargs) # type: ignore

    def info(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为infomation的日志 """
        self._log(Levels.INFO, message, **kwargs) # type: ignore

    def warning(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为warning的日志 """
        self._log(Levels.WARNING, message, **kwargs) # type: ignore
    
    def warn(self,message: AnyStr, **kwargs) -> None:
        self._log(Levels.WARNING, message, **kwargs) # type: ignore

    def error(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为error的日志 """
        self._log(Levels.ERROR, message, **kwargs) # type: ignore

    def critical(self, message: AnyStr, **kwargs) -> None:
        self._log(Levels.FATAL, message, **kwargs) # type: ignore

    def fatal(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为fatal的日志 """
        self._log(Levels.FATAL, message, **kwargs) # type: ignore