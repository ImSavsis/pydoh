# quickstart

## установка

```
pip install pydoh
```

## разовый резолвинг

```python
import pydoh

ips = pydoh.resolve("example.com")
print(ips)  # ['93.184.216.34']
```

`resolve()` возвращает список строк-адресов, первый обычно и есть тот, что нужен.

## ipv6

```python
ips = pydoh.resolve6("example.com")
```

или через параметр:

```python
pydoh.resolve("example.com", record_type=28)
```

## подменить резолвинг во всём приложении

самый частый кейс — не переписывать код, а просто подменить как питон резолвит домены:

```python
import pydoh
pydoh.patch_socket()

import requests
requests.get("https://example.com")  # уже через DoH, без изменений в коде requests
```

ставь `patch_socket()` в самом начале скрипта, до импорта/использования сетевых библиотек.

вернуть как было:

```python
pydoh.unpatch_socket()
```

## свой DoH-провайдер

если хочешь резолвить через свой сервер, а не через cloudflare/google/quad9:

```python
from pydoh.providers import Provider

my_provider = Provider(name="mine", host="doh.example.com", path="/dns-query")
ips = pydoh.resolve("example.com", providers=[my_provider])
```

сервер должен поддерживать [RFC 8484](https://www.rfc-editor.org/rfc/rfc8484) (`POST` с телом `application/dns-message`).
