
import warnings
from typing import Callable , Any , Union

class Deprecated:
    def __init__(self, reason: str,d_version: Union[str,None] = None) -> None:
        self.reason = reason
        self.d_version = d_version

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not self.d_version:
               warnings.warn(f"{func.__name__} is deprecated. depercated as {self.reason}", DeprecationWarning,stacklevel=2)
               return func(*args, **kwargs)
            else:
                warnings.warn(f"{func.__name__} is deprecated. depercated as {self.reason}, remove in {self.d_version} future versions", FutureWarning,stacklevel=2)
                return func(*args, **kwargs)
        return wrapper

