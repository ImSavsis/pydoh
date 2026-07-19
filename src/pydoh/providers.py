from typing import NamedTuple, List


class Provider(NamedTuple):
    name: str
    host: str
    path: str


CLOUDFLARE = Provider("cloudflare", "cloudflare-dns.com", "/dns-query")
GOOGLE = Provider("google", "dns.google", "/dns-query")
QUAD9 = Provider("quad9", "dns.quad9.net", "/dns-query")

DEFAULT_PROVIDERS: List[Provider] = [CLOUDFLARE, GOOGLE, QUAD9]
