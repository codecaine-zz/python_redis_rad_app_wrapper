import sys
import os

# Add parent directory to path to import easy_redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_redis import EasyRedis


def main():
    print("--- Task Queue / Todo List Demo ---")

    # Initialize EasyRedis and connect to "task_app" namespace
    redis = EasyRedis()
    app = redis.app("task_app")

    list_key = "my_tasks"

    # Clear old list for a fresh demo run
    print("Clearing any existing tasks...")
    app.clear_list(list_key)

    # Add tasks
    print("Adding 3 tasks to the queue...")
    app.add_to_list(list_key, "Email the team", "Update website", "Buy coffee")

    # Retrieve and list tasks
    tasks = app.get_list(list_key)
    print(f"Current tasks in queue ({len(tasks)}):")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

    # Additional task
    print("\nUrgent task comes in...")
    app.add_to_list(list_key, "Fix critical bug")

    # Show updated list
    updated_tasks = app.get_list(list_key)
    print("Updated task list:")
    print(updated_tasks)

    # Clean up (Optional, but good for demos)
    print("\nDemo complete. Clearing list.")
    app.clear_list(list_key)


if __name__ == "__main__":
    main()
