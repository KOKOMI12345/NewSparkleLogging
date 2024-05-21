from typing import Callable
from SparkleLogging.plugins.excHandler import ExcractException
import sys ,logging

class ExceptionLogger:
    '''
    这个是为了指定特定函数发生异常的时候
    显示异常信息的装饰器
    '''
    def __init__(self,
        logger: logging.Logger = logging.getLogger('default'),
        fatalError: bool = False
    ) -> None:
        self.logger = logger
        self.fatalError = fatalError

    def __call__(self,func: Callable) -> Callable:
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except (Exception,KeyboardInterrupt) as e:
                exctype , value , tb = sys.exc_info()
                exc_infos = ExcractException(exctype,value,tb)
                if self.logger is not None:
                    if self.fatalError == False:
                       self.logger.error(exc_infos)
                       return
                    else:
                        self.logger.fatal(exc_infos)
                        return
                else:
                    print(exc_infos)
                    return
        return wrapper