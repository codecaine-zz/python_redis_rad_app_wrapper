# EasyRedis

Dead-simple Redis wrapper for RAD (Rapid Application Development) apps. Just create it, pick your app name, and go.

EasyRedis provides a clean, namespaced interface for Redis, making it easy to manage data for multiple applications or components within the same Redis instance without key collisions.

## Features

- **Namespace Isolation**: Automatically namespaces keys with your app name (e.g., `myapp:mykey`).
- **Simplified API**: Easy methods for handling strings, dictionaries, and lists.
- **Automatic String Decoding**: Returns Python strings instead of bytes.
- **Built-in Expiration**: Easy TTL (Time To Live) support for all data types.

## Installation

### From Source

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### As a Package

You can install EasyRedis as a package in your Python environment:

```bash
# Development installation (editable)
pip install -e .

# Or regular installation
pip install .
```

### For Development

Install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from easy_redis import EasyRedis

# 1. Connect to Redis (defaults to localhost:6379)
db = EasyRedis()

# 2. Create a namespaced "app"
# All keys saved here will start with "auth:"
sessions = db.app("auth")

# 3. Store data
sessions.save("user_token", "abc-123", expire_seconds=3600)

# 4. Store dictionaries
sessions.save_dict("user:42", {
    "name": "Alice",
    "role": "admin"
}, expire_seconds=1800)

# 5. Retrieve data
token = sessions.load("user_token")
user_info = sessions.load_dict("user:42")

print(f"Token: {token}")
print(f"User: {user_info}")
```

## Demo Applications

The `demo/` folder contains beginner-friendly examples demonstrating common use cases:

- **counter_app.py** - Basic counters and expiration (page views, temporary tokens)
- **task_queue.py** - Task queue/todo list management
- **user_session.py** - User session and profile storage
- **cache_demo.py** - Data caching patterns for performance
- **rate_limiter.py** - API rate limiting protection
- **leaderboard.py** - Game leaderboard and score tracking
- **notification_queue.py** - Notification system and messaging
- **config_settings.py** - Configuration management and feature flags

Each demo is a standalone script you can run directly:

```bash
python demo/counter_app.py
```

See [demo/README.md](demo/README.md) for detailed descriptions and usage instructions for each example.

## Running Tests

This project uses `pytest` for testing. Ensure you have a Redis instance running locally on port 6379 before running tests.

Run the tests with:

```bash
pytest
```

---

## API Documentation

### `class EasyRedis`

The main entry point for the library.

#### `__init__(host="localhost", port=6379, password=None)`

Connect to Redis.

- **Parameters**:
  - `host` (str): Redis host address.
  - `port` (int): Redis port number.
  - `password` (str): Redis password (optional).

#### `app(app_name) -> AppSpace`

Create a namespace for your specific application or component.

- **Parameters**:
  - `app_name` (str): The prefix to use for all keys (e.g., "myapp").
- **Returns**: An `AppSpace` instance.

---

### `class AppSpace`

Represents a namespaced section of Redis. All keys operated on by an `AppSpace` instance are automatically prefixed with `app_name:`.

#### Basic Values

- **`save(name, value, expire_seconds=None)`**
  Save a simple string value.
  - `name`: The key name (will be prefixed).
  - `value`: The string value to save.
  - `expire_seconds` (optional): Auto-delete after this many seconds.

- **`load(name) -> str | None`**
  Load a value.
  - Returns `None` if the key does not exist.

- **`delete(name)`**
  Delete a value.

- **`exists(name) -> bool`**
  Check if a key exists.

#### Dictionaries (Maps)

- **`save_dict(name, data, expire_seconds=None)`**
  Save a dictionary (hash).
  - `name`: The key name.
  - `data` (dict): The dictionary to save.
  - `expire_seconds` (optional): Auto-delete after this many seconds.

- **`load_dict(name) -> dict`**
  Load a dictionary.
  - Returns an empty dict `{}` if not found.

#### Lists

- **`add_to_list(name, *values, expire_seconds=None)`**
  Append items to the end of a list.
  - `name`: The key name.
  - `*values`: One or more items to add.
  - `expire_seconds` (optional): Update expiration for the list.

- **`get_list(name) -> list`**
  Get all items in a list.
  - Returns an empty list `[]` if not found.

- **`clear_list(name)`**
  Remove all items from a list (deletes the key).

#### Expiration & TTL

- **`get_ttl(name) -> int`**
  Get remaining seconds until key expires.
  - Returns `> 0`: Seconds remaining.
  - Returns `-1`: Key exists but has no expiration (permanent).
  - Returns `-2`: Key does not exist.

- **`set_expire(name, seconds) -> bool`**
  Set or update expiration on an existing key.
  - Returns `True` if set, `False` if key didn't exist.

- **`remove_expire(name) -> bool`**
  Make a key permanent (remove expiration).
  - Returns `True` if removed, `False` if key didn't exist.

#### Utility

- **`list_all() -> list[str]`**
  List all keys in this namespace.
  - Returns a list of key names (with the app prefix removed).

- **`delete_all() -> int`**
  Delete all keys in this namespace.
  - Returns the number of keys deleted.
