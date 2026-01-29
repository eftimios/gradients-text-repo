import json 
import os
import redis

STATE_KEY = "state"

def _get_redis_client() -> redis.Redis:
    """Get a Redis client connection with configuration from environment variables."""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    password = os.getenv("REDIS_PASSWORD", None)
    db = int(os.getenv("REDIS_DB", 0))
    
    return redis.Redis(
        host=host,
        port=port,
        password=password,
        db=db,
        decode_responses=True,
        socket_timeout=5,
        socket_connect_timeout=5
    )


def get_state() -> dict:
    """return the json.loads(value of STATE_KEY in redis)"""
    try:
        client = _get_redis_client()
        value = client.get(STATE_KEY)
        
        if value is None:
            return {}
        
        return json.loads(value)
    except (json.JSONDecodeError, redis.ConnectionError, redis.TimeoutError, Exception):
        return {}


def set_state(state: dict) -> None:
    """set the value of STATE_KEY in redis to the state"""
    try:
        client = _get_redis_client()
        json_value = json.dumps(state)
        client.set(STATE_KEY, json_value)
    except (redis.ConnectionError, redis.TimeoutError, Exception):
        pass


def test():
    state = get_state()
    print(json.dumps(state, indent=4, ensure_ascii=False))
    
if __name__ == "__main__":
    test()