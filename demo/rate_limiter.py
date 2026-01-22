import sys
import os
import time

# Add parent directory to path to import easy_redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_redis import EasyRedis


def is_rate_limited(app, user_id, max_requests=5, window_seconds=10):
    """
    Simple rate limiter: max_requests per window_seconds.
    Returns True if rate limited, False if allowed.
    """
    key = f"rate_limit_{user_id}"

    # Get current request count
    current = app.load(key)

    if current is None:
        # First request in this window
        app.save(key, "1", expire_seconds=window_seconds)
        return False

    count = int(current)
    if count >= max_requests:
        return True  # Rate limited!

    # Increment counter
    app.save(key, str(count + 1))
    return False


def main():
    print("--- Rate Limiter Demo ---")
    print("Limits users to 5 requests per 10 seconds\n")

    # Initialize EasyRedis and connect to "rate_limiter_app" namespace
    redis = EasyRedis()
    app = redis.app("rate_limiter_app")

    user_id = "user_456"

    # Simulate 7 rapid requests
    print("Simulating 7 rapid requests from the same user:\n")

    for i in range(1, 8):
        is_limited = is_rate_limited(app, user_id, max_requests=5, window_seconds=10)

        if is_limited:
            print(f"Request {i}: ❌ BLOCKED (rate limit exceeded)")
        else:
            print(f"Request {i}: ✓ ALLOWED")

        time.sleep(0.5)  # Small delay between requests

    # Check TTL
    key = f"rate_limit_{user_id}"
    ttl = app.get_ttl(key)
    if ttl > 0:
        print(f"\nRate limit resets in {ttl} seconds")

    # Wait for window to reset
    print(f"\nWaiting {ttl + 1} seconds for rate limit to reset...")
    time.sleep(ttl + 1)

    print("\nAfter rate limit window reset:")
    is_limited = is_rate_limited(app, user_id, max_requests=5, window_seconds=10)
    if not is_limited:
        print("Request: ✓ ALLOWED (rate limit has reset)")

    # Cleanup
    app.delete(key)


if __name__ == "__main__":
    main()
