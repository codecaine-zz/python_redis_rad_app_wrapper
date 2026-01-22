from easy_redis import EasyRedis
import time


def main():
    print("=" * 60)
    print("EasyRedis Complete API Demo")
    print("=" * 60)

    # Initialize EasyRedis
    db = EasyRedis()
    app = db.app("demo_app")

    # Clean slate for demo
    print("\n🧹 Cleaning up any existing keys...")
    deleted = app.delete_all()
    if deleted > 0:
        print(f"   Deleted {deleted} existing keys")
    print("   Ready!\n")

    # ========== 1. Simple Key-Value Operations ==========
    print("1️⃣  SIMPLE KEY-VALUE OPERATIONS")
    print("-" * 60)

    # save() - Save a simple value
    app.save("username", "alice_2026")
    print("✓ Saved username: alice_2026")

    # load() - Load a value
    loaded_username = app.load("username")
    print(f"✓ Loaded username: {loaded_username}")

    # exists() - Check if key exists
    if app.exists("username"):
        print("✓ Username key exists")

    # Save with expiration
    app.save("temp_token", "TOKEN_XYZ", expire_seconds=5)
    print("✓ Saved temp_token with 5 second expiration")

    # get_ttl() - Get time to live
    ttl = app.get_ttl("temp_token")
    print(f"✓ Token expires in {ttl} seconds")

    # ========== 2. Dictionary Operations ==========
    print("\n2️⃣  DICTIONARY OPERATIONS")
    print("-" * 60)

    # save_dict() - Save structured data
    user_profile = {
        "user_id": "42",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "role": "admin",
        "credits": "1000",
    }
    app.save_dict("user_42", user_profile, expire_seconds=3600)
    print("✓ Saved user profile dictionary")

    # load_dict() - Load structured data
    loaded_profile = app.load_dict("user_42")
    print(f"✓ Loaded user profile: {loaded_profile['name']} ({loaded_profile['role']})")
    print(f"  Email: {loaded_profile['email']}, Credits: {loaded_profile['credits']}")

    # Update dictionary
    loaded_profile["credits"] = "1500"
    loaded_profile["last_login"] = "2026-01-22"
    app.save_dict("user_42", loaded_profile)
    print("✓ Updated user credits to 1500")

    # ========== 3. List Operations ==========
    print("\n3️⃣  LIST OPERATIONS")
    print("-" * 60)

    # add_to_list() - Add items to a list
    app.add_to_list("todo_list", "Write documentation", "Fix bug #123")
    print("✓ Added 2 tasks to todo list")

    app.add_to_list("todo_list", "Review pull request", "Deploy to production")
    print("✓ Added 2 more tasks")

    # get_list() - Retrieve all items
    todos = app.get_list("todo_list")
    print(f"✓ Todo list has {len(todos)} items:")
    for i, task in enumerate(todos, 1):
        print(f"  [{i}] {task}")

    # List with expiration
    app.add_to_list(
        "recent_activity", "User logged in", "Updated profile", expire_seconds=10
    )
    print("✓ Added recent activity with 10 second expiration")

    # ========== 4. Expiration Management ==========
    print("\n4️⃣  EXPIRATION MANAGEMENT")
    print("-" * 60)

    # Save without expiration
    app.save("permanent_key", "This persists forever")
    print("✓ Saved permanent key (no expiration)")

    # set_expire() - Add expiration to existing key
    result = app.set_expire("permanent_key", 15)
    if result:
        print("✓ Added 15 second expiration to permanent key")

    # Check TTL
    ttl = app.get_ttl("permanent_key")
    print(f"✓ Permanent key now expires in {ttl} seconds")

    # remove_expire() - Make key permanent again
    result = app.remove_expire("permanent_key")
    if result:
        print("✓ Removed expiration - key is permanent again")

    # Verify no expiration
    ttl = app.get_ttl("permanent_key")
    if ttl == -1:
        print("✓ Confirmed: key has no expiration")

    # ========== 5. Key Management ==========
    print("\n5️⃣  KEY MANAGEMENT")
    print("-" * 60)

    # list_all() - Show all keys in this app namespace
    all_keys = app.list_all()
    print(f"✓ Total keys in 'demo_app' namespace: {len(all_keys)}")
    print(f"  Keys: {', '.join(all_keys)}")

    # exists() - Check multiple keys
    print("\n✓ Checking key existence:")
    for key in ["username", "user_42", "todo_list", "nonexistent_key"]:
        status = "EXISTS" if app.exists(key) else "NOT FOUND"
        print(f"  {key}: {status}")

    # delete() - Remove specific keys
    app.delete("permanent_key")
    print("\n✓ Deleted permanent_key")

    # clear_list() - Remove entire list
    app.clear_list("todo_list")
    print("✓ Cleared todo_list")

    # ========== 6. Expiration Demo ==========
    print("\n6️⃣  EXPIRATION DEMO (waiting for keys to expire)")
    print("-" * 60)

    # Check temp_token status
    if app.exists("temp_token"):
        print("⏳ temp_token still exists...")
        ttl = app.get_ttl("temp_token")
        print(f"   Waiting {ttl + 1} seconds for it to expire...")
        time.sleep(ttl + 1)

    if not app.exists("temp_token"):
        print("✓ temp_token has expired and been auto-deleted")

    # ========== 7. Multiple Namespaces ==========
    print("\n7️⃣  MULTIPLE APP NAMESPACES")
    print("-" * 60)

    # Different apps with same key names won't conflict
    app1 = db.app("app_one")
    app2 = db.app("app_two")

    app1.save("counter", "100")
    app2.save("counter", "200")

    print(f"✓ app_one counter: {app1.load('counter')}")
    print(f"✓ app_two counter: {app2.load('counter')}")
    print("✓ Keys are isolated in separate namespaces")

    # ========== 8. Final Summary ==========
    print("\n8️⃣  FINAL SUMMARY")
    print("-" * 60)

    # Show remaining keys
    remaining_keys = app.list_all()
    print(f"✓ Keys remaining in 'demo_app': {len(remaining_keys)}")
    for key in remaining_keys:
        ttl = app.get_ttl(key)
        if ttl > 0:
            print(f"  {key} (expires in {ttl}s)")
        elif ttl == -1:
            print(f"  {key} (permanent)")
        else:
            print(f"  {key} (expired)")

    # Cleanup
    print("\n🧹 Cleaning up demo keys...")
    deleted_demo = app.delete_all()
    print(f"✓ Deleted {deleted_demo} keys from 'demo_app'")

    deleted_app1 = app1.delete_all()
    print(f"✓ Deleted {deleted_app1} keys from 'app_one'")

    deleted_app2 = app2.delete_all()
    print(f"✓ Deleted {deleted_app2} keys from 'app_two'")

    print("\n" + "=" * 60)
    print("✅ Demo Complete! All EasyRedis API methods demonstrated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
