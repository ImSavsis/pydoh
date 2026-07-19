from savdoh import resolve


def test_live_resolve_example_com():
    ips = resolve("example.com", use_cache=False)
    assert len(ips) > 0
    assert all(part.isdigit() for ip in ips for part in ip.split("."))
