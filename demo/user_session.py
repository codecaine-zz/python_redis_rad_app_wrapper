import sys
import os
import pprint

# Add parent directory to path to import easy_redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_redis import EasyRedis


def main():
    print("--- User Session Store Demo ---")

    # Initialize EasyRedis and connect to "session_app" namespace
    redis = EasyRedis()
    app = redis.app("session_app")

    user_id = "user_42"

    # Simulating a user login - storing session data
    user_data = {
        "username": "coder_jane",
        "role": "admin",
        "theme": "dark",
        "last_login": "2023-10-27 10:00:00",
    }

    print(f"Logging in {user_data['username']} (ID: {user_id})...")

    # Save dictionary with a 1 hour expiration (3600 seconds)
    # Using a short expiration here just to show the param,
    # but in real app it might be 30 days etc.
    app.save_dict(user_id, user_data, expire_seconds=3600)

    print("Session saved.")

    # Retrieve the session
    print("\nRetrieving session details...")
    loaded_data = app.load_dict(user_id)

    print("Session Data Loaded:")
    pprint.pprint(loaded_data)

    # Verify specific field
    if loaded_data.get("role") == "admin":
        print("\n>> User is an ADMIN. Access Granted.")
    else:
        print("\n>> User is NOT an admin. Access Denied.")

    # Check TTL
    ttl = app.get_ttl(user_id)
    print(f"Session expires in {ttl} seconds.")

    # List all keys in this app namespace
    print("\nListing all keys in 'session_app':")
    all_keys = app.list_all()
    print(all_keys)


if __name__ == "__main__":
    main()
