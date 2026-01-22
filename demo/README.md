# EasyRedis Demo Applications

This folder contains beginner-friendly starter templates demonstrating various use cases with EasyRedis.

## 🚀 Getting Started

Make sure you have Redis running locally:

```bash
redis-server
```

Install dependencies:

```bash
pip install -r ../requirements.txt
```

## 📚 Available Demos

### 1. **counter_app.py** - Simple Counter & Expiration

Learn the basics of saving, loading, and expiring keys.

- Page view counter
- Temporary access tokens with auto-expiration

```bash
python demo/counter_app.py
```

**Key Concepts:** `save()`, `load()`, `exists()`, expiration

---

### 2. **task_queue.py** - Task Queue / Todo List

Manage lists of items with Redis.

- Add tasks to a queue
- Retrieve and display tasks
- Clear completed tasks

```bash
python demo/task_queue.py
```

**Key Concepts:** `add_to_list()`, `get_list()`, `clear_list()`

---

### 3. **user_session.py** - User Session Management

Store structured data like user profiles and sessions.

- Save user information as dictionaries
- Set session expiration times
- Check time-to-live (TTL)

```bash
python demo/user_session.py
```

**Key Concepts:** `save_dict()`, `load_dict()`, `get_ttl()`, `list_all()`

---

### 4. **cache_demo.py** - Data Caching

Speed up your application by caching expensive operations.

- Cache database queries
- Demonstrate cache hits vs misses
- Set cache expiration

```bash
python demo/cache_demo.py
```

**Key Concepts:** Caching patterns, performance optimization

---

### 5. **rate_limiter.py** - Rate Limiting

Protect your API from abuse with rate limiting.

- Limit requests per time window
- Block excessive requests
- Automatic window reset

```bash
python demo/rate_limiter.py
```

**Key Concepts:** Rate limiting patterns, TTL-based counters

---

### 6. **leaderboard.py** - Game Leaderboard

Track and display high scores.

- Store player scores
- Sort and rank players
- Update scores dynamically

```bash
python demo/leaderboard.py
```

**Key Concepts:** Dictionary operations, sorting data

---

### 7. **notification_queue.py** - Notification System

Simple messaging and notification queue.

- Queue notifications for users
- Display inbox contents
- Mark notifications as read

```bash
python demo/notification_queue.py
```

**Key Concepts:** List-based queuing, message systems

---

### 8. **config_settings.py** - Configuration Management

Manage application settings and feature flags.

- Store app configuration
- Update settings dynamically
- Feature flag patterns

```bash
python demo/config_settings.py
```

**Key Concepts:** Configuration management, feature flags

---

## 🎯 Use Cases by Category

### **Data Storage**

- `user_session.py` - Store user data
- `config_settings.py` - App configuration

### **Performance**

- `cache_demo.py` - Speed up with caching
- `rate_limiter.py` - Control request flow

### **Queues & Lists**

- `task_queue.py` - Task management
- `notification_queue.py` - Message queuing

### **Counters & Tracking**

- `counter_app.py` - Simple counters
- `leaderboard.py` - Score tracking

## 💡 Tips for Beginners

1. **Start Simple**: Begin with `counter_app.py` to understand basic operations
2. **Namespace Everything**: Each demo uses its own app namespace (e.g., `app("counter_app")`)
3. **Expiration is Powerful**: Use `expire_seconds` to auto-cleanup old data
4. **Choose the Right Data Type**:
   - Simple values: `save()` / `load()`
   - Structured data: `save_dict()` / `load_dict()`
   - Ordered lists: `add_to_list()` / `get_list()`

## 🛠️ Customization Ideas

Modify these demos to build your own applications:

- **Blog**: Use `cache_demo.py` to cache blog posts
- **Chat App**: Adapt `notification_queue.py` for chat messages
- **API**: Use `rate_limiter.py` to protect your endpoints
- **Game**: Extend `leaderboard.py` with multiplayer features
- **E-commerce**: Use `counter_app.py` for inventory tracking

## 📖 Learn More

Check out the main [README.md](../README.md) for full EasyRedis documentation.
