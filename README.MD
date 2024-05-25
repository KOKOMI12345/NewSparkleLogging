# SparkleLogging日志库 [new]

![Sparkle!](picture_pixiv_116702098_0.jpg)

## 描述

新的 SparkleLogging日志库是从底层开始写起来的,并没有基于logging标准库往上搭建,所以功能暂时不完善,

# CAUTION

注意，虽然我在需要共享资源的地方使用了 "with lock" 来确保线程安全，但这个日志库是我从底层开始编写的，
我无法绝对保证在多线程、多进程或异步环境中的绝对安全性。如果在特定环境下遇到问题，请务必审慎考虑并进行适当的调整。

# Get started

一般来说，你只需要简单的

```python
from SparkleLogging import logger

# 就可以开始记录日志

logger.trace("test")
logger.debug("test")
logger.info("test")
logger.warning("test")
logger.error("test")
logger.fatal("test")

```

# 更新了setLevel接口用于设置日志级别过滤

- 同时修复了一个addNewLevel可能会覆盖自己日志库定义等级的bug

```python
from SparkleLogging import logger
from SparkleLogging.core._level import Levels

logger.setLevel(Levels.INFO)

logger.trace("Trace message") # 过滤
logger.debug("Debug message") # 过滤
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.fatal("fatal message")

# 添加了addNewLevel方法来提升灵活性
```

```python
from SparkleLogging import logger

TEST = 25
logger.addNewLevel("test", TEST, 91, "bright_magenta")

logger.log(TEST, "test")
```

# 更新了FileHandler,保证了部分线程安全

```python
from SparkleLogging import logger
from SparkleLogging.core._handler import FileHandler
from SparkleLogging.core._formatter import Formatter

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

# close方法写在了logger中，可以直接调用logger.close()方法来释放资源

```python
from SparkleLogging import logger
from SparkleLogging.core._handler import FileHandler
from SparkleLogging.core._formatter import Formatter

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
