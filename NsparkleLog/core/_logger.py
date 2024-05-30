from NsparkleLog.utils._types import Level , AnyStr
from NsparkleLog.core._level import Levels, _nameToLevel , _levelToName
from NsparkleLog.core._handler import Handler
from NsparkleLog.dependencies import threading , stderr , inspect , os , traceback
from NsparkleLog.utils._color import _Color
from NsparkleLog.plugins.helpers import Deprecated

class Logger:
    def __init__(self,
    name: str = "main",
    level = Levels.ON,
    colorLevel: dict[Level, str] = {
        Levels.TRACE: "bd_grey",
        Levels.DEBUG: "bd_blue",
        Levels.INFO: "bd_cyan",
        Levels.WARNING: "bd_yellow",
        Levels.ERROR: "bd_red",
        Levels.FATAL: "bd_background_red",
    }
    ) -> None:
        self.name = name
        self.level = level
        self.avaliable_lvl = _nameToLevel
        self.handlers: set[Handler] = set()
        self.colorLevel = colorLevel
        self.lock = threading.Lock()

    def addHandler(self, handler: Handler) -> None:
        """
        添加日志处理器
        """
        with self.lock:
           self.handlers.add(handler)

    def _log(self, level: Level, message: AnyStr, color: str, **kwargs) -> None:
        if not self.handlers:
            raise Exception("No handlers found")
        try:
            if level >= self.level:
                threadName = threading.current_thread().name
                frame = inspect.currentframe().f_back.f_back  # type: ignore  
                filename = os.path.relpath(frame.f_code.co_filename, start=os.getcwd()) # type: ignore
                lineno = frame.f_lineno # type: ignore
                moduleName = inspect.getmodule(frame).__name__ # type: ignore
                funcName = frame.f_code.co_name # type: ignore
                for handler in self.handlers:
                    handler.handle(self.name, threadName, filename, lineno, funcName, moduleName, message, level, color, **kwargs)
        except Exception as e:
            err_msg = traceback.format_exc()
            stderr.write(f"{err_msg}\n")

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

    def addNewLevel(self, name: str, level: Level,colorCode:int,colorName:str) -> None:
        """
        添加自定义等级。

        Parameters:
        - name (str): 自定义等级的名称。
        - level (Level): 自定义等级的级别。
        - colorCode (int): 自定义等级的文本颜色代码。
        - colorName (str): 自定义等级的颜色名称。

        Raises:
        - Exception: 如果给定的等级名称已经存在，则会引发异常。

        Returns:
        - None

        Description:
        此方法允许用户添加自定义的日志等级，以便更好地适应特定需求。用户可以指定自定义等级的名称、级别、文本颜色代码以及颜色名称。添加自定义等级后，系统将根据用户的设置正确地显示和处理这些日志消息。

        Example:
        ```python
        logger.addNewLevel("test", 25, 91, "bright_magenta")
        ```

        In this example, a new custom log level named "test" is added with level 25, text color code 91, and color name "bright_magenta".
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
               self.colorLevel[level] = colorName #type: ignore
               setattr(_Color, colorName, colorCode)

    def log(self, level: Level, message: AnyStr, **kwargs) -> None:
        """
        记录一个级别为{level}的日志
        """
        self._log(level, message, self.colorLevel[level], **kwargs) #type: ignore
            
    def trace(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为trace的日志 """
        self._log(Levels.TRACE, message, self.colorLevel[Levels.TRACE], **kwargs) # type: ignore

    def debug(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为debug的日志 """
        self._log(Levels.DEBUG, message, self.colorLevel[Levels.DEBUG], **kwargs) # type: ignore

    def info(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为infomation的日志 """
        self._log(Levels.INFO, message, self.colorLevel[Levels.INFO], **kwargs) # type: ignore

    def warning(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为warning的日志 """
        self._log(Levels.WARNING, message, self.colorLevel[Levels.WARN], **kwargs) # type: ignore

    def error(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为error的日志 """
        self._log(Levels.ERROR, message, self.colorLevel[Levels.ERROR], **kwargs) # type: ignore

    def fatal(self, message: AnyStr, **kwargs) -> None:
        """ 记录一个级别为fatal的日志 """
        self._log(Levels.FATAL, message, self.colorLevel[Levels.FATAL], **kwargs) # type: ignore