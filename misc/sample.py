from typing import Literal

from maths_question_generator.arithmetic import Arithmetic


def generate(opers: list[Literal["+", "-", "*", "/"]]) -> tuple[str, int]:
    a = Arithmetic(opers=opers).base()
    return a["question"], int(a["answer"])
