from datetime import datetime, timedelta
from typing import Generic, TypeVar

T = TypeVar("T")


class TTLCache(Generic[T]):
    def __init__(self, ttl_seconds: int = 300) -> None:
        self.ttl = timedelta(seconds=ttl_seconds)
        self._store: dict[str, tuple[datetime, T]] = {}

    def get(self, key: str) -> T | None:
        entry = self._store.get(key)
        if not entry:
            return None
        created_at, value = entry
        if datetime.utcnow() - created_at > self.ttl:
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: T) -> None:
        self._store[key] = (datetime.utcnow(), value)
