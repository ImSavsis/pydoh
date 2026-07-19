import struct

from savdoh.wire import build_query, parse_response


def test_build_query_shape():
    query, query_id = build_query("example.com")
    assert isinstance(query, bytes)
    assert 0 <= query_id <= 0xFFFF
    assert query[12:20] == b"\x07example"


def test_parse_response_a_record():
    query, query_id = build_query("example.com")
    question = query[12:]

    header = struct.pack(">HHHHHH", query_id, 0x8180, 1, 1, 0, 0)
    answer = b"\xc0\x0c" + struct.pack(">HHIH", 1, 1, 300, 4) + bytes([93, 184, 216, 34])
    response = header + question + answer

    resp_id, answers = parse_response(response)
    assert resp_id == query_id
    assert answers == [("93.184.216.34", 300)]


def test_parse_response_aaaa_record():
    query, query_id = build_query("example.com", record_type=28)
    question = query[12:]

    rdata = bytes.fromhex("20010db8000000000000000000000001")
    header = struct.pack(">HHHHHH", query_id, 0x8180, 1, 1, 0, 0)
    answer = b"\xc0\x0c" + struct.pack(">HHIH", 28, 1, 60, 16) + rdata
    response = header + question + answer

    resp_id, answers = parse_response(response)
    assert resp_id == query_id
    assert answers == [("2001:0db8:0000:0000:0000:0000:0000:0001", 60)]


def test_parse_response_no_answers():
    query, query_id = build_query("nx.example.com")
    question = query[12:]
    header = struct.pack(">HHHHHH", query_id, 0x8183, 1, 0, 0, 0)
    response = header + question

    resp_id, answers = parse_response(response)
    assert resp_id == query_id
    assert answers == []
