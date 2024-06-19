from NsparkleLog.dependencies import threading , asyncio , multiprocessing , Union , Lock

def get_current_lock() -> Union[threading.Lock, asyncio.Lock, Lock]:
    """
    根据当前环境返回适当的锁类型
    """
    # 检测异步环境
    if asyncio.get_event_loop().is_running():
        return asyncio.Lock()
    # 检测多进程环境
    elif (multiprocessing.current_process().name != 'MainProcess' and 
          len(multiprocessing.active_children()) > 1):
        return multiprocessing.Lock()
    # 默认返回线程锁
    else:
        return threading.Lock()