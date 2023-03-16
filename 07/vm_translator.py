import enum
import re
from typing import Type


class MyEnum(enum.Enum):
    @classmethod
    def values_list(cls):
        return list(map(lambda x: x.value, cls.__members__.values()))

    @classmethod
    def enum_by_name(cls, name: str) -> Type["MyEnum"] | None:
        return cls.__members__.get(name)


class ArithmeticType(MyEnum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQUALS = "eq"
    GREATER = "gt"
    LESS = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


def D_to_stack_top() -> list[str]:
    """
    *SP = D{val}
    """
    return [
        "@SP",
        "A=M",
        "M=D",
    ]


def stack_top_toD() -> list[str]:
    """
    D{val} = *SP
    """
    return [
        "@SP",
        "A=M",
        "D=M",
    ]


def inc_var(name: str = "SP") -> list[str]:
    """
    name++;
    """
    return [
        f"@{name}",
        "D=M",
        "M=D+1",
    ]


def decr_var(name: str = "SP") -> list[str]:
    """
    name--;
    """
    return [
        f"@{name}",
        "D=M",
        "M=D-1",
    ]


def segment_i_to_D(segment_type: str, i: int) -> list[str]:
    """
    M = value in segment
    """

    seg_ptr_addr_mapping = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "temp": 5,
    }

    asm_lines: list[str] = []

    if segment_type == "constant":
        asm_lines = [
            # *SP=17
            f"@{i}",
            "D=A",
        ]
    elif segment_type == "static":
        asm_lines.extend([
            f"@Foo.{i}",  # A = Foo.5{addr}, M = Foo.5{val}
            "D=M",
        ])
    elif segment_type == "pointer":
        asm_lines.extend([
            f"@{'THIS' if i == 0 else 'THAT'}",  # A = THAT{addr}, M = THAT{val}
            "D=M",
        ])
    elif segment_type in seg_ptr_addr_mapping:
        ptr_addr = seg_ptr_addr_mapping[segment_type]

        asm_lines = [
            # addr = LCL+i; *SP = *addr; SP++;
            # addr = *LCL + 2
            f"@{ptr_addr}",  # A = LCL{addr} (1), M = LCL{val}
            "D=M",  # D = *LCL (10)
            f"@{i}",  # A = i (2)
            "D=D+A",  # D = D + A (10 + 2 = 12)
            "@addr",  # A -> addr, M = addr{val} (new var)
            "M=D",  # addr = 12
            "A=M",  # A = addr{val}, M = *addr // (A = 12, M = 15)
            # *SP = *addr
            # "M=D",  # D = 15, M = ..
            "D=M",
        ]
    else:
        raise Exception(f"Unhandled segment type: {segment_type}")

    return asm_lines


def push_to_asm(segment_type: str, i: int) -> list[str]:
    """
    SP++, *SP=val
    """

    return [
        *segment_i_to_D(segment_type, i),
        # "D=M",
        *D_to_stack_top(),
        *inc_var("SP"),
    ]


def pop_to_asm(segment_type: str, i: int) -> list[str]:
    return [
        *decr_var("SP"),
        *segment_i_to_D(segment_type, i),
        # "M=D",
        *stack_top_toD(),
    ]


def arithmetic_to_asm(line: str) -> list[str]:
    asm_lines: list[str]

    if line in [ArithmeticType.ADD.value, ArithmeticType.SUB.value]:
        asm_lines = [
            *decr_var("SP"),
            *stack_top_toD(),
            "@temp",
            "M=D",  # temp1 = *SP
            *decr_var("SP"),
            *stack_top_toD(),
            "@temp",  # A = &temp1, M = temp1
            "D=D+M" if line == ArithmeticType.ADD.value else "D=D-M",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]
    elif line == ArithmeticType.NEG.value:
        asm_lines = [
            *decr_var("SP"),
            *stack_top_toD(),
            "D=-D",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]
    else:
        # raise Exception(f"Unknown arithmetic operation: {line}")
        return []

    return asm_lines


def main(vm_filename: str):
    with open(vm_filename) as fin:
        lines = list(map(str.strip, fin.readlines()))

    asm_lines_all: list[str] = []

    for line in lines:
        if re.compile(r"^(push|pop) [a-z]+ [0-9]+$").match(line):
            _, segment_type, i = line.split(" ")

            if line.startswith("push"):
                f = push_to_asm
            else:
                f = pop_to_asm

            asm_lines = f(segment_type, int(i))
        elif line in ArithmeticType.values_list():
            asm_lines = arithmetic_to_asm(line)
        elif line.startswith("//") or not line:
            continue
        else:
            raise Exception(f"Unknown VM line: {line}")

        asm_lines_all.extend([
            f"// {line}",
            *asm_lines,
            "",
        ])

    s = "\n".join(asm_lines_all)
    print(s)

    asm_fname = vm_filename.replace(".vm", "")
    asm_fname += ".asm"

    with open(asm_fname, 'w') as fout:
        fout.write(s)


if __name__ == '__main__':
    # VM_FILENAME = "./MemoryAccess/BasicTest/BasicTest.vm"
    VM_FILENAME = "./myTest.vm"
    main(VM_FILENAME)
