import random
import struct
from typing import List, Tuple


def _encode_name(name: str) -> bytes:
    parts = name.rstrip(".").split(".")
    out = bytearray()
    for part in parts:
        encoded = part.encode("ascii")
        out.append(len(encoded))
        out.extend(encoded)
    out.append(0)
    return bytes(out)


def build_query(name: str, record_type: int = 1) -> Tuple[bytes, int]:
    query_id = random.randint(0, 0xFFFF)
    header = struct.pack(">HHHHHH", query_id, 0x0100, 1, 0, 0, 0)
    question = _encode_name(name) + struct.pack(">HH", record_type, 1)
    return header + question, query_id


def _read_name(data: bytes, offset: int) -> Tuple[str, int]:
    labels: List[str] = []
    jumped = False
    return_offset = offset

    while True:
        length = data[offset]
        if length == 0:
            offset += 1
            break
        if (length & 0xC0) == 0xC0:
            pointer = ((length & 0x3F) << 8) | data[offset + 1]
            if not jumped:
                return_offset = offset + 2
            offset = pointer
            jumped = True
            continue
        offset += 1
        labels.append(data[offset:offset + length].decode("ascii", errors="replace"))
        offset += length

    end_offset = return_offset if jumped else offset
    return ".".join(labels), end_offset


def parse_response(data: bytes) -> Tuple[int, List[Tuple[str, int]]]:
    query_id, _flags, qdcount, ancount, _nscount, _arcount = struct.unpack(">HHHHHH", data[:12])
    offset = 12

    for _ in range(qdcount):
        _, offset = _read_name(data, offset)
        offset += 4

    answers: List[Tuple[str, int]] = []
    for _ in range(ancount):
        _name, offset = _read_name(data, offset)
        rtype, _rclass, ttl, rdlength = struct.unpack(">HHIH", data[offset:offset + 10])
        offset += 10
        rdata = data[offset:offset + rdlength]
        offset += rdlength

        if rtype == 1 and len(rdata) == 4:
            answers.append((".".join(str(b) for b in rdata), ttl))
        elif rtype == 28 and len(rdata) == 16:
            groups = [rdata[i:i + 2].hex() for i in range(0, 16, 2)]
            answers.append((":".join(groups), ttl))

    return query_id, answers
