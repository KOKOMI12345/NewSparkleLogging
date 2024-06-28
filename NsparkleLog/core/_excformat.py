import traceback , sys , threading ,multiprocessing
from typing import Optional

def format_stack_trace(exctype, value, tb, nested: bool = False,stackTraceMode: bool = False) -> str:
    tb_list = traceback.extract_tb(tb)

    if nested:
        exception_info = f"{exctype.__name__}: {value}\n"
    else:
        if not stackTraceMode:
            exception_info = f"Exception in process: {multiprocessing.current_process().name}, thread: {threading.current_thread().name}; {exctype.__name__}: {value}\n"
            exception_info += "Traceback (most recent call last):\n"
        else:
            exception_info = f"This is just a stack trace\n"
            exception_info += "Traceback (most recent call last):\n"

    for filename, lineno, funcname, line in tb_list:
        exception_info += f"  at {funcname} in ({filename}:{lineno})\n"
    
    # 检查是否有原因和其他信息
    cause = getattr(value, '__cause__', None)
    context = getattr(value, '__context__', None)
    
    if cause:
        exception_info += "Caused by: "
        exception_info += format_stack_trace(type(cause), cause, cause.__traceback__, nested=True)
    if context and not cause:
        exception_info += "original exception: "
        exception_info += format_stack_trace(type(context), context, context.__traceback__, nested=True)
    
    return exception_info

def ExtractException(exctype: type, e, tb) -> Optional[str]:
    # 获取回溯信息并格式化为字符串
    tb_str = format_stack_trace(exctype, e, tb)
    
    # 记录异常信息到日志
    exception_info = "发生异常:\n"
    exception_info += tb_str
    return exception_info

def GetStackTrace(vokeInfo: str = "in") -> str:
    """
    获取堆栈跟踪信息
    参数:
        vokeInfo: str
            指定获取堆栈跟踪的调用信息
            'in': 获取当前调用栈信息的前两层
            'out': 获取当前调用栈信息的前一层
    """
    try:
        raise Exception("获取堆栈跟踪")
    except Exception:
        # 获取当前调用栈信息的前两层
        stack = traceback.extract_stack(limit=3)
        stack_trace = "Stack Trace:\n"
        if vokeInfo == "in":
            for frame in stack[:-2]:
                func_name = frame.name
                file_name = frame.filename
                line_no = frame.lineno
                stack_trace += f"   at {func_name} in ({file_name}:{line_no})\n"
        elif vokeInfo == "out":
            for frame in stack[:-1]:
                func_name = frame.name
                file_name = frame.filename
                line_no = frame.lineno
                stack_trace += f"   at {func_name} in ({file_name}:{line_no})\n"
        else:
            raise ValueError("参数vokeInfo只能为'in'或'out'")
        return stack_trace