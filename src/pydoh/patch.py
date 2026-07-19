import socket as _socket

from .resolver import resolve

_original_getaddrinfo = _socket.getaddrinfo
_patched = False


def _is_ip_literal(host: str) -> bool:
    try:
        _socket.inet_aton(host)
        return True
    except OSError:
        pass
    try:
        _socket.inet_pton(_socket.AF_INET6, host)
        return True
    except OSError:
        return False


def _doh_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if not host or _is_ip_literal(host):
        return _original_getaddrinfo(host, port, family, type, proto, flags)

    try:
        ips = resolve(host)
    except Exception:
        return _original_getaddrinfo(host, port, family, type, proto, flags)

    if not ips:
        return _original_getaddrinfo(host, port, family, type, proto, flags)

    resolved_port = port if isinstance(port, int) else 0
    return [
        (_socket.AF_INET, _socket.SOCK_STREAM, 6, "", (ip, resolved_port))
        for ip in ips
    ]


def patch_socket() -> None:
    global _patched
    if _patched:
        return
    _socket.getaddrinfo = _doh_getaddrinfo
    _patched = True


def unpatch_socket() -> None:
    global _patched
    if not _patched:
        return
    _socket.getaddrinfo = _original_getaddrinfo
    _patched = False
