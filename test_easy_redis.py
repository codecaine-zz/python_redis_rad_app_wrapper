import pytest
import redis
from easy_redis import EasyRedis, AppSpace


@pytest.fixture
def redis_client():
    """Fixture to create a Redis client for testing."""
    client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    yield client
    # Cleanup: flush test keys after each test
    client.flushdb()


@pytest.fixture
def easy_redis():
    """Fixture to create an EasyRedis instance."""
    er = EasyRedis()
    yield er
    # Cleanup
    er.client.flushdb()


@pytest.fixture
def app_space(easy_redis):
    """Fixture to create an AppSpace instance for testing."""
    return easy_redis.app("test_app")


class TestEasyRedis:
    """Test the EasyRedis class."""

    def test_init_default_params(self):
        """Test EasyRedis initialization with default parameters."""
        er = EasyRedis()
        assert er.client is not None
        assert isinstance(er.client, redis.Redis)
        er.client.flushdb()

    def test_init_custom_params(self):
        """Test EasyRedis initialization with custom parameters."""
        er = EasyRedis(host="localhost", port=6379, password=None)
        assert er.client is not None
        er.client.flushdb()

    def test_app_returns_appspace(self, easy_redis):
        """Test that app() method returns an AppSpace instance."""
        app = easy_redis.app("my_app")
        assert isinstance(app, AppSpace)
        assert app.app_name == "my_app"

    def test_decode_responses(self, easy_redis):
        """Test that decode_responses is enabled."""
        # Set a value and ensure it's returned as string, not bytes
        easy_redis.client.set("test_key", "test_value")
        value = easy_redis.client.get("test_key")
        assert isinstance(value, str)
        assert value == "test_value"


class TestAppSpace:
    """Test the AppSpace class."""

    def test_key_generation(self, app_space):
        """Test that _key() properly namespaces keys."""
        key = app_space._key("mykey")
        assert key == "test_app:mykey"

    def test_save_and_load(self, app_space):
        """Test saving and loading simple values."""
        app_space.save("username", "john_doe")
        value = app_space.load("username")
        assert value == "john_doe"

    def test_load_nonexistent_key(self, app_space):
        """Test loading a key that doesn't exist."""
        value = app_space.load("nonexistent")
        assert value is None

    def test_save_with_expiration(self, app_space):
        """Test saving a value with expiration time."""
        app_space.save("temp_token", "abc123", expire_seconds=2)
        assert app_space.exists("temp_token")
        ttl = app_space.get_ttl("temp_token")
        assert ttl > 0
        assert ttl <= 2

    def test_delete(self, app_space):
        """Test deleting a value."""
        app_space.save("to_delete", "value")
        assert app_space.exists("to_delete")
        app_space.delete("to_delete")
        assert not app_space.exists("to_delete")

    def test_exists_true(self, app_space):
        """Test exists() returns True for existing key."""
        app_space.save("existing", "value")
        assert app_space.exists("existing") is True

    def test_exists_false(self, app_space):
        """Test exists() returns False for non-existing key."""
        assert app_space.exists("nonexistent") is False

    def test_save_dict(self, app_space):
        """Test saving a dictionary."""
        user_data = {"name": "Alice", "age": "30", "city": "NYC"}
        app_space.save_dict("user_42", user_data)
        loaded = app_space.load_dict("user_42")
        assert loaded == user_data

    def test_load_dict_nonexistent(self, app_space):
        """Test loading a dictionary that doesn't exist."""
        loaded = app_space.load_dict("nonexistent_dict")
        assert loaded == {}

    def test_save_dict_with_expiration(self, app_space):
        """Test saving a dictionary with expiration."""
        data = {"key": "value"}
        app_space.save_dict("temp_dict", data, expire_seconds=2)
        assert app_space.exists("temp_dict")
        ttl = app_space.get_ttl("temp_dict")
        assert ttl > 0
        assert ttl <= 2

    def test_add_to_list(self, app_space):
        """Test adding items to a list."""
        app_space.add_to_list("todos", "Buy milk", "Walk dog")
        todos = app_space.get_list("todos")
        assert todos == ["Buy milk", "Walk dog"]

    def test_add_to_list_single_item(self, app_space):
        """Test adding a single item to a list."""
        app_space.add_to_list("tasks", "Task 1")
        tasks = app_space.get_list("tasks")
        assert tasks == ["Task 1"]

    def test_add_to_list_multiple_times(self, app_space):
        """Test adding to the same list multiple times."""
        app_space.add_to_list("items", "item1")
        app_space.add_to_list("items", "item2", "item3")
        items = app_space.get_list("items")
        assert items == ["item1", "item2", "item3"]

    def test_get_list_nonexistent(self, app_space):
        """Test getting a list that doesn't exist."""
        items = app_space.get_list("nonexistent_list")
        assert items == []

    def test_add_to_list_with_expiration(self, app_space):
        """Test adding to list with expiration."""
        app_space.add_to_list("temp_list", "item1", expire_seconds=2)
        assert app_space.exists("temp_list")
        ttl = app_space.get_ttl("temp_list")
        assert ttl > 0
        assert ttl <= 2

    def test_clear_list(self, app_space):
        """Test clearing a list."""
        app_space.add_to_list("to_clear", "item1", "item2")
        assert len(app_space.get_list("to_clear")) == 2
        app_space.clear_list("to_clear")
        assert app_space.get_list("to_clear") == []

    def test_get_ttl_with_expiration(self, app_space):
        """Test getting TTL for a key with expiration."""
        app_space.save("key", "value", expire_seconds=10)
        ttl = app_space.get_ttl("key")
        assert ttl > 0
        assert ttl <= 10

    def test_get_ttl_no_expiration(self, app_space):
        """Test getting TTL for a key without expiration."""
        app_space.save("permanent_key", "value")
        ttl = app_space.get_ttl("permanent_key")
        assert ttl == -1

    def test_get_ttl_nonexistent_key(self, app_space):
        """Test getting TTL for a non-existent key."""
        ttl = app_space.get_ttl("nonexistent")
        assert ttl == -2

    def test_set_expire_existing_key(self, app_space):
        """Test setting expiration on an existing key."""
        app_space.save("key", "value")
        result = app_space.set_expire("key", 5)
        assert result is True
        ttl = app_space.get_ttl("key")
        assert ttl > 0
        assert ttl <= 5

    def test_set_expire_nonexistent_key(self, app_space):
        """Test setting expiration on a non-existent key."""
        result = app_space.set_expire("nonexistent", 5)
        assert result is False

    def test_remove_expire(self, app_space):
        """Test removing expiration from a key."""
        app_space.save("key", "value", expire_seconds=10)
        assert app_space.get_ttl("key") > 0
        result = app_space.remove_expire("key")
        assert result is True
        assert app_space.get_ttl("key") == -1

    def test_remove_expire_nonexistent_key(self, app_space):
        """Test removing expiration from a non-existent key."""
        result = app_space.remove_expire("nonexistent")
        assert result is False

    def test_list_all_keys(self, app_space):
        """Test listing all keys for an app."""
        app_space.save("key1", "value1")
        app_space.save("key2", "value2")
        app_space.save_dict("dict1", {"a": "b"})
        all_keys = app_space.list_all()
        assert "key1" in all_keys
        assert "key2" in all_keys
        assert "dict1" in all_keys
        assert len(all_keys) >= 3

    def test_list_all_empty(self, app_space):
        """Test listing keys when app has no keys."""
        all_keys = app_space.list_all()
        assert all_keys == []

    def test_namespace_isolation(self, easy_redis):
        """Test that different app namespaces are isolated."""
        app1 = easy_redis.app("app1")
        app2 = easy_redis.app("app2")

        app1.save("shared_key", "app1_value")
        app2.save("shared_key", "app2_value")

        assert app1.load("shared_key") == "app1_value"
        assert app2.load("shared_key") == "app2_value"

    def test_multiple_operations_sequence(self, app_space):
        """Test a sequence of multiple operations."""
        # Save a value
        app_space.save("counter", "0")
        assert app_space.load("counter") == "0"

        # Save a dict
        app_space.save_dict("user", {"name": "Bob", "age": "25"})
        user = app_space.load_dict("user")
        assert user["name"] == "Bob"

        # Add to list
        app_space.add_to_list("logs", "log1", "log2")
        logs = app_space.get_list("logs")
        assert len(logs) == 2

        # List all keys
        all_keys = app_space.list_all()
        assert len(all_keys) == 3

    def test_update_existing_value(self, app_space):
        """Test updating an existing value."""
        app_space.save("status", "pending")
        assert app_space.load("status") == "pending"

        app_space.save("status", "completed")
        assert app_space.load("status") == "completed"

    def test_update_dict_field(self, app_space):
        """Test updating a dictionary."""
        app_space.save_dict("settings", {"theme": "dark", "lang": "en"})
        app_space.save_dict("settings", {"theme": "light"})
        settings = app_space.load_dict("settings")
        # Note: hset with mapping updates/adds fields, doesn't replace
        assert settings["theme"] == "light"

    def test_empty_list_operations(self, app_space):
        """Test operations on empty lists."""
        # Getting non-existent list returns empty list
        assert app_space.get_list("empty") == []

        # Clearing non-existent list doesn't error
        app_space.clear_list("empty")
        assert app_space.get_list("empty") == []

    def test_expiration_updates(self, app_space):
        """Test that expiration can be updated multiple times."""
        app_space.save("key", "value", expire_seconds=10)
        ttl1 = app_space.get_ttl("key")

        app_space.set_expire("key", 20)
        ttl2 = app_space.get_ttl("key")

        assert ttl2 > ttl1

    def test_set_expire_helper(self, app_space):
        """Test the _set_expire helper method."""
        app_space.save("key", "value")
        app_space._set_expire("key", 5)
        ttl = app_space.get_ttl("key")
        assert ttl > 0
        assert ttl <= 5

    def test_set_expire_helper_none(self, app_space):
        """Test _set_expire with None doesn't set expiration."""
        app_space.save("key", "value")
        app_space._set_expire("key", None)
        ttl = app_space.get_ttl("key")
        assert ttl == -1

    def test_special_characters_in_keys(self, app_space):
        """Test using special characters in key names."""
        app_space.save("key:with:colons", "value1")
        app_space.save("key-with-dashes", "value2")
        app_space.save("key_with_underscores", "value3")

        assert app_space.load("key:with:colons") == "value1"
        assert app_space.load("key-with-dashes") == "value2"
        assert app_space.load("key_with_underscores") == "value3"

    def test_unicode_values(self, app_space):
        """Test storing and retrieving unicode values."""
        app_space.save("unicode", "Hello 世界 🌍")
        value = app_space.load("unicode")
        assert value == "Hello 世界 🌍"

    def test_dict_with_numeric_strings(self, app_space):
        """Test dictionary with numeric string values."""
        data = {"count": "42", "price": "19.99"}
        app_space.save_dict("numbers", data)
        loaded = app_space.load_dict("numbers")
        assert loaded["count"] == "42"
        assert loaded["price"] == "19.99"

    def test_delete_all_empty_namespace(self, app_space):
        """Test delete_all() on empty namespace."""
        deleted = app_space.delete_all()
        assert deleted == 0

    def test_delete_all_single_key(self, app_space):
        """Test delete_all() with a single key."""
        app_space.save("key1", "value1")
        assert app_space.exists("key1")

        deleted = app_space.delete_all()
        assert deleted == 1
        assert not app_space.exists("key1")

    def test_delete_all_multiple_keys(self, app_space):
        """Test delete_all() with multiple keys of different types."""
        # Create multiple keys
        app_space.save("string_key", "value")
        app_space.save_dict("dict_key", {"field": "value"})
        app_space.add_to_list("list_key", "item1", "item2")

        # Verify all exist
        assert len(app_space.list_all()) == 3

        # Delete all
        deleted = app_space.delete_all()
        assert deleted == 3

        # Verify all gone
        assert len(app_space.list_all()) == 0
        assert not app_space.exists("string_key")
        assert not app_space.exists("dict_key")
        assert not app_space.exists("list_key")

    def test_delete_all_namespace_isolation(self, easy_redis):
        """Test that delete_all() only deletes keys in its namespace."""
        app1 = easy_redis.app("app1")
        app2 = easy_redis.app("app2")

        # Add keys to both apps
        app1.save("key1", "value1")
        app1.save("key2", "value2")
        app2.save("key1", "value1")
        app2.save("key2", "value2")

        # Delete all from app1
        deleted = app1.delete_all()
        assert deleted == 2

        # Verify app1 keys are gone but app2 keys remain
        assert len(app1.list_all()) == 0
        assert len(app2.list_all()) == 2
        assert app2.exists("key1")
        assert app2.exists("key2")
