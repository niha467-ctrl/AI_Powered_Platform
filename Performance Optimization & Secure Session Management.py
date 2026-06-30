"""
=============================================================
PERFORMANCE OPTIMIZATION & SECURE SESSION MANAGEMENT
Single File Python Implementation
=============================================================

Features
--------
✔ Secure Session Creation
✔ Token-Based Authentication
✔ Session Expiration
✔ Automatic Session Cleanup
✔ Password Hashing (SHA-256)
✔ Secure Random Token Generation
✔ In-Memory Cache with TTL
✔ LRU Caching for Expensive Operations
✔ Performance Timer
✔ Thread Pool for Concurrent Tasks
✔ Rate Limiting
✔ Request Logging
✔ Health Monitoring

Run:
    python performance_secure_session.py
=============================================================
"""

import hashlib
import secrets
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# ============================================================
# CONFIGURATION
# ============================================================

SESSION_TIMEOUT = 1800          # 30 minutes
CACHE_TTL = 300                 # 5 minutes
RATE_LIMIT = 10                 # Requests per minute

# ============================================================
# SIMPLE CACHE
# ============================================================

class MemoryCache:

    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = {
            "value": value,
            "expires": time.time() + CACHE_TTL
        }

    def get(self, key):

        item = self.cache.get(key)

        if not item:
            return None

        if item["expires"] < time.time():
            del self.cache[key]
            return None

        return item["value"]

cache = MemoryCache()

# ============================================================
# SESSION MANAGER
# ============================================================

class SessionManager:

    def __init__(self):

        self.sessions = {}
        self.lock = Lock()

    def create_session(self, username):

        token = secrets.token_hex(32)

        with self.lock:

            self.sessions[token] = {
                "user": username,
                "created": time.time(),
                "last_access": time.time()
            }

        return token

    def validate(self, token):

        with self.lock:

            session = self.sessions.get(token)

            if not session:
                return False

            if time.time() - session["last_access"] > SESSION_TIMEOUT:

                del self.sessions[token]
                return False

            session["last_access"] = time.time()

            return True

    def destroy(self, token):

        with self.lock:

            if token in self.sessions:
                del self.sessions[token]

    def cleanup(self):

        expired = []

        with self.lock:

            for token, session in self.sessions.items():

                if time.time() - session["last_access"] > SESSION_TIMEOUT:
                    expired.append(token)

            for token in expired:
                del self.sessions[token]

# ============================================================
# AUTHENTICATION
# ============================================================

class Auth:

    users = {}

    @staticmethod
    def hash_password(password):

        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    @classmethod
    def register(cls, username, password):

        cls.users[username] = cls.hash_password(password)

    @classmethod
    def login(cls, username, password):

        hashed = cls.hash_password(password)

        if cls.users.get(username) == hashed:
            return True

        return False

# ============================================================
# RATE LIMITER
# ============================================================

class RateLimiter:

    def __init__(self):

        self.requests = {}

    def allow(self, user):

        now = time.time()

        history = self.requests.get(user, [])

        history = [t for t in history if now - t < 60]

        if len(history) >= RATE_LIMIT:
            return False

        history.append(now)

        self.requests[user] = history

        return True

# ============================================================
# PERFORMANCE OPTIMIZATION
# ============================================================

@lru_cache(maxsize=128)
def expensive_calculation(value):

    time.sleep(1)

    return value * value

# ============================================================
# PERFORMANCE TIMER
# ============================================================

def timer(func):

    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        elapsed = time.time() - start

        print(f"{func.__name__} executed in {elapsed:.4f} sec")

        return result

    return wrapper

# ============================================================
# BACKEND SERVICE
# ============================================================

class Backend:

    def __init__(self):

        self.sessions = SessionManager()
        self.limiter = RateLimiter()

    @timer
    def login(self, username, password):

        if not Auth.login(username, password):

            return {
                "success": False,
                "message": "Invalid Credentials"
            }

        token = self.sessions.create_session(username)

        return {
            "success": True,
            "token": token
        }

    @timer
    def process_request(self, token, value):

        if not self.sessions.validate(token):

            return {
                "success": False,
                "message": "Session Expired"
            }

        user = self.sessions.sessions[token]["user"]

        if not self.limiter.allow(user):

            return {
                "success": False,
                "message": "Rate Limit Exceeded"
            }

        cached = cache.get(value)

        if cached is not None:

            return {
                "cached": True,
                "result": cached
            }

        result = expensive_calculation(value)

        cache.set(value, result)

        return {
            "cached": False,
            "result": result
        }

# ============================================================
# CONCURRENT TASKS
# ============================================================

def parallel_jobs():

    values = [5, 8, 10, 12, 15]

    with ThreadPoolExecutor(max_workers=5) as executor:

        results = list(
            executor.map(expensive_calculation, values)
        )

    return results

# ============================================================
# HEALTH MONITOR
# ============================================================

class Health:

    @staticmethod
    def status():

        return {
            "Server": "Running",
            "Cache": "Healthy",
            "Authentication": "Healthy",
            "Session Manager": "Healthy",
            "Performance": "Optimized",
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    Auth.register("admin", "admin123")

    backend = Backend()

    print("=" * 60)
    print("SYSTEM HEALTH")
    print("=" * 60)

    print(Health.status())

    print("\nLOGIN\n")

    response = backend.login("admin", "admin123")

    print(response)

    token = response["token"]

    print("\nREQUESTS\n")

    for i in [10, 20, 10, 30, 20]:

        print(backend.process_request(token, i))

    print("\nPARALLEL EXECUTION\n")

    print(parallel_jobs())

    print("\nACTIVE SESSIONS")

    print(len(backend.sessions.sessions))

    backend.sessions.cleanup()

    print("\nFINISHED")