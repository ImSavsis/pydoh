import struct

import savdoh.resolver as resolver_module
from savdoh.resolver import ResolveError, resolve


def _make_response(query_id, ip):
    header = struct.pack(">HHHHHH", query_id, 0x8180, 1, 1, 0, 0)
    name = b"\x07example\x03com\x00"
    question = name + struct.pack(">HH", 1, 1)
    rdata = bytes(int(part) for part in ip.split("."))
    answer = b"\xc0\x0c" + struct.pack(">HHIH", 1, 1, 300, 4) + rdata
    return header + question + answer


def test_resolve_returns_ip(monkeypatch):
    def fake_doh_request(provider, query, timeout):
        query_id = struct.unpack(">H", query[:2])[0]
        return _make_response(query_id, "93.184.216.34")

    monkeypatch.setattr(resolver_module, "_doh_request", fake_doh_request)
    resolver_module._cache.clear()

    ips = resolve("example.com", use_cache=False)
    assert ips == ["93.184.216.34"]


def test_resolve_uses_cache(monkeypatch):
    calls = []

    def fake_doh_request(provider, query, timeout):
        calls.append(1)
        query_id = struct.unpack(">H", query[:2])[0]
        return _make_response(query_id, "1.1.1.1")

    monkeypatch.setattr(resolver_module, "_doh_request", fake_doh_request)
    resolver_module._cache.clear()

    resolve("example.com", use_cache=True)
    resolve("example.com", use_cache=True)
    assert len(calls) == 1


def test_resolve_falls_back_to_next_provider(monkeypatch):
    attempts = []

    def fake_doh_request(provider, query, timeout):
        attempts.append(provider.name)
        if provider.name == "cloudflare":
            raise RuntimeError("simulated failure")
        query_id = struct.unpack(">H", query[:2])[0]
        return _make_response(query_id, "8.8.8.8")

    monkeypatch.setattr(resolver_module, "_doh_request", fake_doh_request)
    resolver_module._cache.clear()

    ips = resolve("example.com", use_cache=False)
    assert ips == ["8.8.8.8"]
    assert attempts[0] == "cloudflare"


def test_resolve_raises_when_all_providers_fail(monkeypatch):
    def fake_doh_request(provider, query, timeout):
        raise RuntimeError("down")

    monkeypatch.setattr(resolver_module, "_doh_request", fake_doh_request)
    resolver_module._cache.clear()

    try:
        resolve("example.com", use_cache=False)
        assert False, "expected ResolveError"
    except ResolveError:
        pass
