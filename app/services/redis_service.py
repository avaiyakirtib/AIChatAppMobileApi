import redis
from app.core.config import settings

# Create a connection pool to Redis
# The `decode_responses=True` ensures that the data we get back is a string, not bytes.
redis_pool = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)

def get_redis_connection():
    """Returns a Redis connection from the pool."""
    return redis.Redis(connection_pool=redis_pool)

def add_token_to_denylist(jti: str, expires_in: int):
    """
    Adds a token's JTI (JWT ID) to the denylist with an expiration time.
    The expiration is a performance optimization to prevent the list from growing indefinitely.
    """
    r = get_redis_connection()
    # We use a key prefix "denylist:" for better organization
    r.set(f"denylist:{jti}", "denylisted", ex=expires_in)

def is_token_denylisted(jti: str) -> bool:
    """
    Checks if a token's JTI is in the denylist.
    """
    r = get_redis_connection()
    return r.exists(f"denylist:{jti}") > 0