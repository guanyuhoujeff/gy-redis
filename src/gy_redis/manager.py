import redis
from typing import Optional, Union

from .handler import (
    RedisConnector, 
    RedisDictHander,
    RedisImageHander,
    RedisBytesHander
)
         
class RedisManager(object):
    ## python SingleTon
    _instance = None 
    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance
    
    def __init__(self, redis_client: Union[redis.Redis, redis.Sentinel], sentinel_name : Optional[str]=None):
        """管理redis handler 的 manager

        Args:
            redis_client (Union[redis.Redis, redis.Sentinel]): 可以給官方（redis-py）的一般redis 或哨兵模式的redis
            sentinel_name (Optional[str], optional): 如果是給哨兵模式的redis，就要給sentinel_name . Defaults to None.
        """
        self._redis_client = RedisConnector(redis_client)
    
    def makeDictHandler(self, topic : str) -> RedisDictHander:
        return RedisDictHander(self._redis_client, topic)

    def makeImageHandler(self, topic : str) -> RedisImageHander:
        return RedisImageHander(self._redis_client, topic)

    def makeBytesHandler(self, topic : str) -> RedisBytesHander:
        return RedisBytesHander(self._redis_client, topic)
