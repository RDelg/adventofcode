import operator
import functools

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Union


RAW_DEMO_1 = "D2FE28"
RAW_DEMO_2 = "38006F45291200"
RAW_DEMO_3 = "EE00D40C823060"
RAW_DEMO_4 = "8A004A801A8002F478"
RAW_DEMO_5 = "620080001611562C8802118E34"
RAW_DEMO_6 = "C0015000016115A2E0802F182340"
RAW_DEMO_7 = "A0016C880162017C3686B18A3D4780"
RAW_DEMO_8 = "C200B40A82"
RAW_DEMO_9 = "04005AC33890"
RAW_DEMO_10 = "880086C3E88112"
RAW_DEMO_11 = "CE00C43D881120"
RAW_DEMO_12 = "D8005AC2A8F0"
RAW_DEMO_13 = "F600BC2D8F"
RAW_DEMO_14 = "9C005AC2F8F0"
RAW_DEMO_15 = "9C0141080250320F1802104A08"


class PacketType(int, Enum):
    sum = 0
    product = 1
    minimum = 2
    maximum = 3
    literal = 4
    greater_than = 5
    less_than = 6
    equal_to = 7


@dataclass
class Packet:
    version: int
    type_id: int
    type: PacketType
    value: Union[List["Packet"], int]
    _bits: int = 0

    @classmethod
    def from_hex(cls, data: str) -> "Packet":
        decoded = cls.hex_to_binary(data)
        version, type_id = cls.get_header(decoded)
        return cls(
            version,
            type_id,
            (x := cls.get_type(type_id)),
            (y := cls.get_value(x, decoded[6:]))[0],
            (6 + y[1]),
        )

    @classmethod
    def from_bin(cls, data: str) -> "Packet":
        version, type_id = cls.get_header(data)
        return cls(
            version,
            type_id,
            (x := cls.get_type(type_id)),
            (y := cls.get_value(x, data[6:]))[0],
            (6 + y[1]),
        )

    @staticmethod
    def get_type(type_id: int) -> PacketType:
        return PacketType(type_id)

    @staticmethod
    def get_value(
        ptype: PacketType, data: str
    ) -> Tuple[Union[List["Packet"], int], int]:
        if ptype == PacketType.literal:
            return Packet.get_literal_value(data)
        else:
            return Packet.get_operator_value(data)

    @staticmethod
    def get_operator_value(data: str) -> List["Packet"]:
        length_type_id = int(data[0])
        packets = []
        if length_type_id == 0:
            bits_len = int(data[1:16], 2)
            packets.append(Packet.from_bin(data[16 : 16 + bits_len]))
            while (x := sum([x._bits for x in packets])) < bits_len:
                packets.append(Packet.from_bin(data[16 + x : 16 + bits_len]))
            return packets, bits_len + 16
        elif length_type_id == 1:
            sub_packets = int(data[1:12], 2)
            packets.append(Packet.from_bin(data[12:]))
            while len(packets) < sub_packets:
                skip_bits = sum([x._bits for x in packets])
                packets.append(Packet.from_bin(data[12 + skip_bits :]))
            bits = sum([x._bits for x in packets])
            return packets, 12 + bits
        else:
            raise ValueError(f"Unknown operator length type: {length_type_id}")

    @staticmethod
    def get_literal_value(data: str) -> Tuple[int, int]:
        vs = []
        c = 0
        while True:
            vs.append(data[c + 1 : c + 5])
            if data[c] == "0":
                break
            c += 5
        return int("".join(vs), 2), c + 5

    @staticmethod
    def hex_to_binary(data: str) -> str:
        decoded = "".join([bin(int(x, 16))[2:].zfill(4) for x in data])
        if len(decoded) % 4 != 0:
            decoded = decoded.zfill(4 * ((len(decoded) // 4) + 1))
        return decoded

    @staticmethod
    def get_header(data: str) -> Tuple[int, int]:
        v = data[0:3]
        t = data[3:6]
        return int(v, 2), int(t, 2)

    def sum_versions(self) -> int:
        v = self.version
        if isinstance(self.value, list):
            for p in self.value:
                v += p.sum_versions()
        return v

    def operator(self) -> str:
        if self.type == PacketType.sum:
            return "sum"
        elif self.type == PacketType.product:
            return "prod"
        elif self.type == PacketType.minimum:
            return "min"
        elif self.type == PacketType.maximum:
            return "max"
        elif self.type == PacketType.less_than:
            return "less"
        elif self.type == PacketType.greater_than:
            return "greater"
        elif self.type == PacketType.equal_to:
            return "equal"
        else:
            raise ValueError(f"Unknown operator: {self.type}")

    def to_math_expresion(self) -> str:
        if isinstance(self.value, list):
            return (
                self.operator()
                + "("
                + "["
                + ",".join([x.to_math_expresion() for x in self.value])
                + "]"
                + ")"
            )
        else:
            return str(self.value)


def prod(*args) -> float:
    return functools.reduce(operator.mul, *args, 1)


def less(*args) -> bool:
    return functools.reduce(operator.lt, *args)


def greater(*args) -> bool:
    return functools.reduce(operator.gt, *args)


def equal(*args) -> bool:
    return functools.reduce(operator.eq, *args)


if __name__ == "__main__":
    # Data
    with open("data/16.txt", "r") as f:
        data = f.read()

    # Part 1
    # Demo 1
    c = Packet.from_hex(RAW_DEMO_1)
    assert c == Packet(
        version=6, type_id=4, type=PacketType.literal, value=2021, _bits=21
    )

    # Demo 2
    c = Packet.from_hex(RAW_DEMO_2)
    assert c == Packet(
        version=1,
        type_id=6,
        type=PacketType(6),
        value=[
            Packet(
                version=6,
                type_id=4,
                type=PacketType.literal,
                value=10,
                _bits=11,
            ),
            Packet(
                version=2,
                type_id=4,
                type=PacketType.literal,
                value=20,
                _bits=16,
            ),
        ],
        _bits=49,
    )

    # Demo 3
    c = Packet.from_hex(RAW_DEMO_3)
    assert c == Packet(
        version=7,
        type_id=3,
        type=PacketType(3),
        value=[
            Packet(
                version=2,
                type_id=4,
                type=PacketType.literal,
                value=1,
                _bits=11,
            ),
            Packet(
                version=4,
                type_id=4,
                type=PacketType.literal,
                value=2,
                _bits=11,
            ),
            Packet(
                version=1,
                type_id=4,
                type=PacketType.literal,
                value=3,
                _bits=11,
            ),
        ],
        _bits=51,
    )
    # Versions check
    # Demo 4
    c = Packet.from_hex(RAW_DEMO_4)
    assert c.sum_versions() == 16
    # Demo 5
    c = Packet.from_hex(RAW_DEMO_5)
    # print(c)
    assert c.sum_versions() == 12
    # # Demo 6
    c = Packet.from_hex(RAW_DEMO_6)
    assert c.sum_versions() == 23
    # Demo 7
    c = Packet.from_hex(RAW_DEMO_7)
    assert c.sum_versions() == 31

    # Real
    c = Packet.from_hex(data)
    print("Part 1:", c.sum_versions())

    # Part 2
    # Demo 8
    c = Packet.from_hex(RAW_DEMO_8)
    assert eval(c.to_math_expresion()) == 3
    # Demo 9
    c = Packet.from_hex(RAW_DEMO_9)
    assert eval(c.to_math_expresion()) == 54
    # Demo 10
    c = Packet.from_hex(RAW_DEMO_10)
    assert eval(c.to_math_expresion()) == 7
    # Demo 11
    c = Packet.from_hex(RAW_DEMO_11)
    assert eval(c.to_math_expresion()) == 9
    # Demo 12
    c = Packet.from_hex(RAW_DEMO_12)
    assert eval(c.to_math_expresion()) == 1
    # Demo 13
    c = Packet.from_hex(RAW_DEMO_13)
    assert eval(c.to_math_expresion()) == 0
    # Demo 14
    c = Packet.from_hex(RAW_DEMO_14)
    assert eval(c.to_math_expresion()) == 0
    # Real
    c = Packet.from_hex(data)
    print("Part 2:", eval(c.to_math_expresion()))
