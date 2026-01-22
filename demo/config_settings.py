import sys
import os

# Add parent directory to path to import easy_redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_redis import EasyRedis


def main():
    print("--- Application Configuration Demo ---")
    print("Store and manage app settings with Redis\n")

    # Initialize EasyRedis and connect to "config_app" namespace
    redis = EasyRedis()
    app = redis.app("config_app")

    config_key = "app_settings"

    # Save initial configuration
    print("1. Setting up initial application configuration:")
    config = {
        "app_name": "MyAwesomeApp",
        "version": "1.0.0",
        "maintenance_mode": "false",
        "max_upload_size_mb": "100",
        "api_rate_limit": "1000",
        "theme": "dark",
        "debug_mode": "false",
    }

    app.save_dict(config_key, config)
    print("   Configuration saved!\n")

    # Load and display configuration
    print("2. Current Application Settings:")
    loaded_config = app.load_dict(config_key)
    for key, value in sorted(loaded_config.items()):
        print(f"   {key}: {value}")

    # Update a setting
    print("\n3. Enabling maintenance mode...")
    current_config = app.load_dict(config_key)
    current_config["maintenance_mode"] = "true"
    app.save_dict(config_key, current_config)
    print("   Maintenance mode enabled!\n")

    # Check specific setting
    print("4. Checking if maintenance mode is active:")
    config = app.load_dict(config_key)
    is_maintenance = config.get("maintenance_mode") == "true"

    if is_maintenance:
        print("   🚧 App is in MAINTENANCE MODE")
        print("   Users will see a maintenance page")
    else:
        print("   ✓ App is running normally")

    # Update multiple settings
    print("\n5. Deploying new version and changing settings:")
    config = app.load_dict(config_key)
    config["version"] = "1.1.0"
    config["maintenance_mode"] = "false"
    config["debug_mode"] = "true"
    config["theme"] = "light"
    app.save_dict(config_key, config)
    print("   Settings updated!\n")

    # Display final configuration
    print("6. Updated Application Settings:")
    final_config = app.load_dict(config_key)
    for key, value in sorted(final_config.items()):
        print(f"   {key}: {value}")

    # Feature flag example
    print("\n7. Using configuration as feature flags:")
    debug_enabled = final_config.get("debug_mode") == "true"
    if debug_enabled:
        print("   🐛 Debug logging is ENABLED")
    else:
        print("   Debug logging is disabled")

    # List all config keys
    print("\n8. All keys in config namespace:")
    all_keys = app.list_all()
    print(f"   {all_keys}")

    # Cleanup
    print("\n9. Demo complete. Clearing configuration...")
    app.delete(config_key)
    print("   Configuration cleared!")


if __name__ == "__main__":
    main()
