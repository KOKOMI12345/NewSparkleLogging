import traceback
from typing import Optional

def format_stack_trace(exctype, value, tb, nested=False) -> str:
    tb_list = traceback.extract_tb(tb)
    
    if nested:
        exception_info = f"{exctype.__name__}: {value}\n"
    else:
        exception_info = f"An Fatal Error has occurred: {exctype.__name__}: {value}\n"
        exception_info += "Traceback (most recent call last):\n"

    for filename, lineno, funcname, line in tb_list:
        exception_info += f"  at {funcname} in ({filename}:{lineno})\n"
    
    # 检查是否有原因和其他信息
    cause = getattr(value, '__cause__', None)
    context = getattr(value, '__context__', None)
    
    if cause:
        exception_info += "failure because of: "
        exception_info += format_stack_trace(type(cause), cause, cause.__traceback__, nested=True)
    if context and not cause:
        exception_info += "caught exception: "
        exception_info += format_stack_trace(type(context), context, context.__traceback__, nested=True)
    
    return exception_info

def ExcractException(exctype, value, tb) -> Optional[str]:
    # 获取回溯信息并格式化为字符串
    tb_str = format_stack_trace(exctype, value, tb)
    
    # 记录异常信息到日志
    exception_info = "发生异常:\n"
    exception_info += tb_str
    return exception_info
