import time
import random
from typing import Callable, Any, List

RETRY_CONFIG = {
    "default_mode": 3,
    "autonomous_mode": 6,
    "base_delays": [10, 30, 60, 120, 180, 200],  # 600s total
    "jitter": 0.30,  # ±30%
    "recoverable_errors": [
        "RateLimitError",
        "NetworkError",
        "ServerError",
        "ModelBusy",
        "Timeout"
    ]
}

def with_retry(func: Callable, mode: str = "autonomous_mode") -> Any:
    max_retries = RETRY_CONFIG.get(mode, 3)
    delays = RETRY_CONFIG.get("base_delays", [10, 30, 60])
    jitter = RETRY_CONFIG.get("jitter", 0.3)
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            error_name = type(e).__name__
            if error_name not in RETRY_CONFIG["recoverable_errors"] and attempt < max_retries - 1:
                # If not explicitly recoverable, we might still want to retry a few times for unknown transient issues
                pass 
            
            if attempt == max_retries - 1:
                raise e
            
            delay = delays[min(attempt, len(delays)-1)]
            actual_delay = delay * (1 + random.uniform(-jitter, jitter))
            
            print(f"Attempt {attempt + 1} failed with {error_name}. Retrying in {actual_delay:.2f}s...")
            time.sleep(actual_delay)
