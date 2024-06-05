# NsparkleLog日志库

![Sparkle!](https://github.com/KOKOMI12345/NewSparkleLogging/blob/main/picture_pixiv_116702098_0.jpg)

## 描述

原来SparkleLogging日志库的新版,新的SparkleLogging日志库是从底层开始写起来的,并没有基于logging标准库往上搭建,所以功能暂时不完善。

### Get started

一般来说，你只需要简单的

```python
from NsparkleLog import logger

# 就可以开始记录日志

logger.trace("test")
logger.debug("test")
logger.info("test")
logger.warning("test")
logger.error("test")
logger.fatal("test")
```

[2024/6/5 22:14]

### 更新了类似loguru的catch装饰器

- 现在可以用@logger.catch来捕获函数中的异常并打印堆栈

```python
from NsparkleLog import logger

@logger.catch
def test():
    raise Exception("this is a test exception")

test()
```

```bash
output:

2024-06-05 22:13:03.793 | ERROR   | MainProcess.MainThread | main.wrapper | NsparkleLog\core\_logger.py:60 - 发生异常:
An Fatal Error has occurred: Exception: This is an exception
Traceback (most recent call last):
  at wrapper in (f:\python_play\NsparkleLog\NsparkleLog\core\_logger.py:58)
  at test in (f:\python_play\NsparkleLog\asynctest.py:12)

```

[2024/6/4 21:52]

### 更新trace方法

- trace方法现在支持withStackTrace参数,如果为True,则包含堆栈跟踪,否则只记录信息

```python
from NsparkleLog import logger

logger.trace("This is a trace message",withStackTrace=True)

```

```bash
output:

2024-06-04 21:50:44.840 | TRACE   | MainProcess.MainThread | main.<module> | asynctest.py:3 - This is a trace message
Stack Trace:
   at <module> in (f:\python_play\NsparkleLog\asynctest.py:3)

```

[2024/6/2 14:01]

### 更新了logger.exception接口

```python
from NsparkleLog import logger
    try:
        raise Exception
    except Exception as e:
        logger.exception(e)
```

[2024/6/1 18:51]

### 完善多线程，多进程，异步的安全

[2024/5/30 21:33]

### 日志库不用再需要显示调用close方法来释放资源,主线程退出后会自动释放资源

### 更新了setLevel接口用于设置日志级别过滤

- 同时修复了一个addNewLevel可能会覆盖自己日志库定义等级的bug

```python
from NsparkleLog import logger
from NsparkleLog.core._level import Levels

logger.setLevel(Levels.INFO)

logger.trace("Trace message") # 过滤
logger.debug("Debug message") # 过滤
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.fatal("fatal message")


```

### 添加了addNewLevel方法来提升灵活性

```python
from NsparkleLog import logger

TEST = 25
logger.addNewLevel("test", TEST, 91, "bright_magenta")

logger.log(TEST, "test")
```

### 更新了FileHandler,保证了部分线程安全

```python
from NsparkleLog import logger
from NsparkleLog.core._handler import FileHandler
from NsparkleLog.core._formatter import Formatter

filehandler = FileHandler(filename="test.log", mode="a+")
fmts = Formatter() #懒得设置格式直接这样也行
filehandler.setFormatter(fmts)
logger.addHandler(filehandler)

logger.trace("Trace message")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.fatal("fatal message")

# 别忘了显示调用close方法释放资源
filehandler.close()
```

### close方法写在了logger中，可以直接调用logger.close()方法来释放资源 [depercated]

```python
from NsparkleLog import logger
from NsparkleLog.core._handler import FileHandler
from NsparkleLog.core._formatter import Formatter

filehandler = FileHandler(filename="test.log", mode="a+")
fmts = Formatter()
filehandler.setFormatter(fmts)
logger.addHandler(filehandler)

logger.trace("Trace message")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.fatal("fatal message")

#可以直接调用logger.close()方法释放资源,但是注意
# 这个close方法是释放所有的handler的资源比如线程之类的,如果你想要精确控制时机,最好还是手动调用每个handler的close方法
# fliehandler.close()
logger.close()
```
