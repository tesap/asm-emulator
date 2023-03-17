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
    *SP = D
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


def push_to_asm(segment_type: str, i: int) -> list[str]:
    """
    D = value in segment
    """

    seg_ptr_addr_mapping = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "temp": 5,
        "pointer": 3,
    }

    asm_lines: list[str] = []

    if segment_type == "constant":
        asm_lines = [
            # *SP=17
            f"@{i}",
            "D=A",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]
    elif segment_type == "static":
        asm_lines.extend([
            f"@Foo.{i}",  # A = Foo.5{addr}, M = Foo.5{val}
            "D=M",
            *D_to_stack_top(),
            *inc_var("SP"),
        ])
    elif segment_type in seg_ptr_addr_mapping:
        ptr_addr = seg_ptr_addr_mapping[segment_type]

        asm_lines = [
            # addr = LCL+i; *SP = *addr; SP++;
            # addr = *LCL + 2
            f"@{ptr_addr}",  # A = LCL{addr} (1), M = LCL{val}
            "D=M",  # D = *LCL (10)
            f"@{i}",  # A = i (2)
            "A=D+A",  # D = D + A (10 + 2 = 12)
            "D=M",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]
    else:
        raise Exception(f"Unhandled segment type: {segment_type}")

    return asm_lines


def pop_to_asm(segment_type: str, i: int) -> list[str]:
    seg_ptr_addr_mapping = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "temp": 5,
        "pointer": 3,
    }

    if segment_type == "static":
        return [
            *decr_var("SP"),
            *stack_top_toD(),
            f"@Foo.{i}",  # A = Foo.5{addr}, M = Foo.5{val}
            "M=D",
        ]
    elif segment_type in seg_ptr_addr_mapping:
        ptr_addr = seg_ptr_addr_mapping[segment_type]

        return [
            # addr = LCL+i; *SP = *addr; SP++;
            # addr = *LCL + 2

            f"@{ptr_addr}",  # A = LCL{addr} (1), M = LCL{val}
            "D=M",  # D = *LCL (10)
            f"@{i}",  # A = i (2)
            "D=D+A",  # D = D + A (10 + 2 = 12)
            "@R13",  # A -> addr, M = addr{val} (new var)
            "M=D",  # R13 = 12

            *decr_var("SP"),
            *stack_top_toD(),

            "@R13",
            "A=M",
            "M=D",

        ]
    else:
        raise Exception(f"Unhandled segment type: {segment_type}")


def arithmetic_to_asm(line: str) -> list[str]:
    def top2_operation(operation: str = "D+M") -> list[str]:
        return [
            *decr_var("SP"),
            *stack_top_toD(),
            "@temp",
            "M=D",  # temp1 = *SP
            *decr_var("SP"),
            *stack_top_toD(),
            "@temp",  # A = &temp1, M = temp1
            f"D={operation}",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]

    def top1_operation(operation: str = "-D") -> list[str]:
        return [
            *decr_var("SP"),
            *stack_top_toD(),
            f"D={operation}",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]

    asm_lines: list[str]

    if line in [ArithmeticType.ADD.value, ArithmeticType.SUB.value]:
        return top2_operation(operation="D+M")
    elif line == ArithmeticType.NEG.value:
        asm_lines = top1_operation(operation="-D")
    elif line == ArithmeticType.NOT.value:
        asm_lines = top1_operation(operation="!D")
    elif line == ArithmeticType.EQUALS.value:
        asm_lines = [
            *top2_operation(operation="D-M"),
            *decr_var("SP"),
            *stack_top_toD(),
            # *D_to_stack_top(),
            "@EQ",
            "D;JEQ",

            "D=0",
            "@ENDIF1",
            "0;JMP",

            "(EQ)",
            "D=1",

            "(ENDIF1)",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]
    elif line == ArithmeticType.GREATER.value:
        asm_lines = [
            *top2_operation(operation="D-M"),
            *decr_var("SP"),
            *stack_top_toD(),
            # *D_to_stack_top(),
            "@GT",
            "D;JGT",

            "D=0",
            "@ENDIF2",
            "0;JMP",

            "(GT)",
            "D=1",

            "(ENDIF2)",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]
    elif line == ArithmeticType.LESS.value:
        asm_lines = [
            *top2_operation(operation="D-M"),
            *decr_var("SP"),
            *stack_top_toD(),
            # *D_to_stack_top(),
            "@LT",
            "D;JLT",

            "D=0",
            "@ENDIF3",
            "0;JMP",

            "(LT)",
            "D=1",

            "(ENDIF3)",
            *D_to_stack_top(),
            *inc_var("SP"),
        ]
    elif line == ArithmeticType.AND.value:
        asm_lines = [
            *top2_operation(operation="D&M")
        ]
    elif line == ArithmeticType.OR.value:
        asm_lines = [
            *top2_operation(operation="D|M")
        ]
    else:
        raise Exception(f"Unknown arithmetic operation: {line}")
        # return []

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
    VM_FILENAME = "./MemoryAccess/BasicTest/BasicTest.vm"
    # VM_FILENAME = "./MemoryAccess/PointerTest/PointerTest.vm"
    # VM_FILENAME = "./myTest.vm"
    main(VM_FILENAME)
