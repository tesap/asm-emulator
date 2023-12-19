import enum
import re, sys
from typing import Type

seg_ptr_addr_mapping = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "temp": 5,
    "pointer": 3,
}

labels_cnt = 0


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


def push_d() -> list[str]:
    return [
        "@SP",
        "AM=M+1",
        "A=A-1",
        "M=D",
    ]


def pop_to_d():
    return [
        "@SP",
        "AM=M-1",
        "D=M",
    ]


def push_to_asm(segment_type: str, i: int) -> list[str]:
    """
    D = value in segment
    """

    if segment_type == "constant":
        return [
            # *SP=17
            f"@{i}",
            "D=A",
            *push_d(),
        ]
    elif segment_type == "static":
        return [
            f"@Foo.{i}",  # A = Foo.5{addr}, M = Foo.5{val}
            "D=M",
            # *D_to_stack_top(),
            # *inc_var("SP"),
            *push_d(),
        ]
    elif segment_type in seg_ptr_addr_mapping:
        ptr_addr = seg_ptr_addr_mapping[segment_type]

        return [
            # addr = LCL+i; *SP = *addr; SP++;
            # addr = *LCL + 2
            f"@{i}",  # A = i (2)
            "D=A",
            # "D=M" if isinstance(ptr_addr, str) else "D=A",  # D = *LCL (10)
            f"@{ptr_addr}",  # A = LCL{addr} (1), M = LCL{val}
            *(["A=M", "A=D+A"] if isinstance(ptr_addr, str) else ["A=D+A"]),  # D = D + A (10 + 2 = 12)
            "D=M",
            *push_d(),
        ]
    else:
        raise Exception(f"Unhandled segment type: {segment_type}")


def pop_to_asm(segment_type: str, i: int) -> list[str]:
    if segment_type == "static":
        return [
            *pop_to_d(),
            f"@Foo.{i}",  # A = Foo.5{addr}, M = Foo.5{val}
            "M=D",
        ]
    elif segment_type in seg_ptr_addr_mapping:
        ptr_addr = seg_ptr_addr_mapping[segment_type]

        return [
            # addr = LCL+i; *SP = *addr; SP++;
            # addr = *LCL + 2

            f"@{i}",  # A = i (2)
            "D=A",
            # "D=M" if isinstance(ptr_addr, str) else "D=A",  # D = *LCL (10)
            f"@{ptr_addr}",  # A = LCL{addr} (1), M = LCL{val}
            *(["A=M", "D=D+A"] if isinstance(ptr_addr, str) else ["D=D+A"]),  # D = D + A (10 + 2 = 12)
            "@R13",  # A -> addr, M = addr{val} (new var)
            "M=D",  # R13 = 12

            *pop_to_d(),

            "@R13",
            "A=M",
            "M=D",
        ]
    else:
        raise Exception(f"Unhandled segment type: {segment_type}")


def arithmetic_to_asm(line: str) -> list[str]:
    global labels_cnt

    def top2_operation(operation: str = "D+M") -> list[str]:
        return [
            # *decr_var("SP"),
            # *stack_top_toD(),
            *pop_to_d(),
            "@R13",
            "M=D",  # temp1 = *SP
            # *decr_var("SP"),
            # *stack_top_toD(),
            *pop_to_d(),
            "@R13",  # A = &temp1, M = temp1
            f"D={operation}",
            # *D_to_stack_top(),
            # *inc_var("SP"),
            *push_d(),
        ]

    def top1_operation(operation: str = "-D") -> list[str]:
        return [
            # *decr_var("SP"),
            # *stack_top_toD(),
            *pop_to_d(),
            f"D={operation}",
            # *D_to_stack_top(),
            # *inc_var("SP"),
            *push_d(),
        ]

    asm_lines: list[str]

    if line == ArithmeticType.ADD.value:
        return top2_operation(operation="D+M")
    elif line == ArithmeticType.SUB.value:
        return top2_operation(operation="D-M")
    elif line == ArithmeticType.NEG.value:
        asm_lines = top1_operation(operation="-D")
    elif line == ArithmeticType.NOT.value:
        asm_lines = top1_operation(operation="!D")
    elif line in [ArithmeticType.EQUALS.value, ArithmeticType.GREATER.value, ArithmeticType.LESS.value]:

        if line == ArithmeticType.EQUALS.value:
            jmp_clause = "D;JEQ"
        elif line == ArithmeticType.GREATER.value:
            jmp_clause = "D;JGT"
        elif line == ArithmeticType.LESS.value:
            jmp_clause = "D;JLT"
        else:
            raise Exception

        label_then = f"THEN{labels_cnt}"
        label_endif = f"ENDIF{labels_cnt}"
        labels_cnt += 1

        asm_lines = [
            *top2_operation(operation="D-M"),
            *pop_to_d(),
            f"@{label_then}",
            jmp_clause,

            "D=0",
            f"@{label_endif}",
            "0;JMP",

            f"({label_then})",
            "D=-1",

            f"({label_endif})",
            *push_d(),
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

    # asm_fname = vm_filename.replace(".vm", "")
    # asm_fname += ".asm"

    # with open(asm_fname, 'w') as fout:
    #     fout.write(s)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print( "Usage: vm_translator file.vm" )
    else:
        main(sys.argv[1])

