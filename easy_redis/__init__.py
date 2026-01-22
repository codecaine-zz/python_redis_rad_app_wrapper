"""EasyRedis - Dead-simple Redis wrapper for RAD apps."""

import redis
from .__version__ import __version__

__all__ = ["EasyRedis", "AppSpace"]


class EasyRedis:
    """
    Dead-simple Redis wrapper for RAD apps.
    Just create it, pick your app name, and go.
    """

    def __init__(self, host="localhost", port=6379, password=None):
        """Connect to Redis. Works out of the box with defaults."""
        self.client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True,  # Returns strings, not bytes [web:20][web:29]
        )

    def app(self, app_name):
        """Get a simple namespace for your app."""
        return AppSpace(self.client, app_name)


class AppSpace:
    """
    Your app's own Redis space.
    All keys are automatically prefixed with your app name.
    """

    def __init__(self, client, app_name):
        self.client = client
        self.app_name = app_name

    def _key(self, name):
        """Build the namespaced key."""
        return f"{self.app_name}:{name}"

    def _set_expire(self, name, seconds):
        """Helper to set expiration on a key."""
        if seconds:
            self.client.expire(self._key(name), seconds)

    # -------- Save and load simple values --------

    def save(self, name, value, expire_seconds=None):
        """
        Save a value.

        expire_seconds: Auto-delete after this many seconds (optional) [web:36][web:21].
        """
        self.client.set(self._key(name), value, ex=expire_seconds)

    def load(self, name):
        """Load a value. Returns None if not found."""
        return self.client.get(self._key(name))

    def delete(self, name):
        """Delete a value."""
        self.client.delete(self._key(name))

    def exists(self, name):
        """Check if a value exists. Returns True or False."""
        return self.client.exists(self._key(name)) > 0

    # -------- Save and load dictionaries --------

    def save_dict(self, name, data, expire_seconds=None):
        """
        Save a dictionary (like user info, settings, etc).

        expire_seconds: Auto-delete after this many seconds (optional) [web:36][web:40].

        Example: save_dict("user_42", {"name": "Bob", "age": 30}, expire_seconds=3600)
        """
        self.client.hset(self._key(name), mapping=data)
        self._set_expire(name, expire_seconds)

    def load_dict(self, name):
        """
        Load a dictionary. Returns empty dict {} if not found.
        """
        result = self.client.hgetall(self._key(name))
        return result if result else {}

    # -------- Save and load lists --------

    def add_to_list(self, name, *values, expire_seconds=None):
        """
        Add items to a list.

        expire_seconds: Set expiration on the entire list (optional) [web:36][web:40].

        Example: add_to_list("todos", "Buy milk", "Walk dog", expire_seconds=7200)
        """
        self.client.rpush(self._key(name), *values)
        self._set_expire(name, expire_seconds)

    def get_list(self, name):
        """Get all items from a list. Returns empty list [] if not found."""
        return self.client.lrange(self._key(name), 0, -1)

    def clear_list(self, name):
        """Remove all items from a list."""
        self.delete(name)

    # -------- TTL / Expiration helpers --------

    def get_ttl(self, name):
        """
        Get remaining seconds until key expires.

        Returns:
        - Number of seconds remaining [web:35]
        - -1 if key exists but has no expiration
        - -2 if key does not exist
        """
        return self.client.ttl(self._key(name))

    def set_expire(self, name, seconds):
        """
        Set or update expiration on an existing key [web:36][web:38].

        Returns True if expiration was set, False if key doesn't exist.
        """
        result = self.client.expire(self._key(name), seconds)
        return result == 1

    def remove_expire(self, name):
        """
        Remove expiration from a key (make it permanent) [web:36].

        Returns True if expiration was removed, False if key doesn't exist.
        """
        result = self.client.persist(self._key(name))
        return result == 1

    # -------- Utility --------

    def list_all(self):
        """List all keys for this app."""
        pattern = f"{self.app_name}:*"
        return [
            key.replace(f"{self.app_name}:", "") for key in self.client.keys(pattern)
        ]

    def delete_all(self):
        """
        Delete all keys for this app.

        Returns the number of keys deleted.
        """
        pattern = f"{self.app_name}:*"
        keys = self.client.keys(pattern)
        if keys:
            return self.client.delete(*keys)
        return 0
