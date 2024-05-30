

"""
日志级别定义
"""

class Levels:
    ON = 0
    TRACE = 1
    DEBUG = 2
    INFO = 3
    WARNING = 4
    WARN = WARNING
    ERROR = 5
    FATAL = 6
    CRITICAL = FATAL
    OFF = float("inf")

_levelToName = {
    Levels.TRACE: "TRACE",
    Levels.DEBUG: "DEBUG",
    Levels.INFO: "INFO",
    Levels.WARNING: "WARNING",
    Levels.ERROR: "ERROR",
    Levels.FATAL: "FATAL",
    Levels.OFF: "OFF",
}

_nameToLevel = {v: k for k, v in _levelToName.items()}