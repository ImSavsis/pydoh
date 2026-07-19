# api

## `resolve(hostname, record_type=1, providers=None, timeout=3.0, use_cache=True) -> list[str]`

резолвит хост, возвращает список IP строками. кидает `ResolveError` если все провайдеры упали.

- `record_type` — `1` для A (по умолчанию), `28` для AAAA
- `providers` — список `Provider`, по умолчанию `pydoh.providers.DEFAULT_PROVIDERS` (cloudflare, google, quad9 по порядку)
- `timeout` — секунды на один HTTPS-запрос к одному провайдеру
- `use_cache` — читать/писать во внутренний кэш по TTL из ответа

## `resolve4(hostname, **kwargs) -> list[str]`

то же самое что `resolve(hostname, record_type=1, **kwargs)`.

## `resolve6(hostname, **kwargs) -> list[str]`

то же самое что `resolve(hostname, record_type=28, **kwargs)`.

## `patch_socket() -> None`

подменяет `socket.getaddrinfo` на версию через `resolve()`. IP-литералы (`127.0.0.1` и т.п.) пропускает мимо DoH напрямую. идемпотентно — повторный вызов ничего не ломает.

## `unpatch_socket() -> None`

возвращает оригинальный `socket.getaddrinfo`.

## `ResolveError`

исключение, вылетает из `resolve()`/`resolve4()`/`resolve6()` если ни один провайдер не ответил валидно.

## `pydoh.providers.Provider`

```python
Provider(name: str, host: str, path: str)
```

именованный tuple, описывает DoH-эндпоинт. готовые: `pydoh.CLOUDFLARE`, `pydoh.GOOGLE`, `pydoh.QUAD9`.
