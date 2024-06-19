
"""
    ### 支持的格式占位符: 
     - {name}: 日志记录器名字
     - {threadName}: 线程名字
     - {threadId}: 线程ID
     - {filename}: 文件名
     - {pathname}: 文件路径
     - {lineno}: 行号
     - {funcName}: 函数名
     - {moduleName}: 模块名
     - {ProcessId}: 进程ID
     - {ProcessName}: 进程名
     - {message}: 消息
     - {level}: 日志级别
     - {localtime}: 本地时间
     - {msecs}: 本地时间毫秒
     - {utcmsecs}: UTC时间毫秒
     - {utctime}: UTC时间
     - {timestamp}: 时间戳(本地时间)
    """

LOGURU_FMT = "{localtime} | {level} | {name}.{funcName} | {message}"