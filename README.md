# savdoh

[![CI](https://github.com/ImSavsis/savdoh/actions/workflows/ci.yml/badge.svg)](https://github.com/ImSavsis/savdoh/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/ImSavsis/savdoh/branch/master/graph/badge.svg)](https://codecov.io/gh/ImSavsis/savdoh)
[![pypi](https://img.shields.io/pypi/v/savdoh.svg)](https://pypi.org/project/savdoh/)
[![downloads](https://img.shields.io/pypi/dm/savdoh.svg)](https://pypi.org/project/savdoh/)
[![versions](https://img.shields.io/pypi/pyversions/savdoh.svg)](https://pypi.org/project/savdoh/)
[![license](https://img.shields.io/github/license/ImSavsis/savdoh.svg)](https://github.com/ImSavsis/savdoh/blob/master/LICENSE)

DNS-over-HTTPS резолвер для питона. ноль зависимостей — весь HTTPS через стандартный `http.client`+`ssl`. провайдер/DPI видит только твой HTTPS к cloudflare, а не голые DNS-запросы.

```mermaid
sequenceDiagram
    App->>savdoh: resolve("example.com")
    savdoh->>Cloudflare: DNS-запрос внутри HTTPS POST
    Cloudflare-->>savdoh: ответ внутри HTTPS
    savdoh-->>App: ["93.184.216.34"]
```

## установка

```
pip install savdoh
```

## юзать

```python
import savdoh

ips = savdoh.resolve("example.com")
```

или подменить резолвинг вообще везде в питоне одной строкой — `requests`, `aiohttp`, что угодно на сокетах будет резолвить через DoH:

```python
import savdoh
savdoh.patch_socket()
```

## фичи

- zero deps, только stdlib
- fallback между cloudflare / google / quad9 если один упал
- кэш по TTL из ответа
- typed (py.typed), питон 3.10–3.13

## что не умеет

не проверяет DNSSEC, не поддерживает TCP-фрагментированные DNS-ответы больше одного UDP-пакета.
