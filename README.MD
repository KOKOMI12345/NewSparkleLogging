# NsparkleLog日志库

![Sparkle!](https://github.com/KOKOMI12345/NewSparkleLogging/blob/main/picture_pixiv_116702098_0.jpg)

## 描述

NsparkleLog 是一个高性能的日志库，设计之初就注重性能和多线程支持。与其他日志库相比，NsparkleLog 在处理大量日志条目时表现出色。

## 性能对比

我们对比了 NsparkleLog 和 Loguru 的性能，结果显示：

- **NsparkleLog**:
  - 总耗时：2.77 秒
  - 平均每条日志耗时：0.000277 秒
- **Loguru**:
  - 总耗时：4.06 秒
  - 平均每条日志耗时：0.000406 秒

这意味着 NsparkleLog 的性能比 Loguru 快约 36%。

## 主要特点

- 多线程支持：使用队列和线程高效处理并发日志记录
- 自定义锁机制：确保线程安全的同时最大化性能
- 从底层实现：避免对第三方库的依赖，进一步优化性能

## 安装

```bash
pip install NsparkleLog
```

## 测试质疑

- 如果您对测试结果感到质疑,可以自己修改下列测试脚本

```python

from NsparkleLog import logger as NsparkleLogger
from loguru import logger as LoguruLogger
import time

# 测试参数
num_messages = 10000
test_message = "This is a test log message."

# 测试 NsparkleLog
nsparkle_times = []
for i in range(num_messages):
    start_time = time.time()
    NsparkleLogger.info(test_message)
    end_time = time.time()
    nsparkle_times.append(end_time - start_time)
nsparkle_duration = sum(nsparkle_times)
nsparkle_avg_time = nsparkle_duration / num_messages

# 测试 Loguru
loguru_times = []
for i in range(num_messages):
    start_time = time.time()
    LoguruLogger.info(test_message)
    end_time = time.time()
    loguru_times.append(end_time - start_time)
loguru_duration = sum(loguru_times)
loguru_avg_time = loguru_duration / num_messages

# 输出结果
print(f"NsparkleLog total duration: {nsparkle_duration:.2f} seconds")
print(f"NsparkleLog average time per message: {nsparkle_avg_time:.6f} seconds")

print(f"Loguru total duration: {loguru_duration:.2f} seconds")
print(f"Loguru average time per message: {loguru_avg_time:.6f} seconds")
```

## 下载总计

[![总下载量:](https://static.pepy.tech/badge/NsparkleLog)](https://pepy.tech/project/NsparkleLog)

[![每月下载量:](https://static.pepy.tech/badge/NsparkleLog/month)](https://pepy.tech/project/NsparkleLog)

[![每周下载量:](https://static.pepy.tech/badge/NsparkleLog/week)](https://pepy.tech/project/NsparkleLog)

### 快速开始

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

[2024/6/28 21:05]

### 修复颜色渲染bug

[2024/6/26 21:32]

### 更新了HTML标签字体渲染

- 用法如下,这里用 cyan 作为示例

```python
from NsparkleLog import logger

logger.trace("<cyan>Hello World</cyan>")
logger.debug("<cyan>Hello World</cyan>")
logger.info("<cyan>Hello World</cyan>")
logger.warning("<cyan>Hello World</cyan>")
logger.error("<cyan>Hello World</cyan>")
logger.fatal("<cyan>Hello World</cyan>")
```

- 你也可以用 Color 类来查看所有自带的颜色

```python
from NsparkleLog import Color

print(Color.GetAvaliableColor())
```

- 当然了,也允许你动态的添加颜色

```python
from NsparkleLog import Color
Color.regColor(50,"test_color")
```

- 如果你有自定义的等级想渲染注册好的颜色或者使用原来的颜色,不要忘了映射噢~

```python
from NsparkleLog import LevelColor , logger

LOGG = 25

logger.addNewLevel("LOGG",LOGG)

LevelColor.mapLevelToColor(LOGG,"cyan")

logger.log(LOGG,"hello world")
```

[2024/6/22 15:26]

### 更新了NsparkleLogHandler类用于转发logging日志消息到NsparkleLog日志库

- 用法如下

```python
from NsparkleLog import NsparkleLogHandler

import logging

logger = logging.getLogger("test")

handler = NsparkleLogHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
```

[2024/6/21 17:26]

### 更新了一个config接口用于配置日志

- 用法

```python
from NsparkleLog import LogManager , Levels , StreamHandler

LogManager.config(
    handlers=[StreamHandler()],
    level=Levels.TRACE,
    colorMode=True,
)

logger = LogManager.GetLogger("test")

logger.trace("Hello, World!")
logger.debug("Hello, World!")
logger.info("Hello, World!")
logger.warning("Hello, World!")
logger.error("Hello, World!")
logger.fatal("Hello, World!")

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

### FileHandler用法

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
```
