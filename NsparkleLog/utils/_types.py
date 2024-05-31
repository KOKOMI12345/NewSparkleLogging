from NsparkleLog.dependencies import TypeVar

Level = TypeVar('Level', int,float)
AnyStr = TypeVar('AnyStr', str, bytes,object)
Stream = TypeVar('Stream', str, bytes,object)