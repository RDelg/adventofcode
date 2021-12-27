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


class PacketType(str, Enum):
    literal = "literal"
    operator = "operator"


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
            (6 + y[1]) if x == PacketType.literal else (7 + y[1]),
        )

    @classmethod
    def from_bin(cls, data: str) -> "Packet":
        version, type_id = cls.get_header(data)
        return cls(
            version,
            type_id,
            (x := cls.get_type(type_id)),
            (y := cls.get_value(x, data[6:]))[0],
            (6 + y[1]) if x == PacketType.literal else (7 + y[1]),
        )

    @staticmethod
    def get_type(type_id: int) -> PacketType:
        if type_id == 4:
            return PacketType.literal
        else:
            return PacketType.operator

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
            return packets, bits_len + 15
        elif length_type_id == 1:
            sub_packets = int(data[1:12], 2)
            packets.append(Packet.from_bin(data[12:]))
            while len(packets) < sub_packets:
                skip_bits = sum([x._bits for x in packets])
                packets.append(Packet.from_bin(data[12 + skip_bits :]))
            bits = sum([x._bits for x in packets])
            return packets, 11 + bits
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
        decoded = bin(int(data, 16))[2:]
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
        type=PacketType.operator,
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
        type=PacketType.operator,
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
