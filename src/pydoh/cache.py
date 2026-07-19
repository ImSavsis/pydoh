import time
from threading import Lock
from typing import Any, Dict, Optional, Tuple


class TTLCache:
    def __init__(self) -> None:
        self._store: Dict[Any, Tuple[float, Any]] = {}
        self._lock = Lock()

    def get(self, key: Any) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            expires_at, value = entry
            if time.time() > expires_at:
                del self._store[key]
                return None
            return value

    def set(self, key: Any, value: Any, ttl: float) -> None:
        with self._lock:
            self._store[key] = (time.time() + ttl, value)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
