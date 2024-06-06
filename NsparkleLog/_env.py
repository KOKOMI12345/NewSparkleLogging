import threading , multiprocessing

default_format = "{localtime}.{msec:03d} | {level:<7} | {ProcessName}.{threadName} | {name}.{funcName} | {filename}:{lineno} - {message}"

allowed_lock_type = type(threading.Lock()) , type(multiprocessing.Lock())