# pydoh

[![CI](https://github.com/ImSavsis/pydoh/actions/workflows/ci.yml/badge.svg)](https://github.com/ImSavsis/pydoh/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/ImSavsis/pydoh/branch/master/graph/badge.svg)](https://codecov.io/gh/ImSavsis/pydoh)
[![pypi](https://img.shields.io/pypi/v/pydoh.svg)](https://pypi.org/project/pydoh/)
[![downloads](https://img.shields.io/pypi/dm/pydoh.svg)](https://pypi.org/project/pydoh/)
[![versions](https://img.shields.io/pypi/pyversions/pydoh.svg)](https://pypi.org/project/pydoh/)
[![license](https://img.shields.io/github/license/ImSavsis/pydoh.svg)](https://github.com/ImSavsis/pydoh/blob/master/LICENSE)

DNS-over-HTTPS резолвер для питона. ноль зависимостей — весь HTTPS через стандартный `http.client`+`ssl`. провайдер/DPI видит только твой HTTPS к cloudflare, а не голые DNS-запросы.

```mermaid
sequenceDiagram
    App->>pydoh: resolve("example.com")
    pydoh->>Cloudflare: DNS-запрос внутри HTTPS POST
    Cloudflare-->>pydoh: ответ внутри HTTPS
    pydoh-->>App: ["93.184.216.34"]
```

## установка

```
pip install pydoh
```

## юзать

```python
import pydoh

ips = pydoh.resolve("example.com")
```

или подменить резолвинг вообще везде в питоне одной строкой — `requests`, `aiohttp`, что угодно на сокетах будет резолвить через DoH:

```python
import pydoh
pydoh.patch_socket()
```

## документация

- [quickstart](docs/quickstart.md) — установка, базовое использование, свой провайдер
- [api](docs/api.md) — все функции с параметрами
- [faq](docs/faq.md) — зачем это надо, что делать если cloudflare забанят, законно ли

## фичи

- zero deps, только stdlib
- fallback между cloudflare / google / quad9 если один упал
- кэш по TTL из ответа
- typed (py.typed), питон 3.10–3.13

## что не умеет

не проверяет DNSSEC, не поддерживает TCP-фрагментированные DNS-ответы больше одного UDP-пакета.
