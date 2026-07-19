import time

from savdoh.cache import TTLCache


def test_cache_hit():
    cache = TTLCache()
    cache.set("k", ["1.2.3.4"], ttl=60)
    assert cache.get("k") == ["1.2.3.4"]


def test_cache_expires():
    cache = TTLCache()
    cache.set("k", ["1.2.3.4"], ttl=0.05)
    assert cache.get("k") == ["1.2.3.4"]
    time.sleep(0.1)
    assert cache.get("k") is None


def test_cache_clear():
    cache = TTLCache()
    cache.set("k", ["1.2.3.4"], ttl=60)
    cache.clear()
    assert cache.get("k") is None


def test_cache_miss():
    cache = TTLCache()
    assert cache.get("missing") is None
