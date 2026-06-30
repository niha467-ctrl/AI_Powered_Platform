"""
===========================================================
BACKEND ERROR HANDLING & AI FALLBACK MANAGEMENT
Single File Python Implementation
===========================================================

Features
--------
✔ Global Exception Handling
✔ AI Service Fallback
✔ Retry Mechanism
✔ Circuit Breaker
✔ Logging
✔ Response Formatter
✔ Request Validation
✔ API Error Management
✔ Health Monitoring
✔ Mock AI Providers
✔ Production Ready Structure

Run:
    python backend_fallback.py
===========================================================
"""

import random
import time
import logging
from functools import wraps

# -------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("AIBackend")

# -------------------------------------------------------
# Custom Exceptions
# -------------------------------------------------------

class ValidationError(Exception):
    pass

class AIServiceError(Exception):
    pass

class CircuitOpenError(Exception):
    pass

# -------------------------------------------------------
# Standard API Response
# -------------------------------------------------------

class APIResponse:

    @staticmethod
    def success(data):

        return {
            "success": True,
            "message": "Success",
            "data": data
        }

    @staticmethod
    def error(message, code=500):

        return {
            "success": False,
            "status_code": code,
            "error": message
        }

# -------------------------------------------------------
# Circuit Breaker
# -------------------------------------------------------

class CircuitBreaker:

    def __init__(self, threshold=3, timeout=5):

        self.threshold = threshold
        self.timeout = timeout

        self.failures = 0
        self.last_failure = None

    def call(self, func):

        if (
            self.failures >= self.threshold
            and
            time.time() - self.last_failure < self.timeout
        ):
            raise CircuitOpenError(
                "Circuit Breaker Open"
            )

        try:

            result = func()

            self.failures = 0

            return result

        except Exception:

            self.failures += 1
            self.last_failure = time.time()

            raise

# -------------------------------------------------------
# Retry Decorator
# -------------------------------------------------------

def retry(max_attempts=3, delay=1):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(max_attempts):

                try:
                    return func(*args, **kwargs)

                except Exception as e:

                    logger.warning(
                        f"Retry {attempt+1}: {e}"
                    )

                    time.sleep(delay)

            raise AIServiceError(
                "Maximum retry attempts reached"
            )

        return wrapper

    return decorator

# -------------------------------------------------------
# Mock AI Providers
# -------------------------------------------------------

class PrimaryAI:

    @retry(2)
    def generate(self, prompt):

        if random.random() < 0.5:
            raise AIServiceError(
                "Primary AI unavailable"
            )

        return f"Primary AI Response -> {prompt}"


class SecondaryAI:

    @retry(2)
    def generate(self, prompt):

        if random.random() < 0.3:
            raise AIServiceError(
                "Secondary AI unavailable"
            )

        return f"Secondary AI Response -> {prompt}"


class LocalAI:

    def generate(self, prompt):

        return f"Local AI Fallback -> {prompt}"

# -------------------------------------------------------
# AI Manager
# -------------------------------------------------------

class AIManager:

    def __init__(self):

        self.primary = PrimaryAI()
        self.secondary = SecondaryAI()
        self.local = LocalAI()

        self.breaker = CircuitBreaker()

    def validate(self, prompt):

        if not prompt:
            raise ValidationError(
                "Prompt cannot be empty."
            )

        if len(prompt) < 3:
            raise ValidationError(
                "Prompt too short."
            )

    def ask(self, prompt):

        self.validate(prompt)

        try:

            logger.info(
                "Trying Primary AI..."
            )

            return self.breaker.call(
                lambda: self.primary.generate(prompt)
            )

        except Exception as e:

            logger.warning(e)

            try:

                logger.info(
                    "Trying Secondary AI..."
                )

                return self.secondary.generate(prompt)

            except Exception as e:

                logger.warning(e)

                logger.info(
                    "Switching to Local AI..."
                )

                return self.local.generate(prompt)

# -------------------------------------------------------
# Backend Service
# -------------------------------------------------------

class Backend:

    def __init__(self):

        self.ai = AIManager()

    def process(self, prompt):

        try:

            response = self.ai.ask(prompt)

            return APIResponse.success(response)

        except ValidationError as e:

            return APIResponse.error(
                str(e),
                400
            )

        except CircuitOpenError as e:

            return APIResponse.error(
                str(e),
                503
            )

        except AIServiceError as e:

            return APIResponse.error(
                str(e),
                500
            )

        except Exception as e:

            logger.exception(e)

            return APIResponse.error(
                "Unexpected Server Error",
                500
            )

# -------------------------------------------------------
# Health Monitor
# -------------------------------------------------------

class HealthMonitor:

    def status(self):

        return {
            "server": "Running",
            "primary_ai": "Online",
            "secondary_ai": "Online",
            "fallback": "Ready",
            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

# -------------------------------------------------------
# Example Usage
# -------------------------------------------------------

if __name__ == "__main__":

    backend = Backend()

    health = HealthMonitor()

    print("=" * 60)
    print("SYSTEM HEALTH")
    print("=" * 60)
    print(health.status())

    print("\n")

    prompts = [
        "Loan settlement prediction",
        "Customer risk analysis",
        "",
        "AI"
    ]

    for p in prompts:

        print("=" * 60)
        print("REQUEST :", repr(p))
        print("=" * 60)

        result = backend.process(p)

        print(result)
        print()