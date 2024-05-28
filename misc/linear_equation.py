from maths_question_generator.arithmetic import Arithmetic
from maths_question_generator.utils import swap_num_with_placeholder


def generate() -> tuple[str, int]:
    a = Arithmetic().base()
    question, answer = swap_num_with_placeholder("x", a["question"].split())
    equation = f"{" ".join(question)} = {a['answer']}"
    return equation, int(answer)
