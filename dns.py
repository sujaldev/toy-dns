import struct
from random import randint
from dataclasses import dataclass, astuple

TYPE_A = 1
CLASS_IN = 1
RECURSION_DESIRED = 1 << 8


@dataclass
class DNSHeader:
    id: int
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

    def to_bytes(self) -> bytes:
        fields = astuple(self)
        return struct.pack("!HHHHHH", *fields)


@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int

    def to_bytes(self) -> bytes:
        return self.name + struct.pack("!HH", self.type_, self.class_)


def encode_dns_name(domain_name: str) -> bytes:
    encoded = b""
    for part in domain_name.encode("ASCII").split(b"."):
        encoded += bytes([len(part)]) + part
    return encoded + b"\x00"


def build_query(domain_name: str, record_type: int) -> bytes:
    header = DNSHeader(
        id=randint(0, 65535),
        num_questions=1,
        flags=RECURSION_DESIRED
    ).to_bytes()

    question = DNSQuestion(
        name=encode_dns_name(domain_name),
        type_=record_type,
        class_=CLASS_IN
    ).to_bytes()

    return header + question
