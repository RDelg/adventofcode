from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Union


RAW_DEMO_1 = "D2FE28"
RAW_DEMO_2 = "38006F45291200"


class PacketType(str, Enum):
    literal = "literal"
    operator = "operator"


@dataclass
class Packet:
    version: int
    type_id: int
    type: PacketType
    value: Union[List["Packet"], int]

    @classmethod
    def from_hex(cls, data: str) -> "Packet":
        decoded = cls.hex_to_binary(data)
        version, type_id = cls.get_header(decoded)
        return cls(
            version,
            type_id,
            (x := cls.get_type(type_id)),
            cls.get_value(x, decoded[6:]),
        )

    @classmethod
    def from_bin(cls, data: str) -> "Packet":
        version, type_id = cls.get_header(data)
        return cls(
            version,
            type_id,
            (x := cls.get_type(type_id)),
            cls.get_value(x, data[6:]),
        )

    @staticmethod
    def get_type(type_id: int) -> PacketType:
        if type_id == 4:
            return PacketType.literal
        else:
            return PacketType.operator

    @staticmethod
    def get_value(ptype: PacketType, data: str) -> Union[List["Packet"], int]:
        if ptype == PacketType.literal:
            return Packet.get_literal_value(data)
        else:
            return Packet.get_operator_value(data)

    @staticmethod
    def get_operator_value(data: str) -> List["Packet"]:
        length_type_id = int(data[0])
        if length_type_id == 0:
            bits_len = int(data[1:16], 2)
            return Packet.from_bin("11010001010")
        elif length_type_id == 1:
            pass
        else:
            raise ValueError(f"Unknown operator length type: {length_type_id}")

    @staticmethod
    def get_literal_value(data: str) -> int:
        vs = []
        c = 0
        while True:
            vs.append(data[c + 1 : c + 5])
            if data[c] == "0":
                break
            c += 5
        return int("".join(vs), 2)

    @staticmethod
    def hex_to_binary(data: str) -> str:
        return (x := bin(int(data, 16))[2:]).zfill(4 * ((len(x) // 4) + 1))

    @staticmethod
    def get_header(data: str) -> Tuple[int, int]:
        v = data[0:3]
        t = data[3:6]
        return int(v, 2), int(t, 2)


if __name__ == "__main__":
    # # Part 1
    # # Demo 1
    # c = Packet.from_hex(RAW_DEMO_1)
    # assert c == Packet(version=6, type_id=4, type=PacketType.literal, value=2021)
    # # Demo 2
    c = Packet.from_hex(RAW_DEMO_2)
    print(c)
