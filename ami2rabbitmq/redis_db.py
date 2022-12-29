import json
import redis
from ami2rabbitmq.exceptions import InvalidKey


class RedisDB():
    _redis = redis.Redis()
    _key_prefix = 'Online:'

    def validate_key(self, key: str) -> bool:
        if not key.startswith(self._key_prefix):
            raise InvalidKey(f'Invalid Key: {key}')
        
        return True

    def get_all_keys(self) -> list:
        return self._redis.keys('Online:*')

    def exists(self, key: str) -> bool:
        return self._redis.exists(key) == 1
    
    def save(self, key: str, valor, ttl=None) -> bool:
        self.validate_key(key)
        return self._redis.set(key, json.dumps(valor), ttl)
    
    def get(self, key: str):
        if self.exists(key):
            return json.loads(self._redis.get(key))
        
        raise redis.exceptions.ResponseError(f'{key} not found')
    
    def delete(self, key: str) -> bool:

        if self.exists(key):
            return self._redis.delete(key)
        
        raise redis.exceptions.ResponseError(f'{key} not found')
    
    def flushall(self) -> None:
        for key in self.get_all_keys():
            self.delete(key)

redis_server = RedisDB()
