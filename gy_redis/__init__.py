import sys

from gy_redis.manager import (
    RedisManager,
    RedisConnector,
    RedisBytesHander,
    RedisDictHander,
    RedisImageHander
)

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


try:
    __version__ = metadata.version("gy_redis")
except metadata.PackageNotFoundError:
    __version__ = "99.99.99"


try:
    VERSION = tuple(map(int_or_str, __version__.split(".")))
except AttributeError:
    VERSION = tuple(99, 99, 99)

__all__ = [
    "RedisManager",
    "RedisConnector",
    "RedisBytesHander",
    "RedisDictHander",
    "RedisImageHander",
]
