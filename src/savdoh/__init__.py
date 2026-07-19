from .resolver import ResolveError, resolve, resolve4, resolve6
from .patch import patch_socket, unpatch_socket
from .providers import CLOUDFLARE, GOOGLE, QUAD9

__version__ = "0.1.0"

__all__ = [
    "resolve",
    "resolve4",
    "resolve6",
    "ResolveError",
    "patch_socket",
    "unpatch_socket",
    "CLOUDFLARE",
    "GOOGLE",
    "QUAD9",
]
