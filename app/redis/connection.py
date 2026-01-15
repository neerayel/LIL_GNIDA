import redis

from app.lil_gnida.config import settings

redis_conn = None

def setup_redis_connection():
    redis_server = settings.redis_server
    redis_conn = redis.Redis(host=redis_server["host"], port=redis_server["port"], db=0)
    return redis_conn

