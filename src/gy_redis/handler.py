import redis
import numpy as np
import cv2
from typing import Optional, Union
import json
import abc
from reactivex.subject import BehaviorSubject
import reactivex.operators as ops

class RedisPubsubJob:
    def __init__(self, pub_sub: redis.client.PubSub,  run_in_thread=False) -> None:
        self._pub_sub = pub_sub
        self._run_in_thread = run_in_thread
        self._pub_sub_thread_job : redis.client.PubSubWorkerThread = None
        
        if self._run_in_thread:
            self._pub_sub_thread_job = self._pub_sub.run_in_thread(sleep_time=0.001)
    
    def addPubsubFunction(self, sub_topic, fn):
        self._pub_sub.subscribe(**{sub_topic: fn})

    def start(self):
        if not self._run_in_thread:
            next(self._pub_sub.listen())
        
    def stop(self):
        if self._run_in_thread and not self._pub_sub_thread_job is None:
            self._pub_sub_thread_job.stop()

    @property
    def is_alive(self) -> bool:
        if self._run_in_thread and not self._pub_sub_thread_job is None:
            return self._pub_sub_thread_job.is_alive
        else:
            return False

class RedisConnector:
    ## python SingleTon
    _instance = None 
    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance

    def __init__(self, redis_client: Union[redis.Redis, redis.Sentinel], sentinel_name : Optional[str]=None):
        if isinstance(redis_client, redis.Redis):
            self._master_client = redis_client
            self._slaver_client = redis_client
        elif isinstance(redis_client, redis.Sentinel):
            if sentinel_name is None:
                raise ValueError('if use redis sentinel, sentinel_name_name not be None')
            self._master_client = redis_client.master_for(sentinel_name)
            self._slaver_client = redis_client.slave_for(sentinel_name)
            
    @property
    def master_client(self):
        return self._master_client
    
    @property
    def slaver_client(self):
        return self._slaver_client

    @property
    def topic_list(self): return [
        k.decode() for k in self._master_client.keys()
    ]
    
    def flushall(self):
        self._master_client.flushall()

class RedisHandlerInterface(abc.ABC):
    def __init__(self, redis_client: RedisConnector, topic: str) -> None:
        super().__init__()
        self._redis_client = redis_client
        self._topic = topic
        self._pubsub_job : Optional[RedisPubsubJob] = None
        self._value_subject : BehaviorSubject = BehaviorSubject(None)
        
    @property
    def topic(self):
        return self._topic
    
    @abc.abstractmethod
    def _convertReadValue(self, value):
        pass
    
    @abc.abstractmethod
    def _convertWriteValue(self, value):
        pass
    
    def get(self):
        value = self._redis_client.slaver_client.get(self._topic)
        value = self._convertReadValue(value)
        return value
    
    def set(self, value):
        self._redis_client._master_client.set(self._topic, self._convertWriteValue(value))
    
    def publish(self, value):
        self._redis_client._master_client.publish(self._topic, self._convertWriteValue(value))
    
    def subscribe(self, callback_function, run_in_thread=True):
        """redis 的訂閱模式

        Args:
            callback_function (_type_): 訂閱模式拿到資料可以用的callback
            run_in_thread (bool, optional): 訂閱模式要不要跑在背景. Defaults to True.
        """
        if self._pubsub_job is None:
            self._pubsub_job = RedisPubsubJob(
                pub_sub=self._redis_client.slaver_client.pubsub(ignore_subscribe_messages = True), 
                run_in_thread=run_in_thread
            )
            self._pubsub_job.addPubsubFunction(self.topic, self._value_subject.on_next)
            self._value_subject.pipe(
                ops.filter(lambda value: not value is None),
                ops.map(lambda value: self._convertReadValue(value['data'])),
            ).subscribe(
                on_next=callback_function, 
                on_error=lambda err: print(f'Error {self.topic} ', str(err))
            )
            
        if not run_in_thread:
            self._pubsub_job.start()
    
    def delete(self):
        self._redis_client.master_client.delete(self.topic)

    def stopPubsubJob(self):
        if not self._pubsub_job is None and self._pubsub_job.is_alive:
            self._pubsub_job.stop()
            

class RedisDictHander(RedisHandlerInterface):
    def __init__(self, redis_client: RedisConnector, topic: str) -> None:
        super().__init__(redis_client, topic)
        
    def _convertReadValue(self, value) -> Optional[dict]:
        if isinstance(value, bytes):
            value = json.loads(value.decode())
        else:
            value = None
        return value
        
    def _convertWriteValue(self, value) -> Optional[dict]:
        return json.dumps(value)



class RedisImageHander(RedisHandlerInterface):
    def __init__(self, redis_client: RedisConnector, topic: str) -> None:
        super().__init__(redis_client, topic)
        
    def _convertReadValue(self, value) -> Optional[np.ndarray]:
        if isinstance(value, bytes):
            value =  cv2.imdecode(
                np.frombuffer(value, np.uint8), 
                cv2.IMREAD_COLOR
            )
        else:
            value = None
        return value
        
    def _convertWriteValue(self, value) -> Optional[np.ndarray]:
        return cv2.imencode('.jpg', value)[1].tobytes()



class RedisBytesHander(RedisHandlerInterface):
    def __init__(self, redis_client: RedisConnector, topic: str) -> None:
        super().__init__(redis_client, topic)
        
    def _convertReadValue(self, value) -> Optional[bytes]:
        return value
        
    def _convertWriteValue(self, value) -> Optional[bytes]:
        return value
        
        
        
