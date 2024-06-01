from NsparkleLog.utils._get_lock import get_current_lock
default_format = "{localtime}.{msec:03d} | {level:<7} | {threadName} | {name}.{funcName} | {filename}:{lineno} - {message}"

current_lock = get_current_lock()