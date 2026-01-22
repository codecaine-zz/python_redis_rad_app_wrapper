import sys
import os
import time

# Add parent directory to path to import easy_redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_redis import EasyRedis


def main():
    print("--- Notification Queue Demo ---")
    print("Simple messaging system using Redis lists\n")

    # Initialize EasyRedis and connect to "notification_app" namespace
    redis = EasyRedis()
    app = redis.app("notification_app")

    inbox_key = "user_inbox_789"

    # Clear previous notifications for demo
    app.clear_list(inbox_key)

    # Simulate sending notifications
    print("1. Sending notifications to user:")
    notifications = [
        "Welcome to our app!",
        "You have a new message from Bob",
        "Your order has shipped",
        "You earned 50 bonus points!",
    ]

    for notif in notifications:
        app.add_to_list(inbox_key, notif)
        print(f"   ✉️  {notif}")
        time.sleep(0.3)

    print()

    # Check notification count
    all_notifications = app.get_list(inbox_key)
    print(f"2. User has {len(all_notifications)} unread notifications\n")

    # Display inbox
    print("3. User's Inbox:")
    for i, notif in enumerate(all_notifications, 1):
        print(f"   [{i}] {notif}")

    # Add urgent notification
    print("\n4. Urgent notification arrives:")
    urgent_msg = "🚨 Security alert: New login detected"
    app.add_to_list(inbox_key, urgent_msg)
    print(f"   {urgent_msg}")

    # Display updated inbox
    print("\n5. Updated Inbox:")
    all_notifications = app.get_list(inbox_key)
    for i, notif in enumerate(all_notifications, 1):
        prefix = "🚨" if "alert" in notif.lower() else "📬"
        print(f"   {prefix} [{i}] {notif}")

    # Simulate reading notifications (clearing them)
    print("\n6. User reads all notifications...")
    time.sleep(1)
    app.clear_list(inbox_key)
    print("   Inbox cleared!")

    # Verify empty
    remaining = app.get_list(inbox_key)
    print(f"\n7. Notifications remaining: {len(remaining)}")


if __name__ == "__main__":
    main()
