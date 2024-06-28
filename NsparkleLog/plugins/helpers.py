import warnings
from typing import Callable, Any, Union , Optional
import inspect

class Deprecated:
    """
    Decorator for deprecated functions.
    - 对弃用函数标记的装饰器

    ### three methods to how to use this decorators
    ### 此装饰器使用的三种方法
    
    - 1. 指定原因(input reason for depercated functions)

    ```
    @Deprecated("this is a test")
    def test1():
        print("test1")
    ```

    - 2. 指定移除版本号(input depercated version)

    ```
    @Deprecated("test",d_version="0.1.0",remove=True)
    def test2():
        print("test2")
    ```
    - 3. 指定新函数名(input new function name)

    ```
    @Deprecated("test", newFuncName="test4")
    def test3():
        print("test3")
    ```
    """
    def __init__(self, 
        reason: str = "no reasons",
        d_version: Optional[str] = None,
        newFuncName: Optional[str] = None,
        remove: bool = False
    ) -> None:
        self.reason = reason
        self.d_version = d_version
        self.newFuncName = newFuncName
        self.remove = remove

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        func_signature = inspect.signature(func)
        
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            formatted_reason = f"Deprecated as {self.reason},"
            formatted_reason += f"Depercated function: {func.__name__}"
            if self.d_version:
                formatted_reason += f", will be removed in version {self.d_version}"
                
            if self.remove:
                warnings.warn(f"{formatted_reason}.", DeprecationWarning, stacklevel=2)
            elif self.newFuncName:
                warnings.warn(f"{formatted_reason}, use {self.newFuncName} instead.", FutureWarning, stacklevel=2)
            else:
                warnings.warn(formatted_reason, DeprecationWarning, stacklevel=2)
                
            return func(*args, **kwargs)
        
        wrapper.__signature__ = func_signature
        return wrapper

if __name__ == "__main__":
    pass