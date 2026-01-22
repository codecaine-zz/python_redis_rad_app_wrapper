import sys
import os
import time

# Add parent directory to path to import easy_redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_redis import EasyRedis


def expensive_database_query(user_id):
    """Simulates a slow database query"""
    print(f"  [Simulating expensive database query for user {user_id}...]")
    time.sleep(2)  # Simulate 2 second delay
    return {
        "id": user_id,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "credits": "1000",
    }


def main():
    print("--- Simple Cache Demo ---")
    print("This demonstrates caching expensive operations with Redis\n")

    # Initialize EasyRedis and connect to "cache_app" namespace
    redis = EasyRedis()
    app = redis.app("cache_app")

    user_id = "user_123"
    cache_key = f"user_profile_{user_id}"

    # First request - cache miss
    print("1. First request (cache miss):")
    start_time = time.time()

    cached_data = app.load_dict(cache_key)
    if not cached_data:
        print("  Cache MISS - fetching from database...")
        user_data = expensive_database_query(user_id)

        # Cache the result for 5 minutes (300 seconds)
        app.save_dict(cache_key, user_data, expire_seconds=300)
        print(f"  Cached for 5 minutes")
    else:
        print("  Cache HIT - loaded from Redis")
        user_data = cached_data

    elapsed = time.time() - start_time
    print(f"  Response time: {elapsed:.2f} seconds")
    print(f"  User data: {user_data}\n")

    # Second request - cache hit
    print("2. Second request (cache hit):")
    start_time = time.time()

    cached_data = app.load_dict(cache_key)
    if not cached_data:
        print("  Cache MISS - fetching from database...")
        user_data = expensive_database_query(user_id)
        app.save_dict(cache_key, user_data, expire_seconds=300)
    else:
        print("  Cache HIT - loaded from Redis")
        user_data = cached_data

    elapsed = time.time() - start_time
    print(f"  Response time: {elapsed:.2f} seconds")
    print(f"  User data: {user_data}\n")

    # Check cache expiration time
    ttl = app.get_ttl(cache_key)
    print(f"3. Cache expires in {ttl} seconds")

    # Optional: Clear cache
    print("\n4. Clearing cache for demo cleanup...")
    app.delete(cache_key)
    print("  Cache cleared!")


if __name__ == "__main__":
    main()
