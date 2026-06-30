# FALLBACK LOGIC IMPLEMENTATION (Single File)

import time
import random
from typing import Any, Callable, List, Dict


# -----------------------------
# Custom Exceptions
# -----------------------------

class PrimaryServiceError(Exception):
    pass

class SecondaryServiceError(Exception):
    pass

class CacheMissError(Exception):
    pass


# -----------------------------
# Fallback Handler Core
# -----------------------------

class FallbackEngine:
    def __init__(self):
        self.logs = []

    # -----------------------------
    # Safe execution wrapper
    # -----------------------------
    def safe_execute(self, func: Callable, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # -----------------------------
    # Primary Service
    # -----------------------------
    def primary_service(self, query: str):
        if random.random() < 0.6:
            raise PrimaryServiceError("Primary service failed")
        return f"Primary response for {query}"

    # -----------------------------
    # Secondary Service
    # -----------------------------
    def secondary_service(self, query: str):
        if random.random() < 0.4:
            raise SecondaryServiceError("Secondary service failed")
        return f"Secondary response for {query}"

    # -----------------------------
    # Cache Layer
    # -----------------------------
    def cache_service(self, query: str, cache: Dict[str, str]):
        if query in cache:
            return cache[query]
        raise CacheMissError("Cache miss")

    # -----------------------------
    # Static Fallback
    # -----------------------------
    def static_fallback(self, query: str):
        return f"Static fallback response for {query} (default answer)"

    # -----------------------------
    # Full Fallback Pipeline
    # -----------------------------
    def fetch(self, query: str, cache: Dict[str, str]):
        start_time = time.time()

        # Step 1: Primary Service
        result = self.safe_execute(self.primary_service, query)
        if result["status"] == "success":
            self.logs.append(("primary", query))
            return result["data"]

        # Step 2: Secondary Service
        result = self.safe_execute(self.secondary_service, query)
        if result["status"] == "success":
            self.logs.append(("secondary", query))
            return result["data"]

        # Step 3: Cache
        result = self.safe_execute(self.cache_service, query, cache)
        if result["status"] == "success":
            self.logs.append(("cache", query))
            return result["data"]

        # Step 4: Static fallback
        self.logs.append(("static", query))
        return self.static_fallback(query)

    # -----------------------------
    # Batch Processing with Fallback
    # -----------------------------
    def process_batch(self, queries: List[str], cache: Dict[str, str]):
        responses = []

        for q in queries:
            response = self.fetch(q, cache)
            responses.append({
                "query": q,
                "response": response
            })

        return responses

    # -----------------------------
    # Retry Mechanism (Optional Enhancement)
    # -----------------------------
    def retry(self, func: Callable, retries: int = 3, delay: float = 0.2):
        for attempt in range(retries):
            try:
                return func()
            except Exception:
                time.sleep(delay * (attempt + 1))
        raise Exception("All retries failed")


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    engine = FallbackEngine()

    cache_store = {
        "hello": "Cached hello response",
        "pricing": "Cached pricing data"
    }

    queries = ["hello", "weather", "pricing", "news"]

    results = engine.process_batch(queries, cache_store)

    for r in results:
        print(r)

    print("\nFallback Logs:")
    print(engine.logs)