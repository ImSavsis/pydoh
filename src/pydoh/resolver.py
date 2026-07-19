import http.client
import ssl
from typing import List, Optional, Sequence

from .cache import TTLCache
from .providers import DEFAULT_PROVIDERS, Provider
from .wire import build_query, parse_response

_cache = TTLCache()


class ResolveError(Exception):
    pass


def _doh_request(provider: Provider, query: bytes, timeout: float) -> bytes:
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection(provider.host, 443, timeout=timeout, context=ctx)
    try:
        headers = {
            "Content-Type": "application/dns-message",
            "Accept": "application/dns-message",
        }
        conn.request("POST", provider.path, body=query, headers=headers)
        resp = conn.getresponse()
        if resp.status != 200:
            raise ResolveError(f"{provider.name} returned HTTP {resp.status}")
        return resp.read()
    finally:
        conn.close()


def resolve(
    hostname: str,
    record_type: int = 1,
    providers: Optional[Sequence[Provider]] = None,
    timeout: float = 3.0,
    use_cache: bool = True,
) -> List[str]:
    cache_key = (hostname, record_type)
    if use_cache:
        cached = _cache.get(cache_key)
        if cached is not None:
            return cached

    query, query_id = build_query(hostname, record_type)
    last_error: Optional[Exception] = None

    for provider in providers or DEFAULT_PROVIDERS:
        try:
            raw = _doh_request(provider, query, timeout)
            resp_id, answers = parse_response(raw)
            if resp_id != query_id:
                continue

            ips = [ip for ip, _ in answers]
            if ips:
                min_ttl = min(ttl for _, ttl in answers)
                if use_cache:
                    _cache.set(cache_key, ips, min_ttl)
                return ips
            return []
        except Exception as exc:
            last_error = exc
            continue

    raise ResolveError(f"could not resolve {hostname}") from last_error


def resolve4(hostname: str, **kwargs) -> List[str]:
    return resolve(hostname, record_type=1, **kwargs)


def resolve6(hostname: str, **kwargs) -> List[str]:
    return resolve(hostname, record_type=28, **kwargs)
