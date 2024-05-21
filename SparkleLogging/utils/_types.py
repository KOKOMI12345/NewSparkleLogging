from SparkleLogging.dependencies import TypeVar


Level = TypeVar("Level", int,int)
AnyStr = TypeVar("AnyStr", str, bytes,object)
Stream = TypeVar("Stream", str , bytes,object)