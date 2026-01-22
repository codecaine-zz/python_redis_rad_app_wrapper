import sys
import os
import time

# Add parent directory to path to import easy_redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_redis import EasyRedis


def main():
    print("--- Simple Counter Demo ---")

    # Initialize EasyRedis and connect to "counter_app" namespace
    redis = EasyRedis()
    app = redis.app("counter_app")

    # Key for our page view counter
    counter_key = "page_views"

    # Check current value
    current_views = app.load(counter_key)
    if current_views is None:
        print("First time running! Initializing counter to 0.")
        current_views = 0
    else:
        current_views = int(current_views)
        print(f"Current page views: {current_views}")

    # Increment counter
    new_views = current_views + 1
    app.save(counter_key, new_views)
    print(f"Updated page views to: {new_views}")

    # Demonstrate expiration (Temporary access token concept)
    token_key = "temp_access_token_123"
    print(f"\nGeneratring temporary access token: {token_key}")
    app.save(token_key, "ACTIVE", expire_seconds=3)

    print("Token created. Checking status...")
    if app.exists(token_key):
        print("Token is VALID.")

    print("Waiting 4 seconds for token to expire...")
    time.sleep(4)

    if not app.exists(token_key):
        print("Token has EXPIRED as expected.")
    else:
        print("Something went wrong, token still exists!")


if __name__ == "__main__":
    main()
