import socket

from pydoh.patch import patch_socket, unpatch_socket


def test_patch_and_unpatch_restores_original():
    original = socket.getaddrinfo
    patch_socket()
    assert socket.getaddrinfo is not original
    unpatch_socket()
    assert socket.getaddrinfo is original


def test_patch_is_idempotent():
    patch_socket()
    patched = socket.getaddrinfo
    patch_socket()
    assert socket.getaddrinfo is patched
    unpatch_socket()


def test_ip_literal_bypasses_doh():
    patch_socket()
    try:
        result = socket.getaddrinfo("127.0.0.1", 80)
        assert result
    finally:
        unpatch_socket()
