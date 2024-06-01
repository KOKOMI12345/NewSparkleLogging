from NsparkleLog.dependencies import threading , asyncio , multiprocessing , Union , Lock

def get_current_lock() -> Union[threading.Lock, asyncio.Lock, Lock]:
    """
    根据不同环境的判断来获取不同的锁 \n
    除非你闲着没事并发调用它,
    否则就不可能出现并发问题！
    """
    thread_lock = threading.Lock()
    asyncio_lock = asyncio.Lock()
    process_lock = multiprocessing.Lock()

    if threading.active_count() > 1:
        return thread_lock
    elif len(multiprocessing.active_children()) > 1:
        return process_lock
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio_lock
    except RuntimeError:
        pass

    return thread_lock