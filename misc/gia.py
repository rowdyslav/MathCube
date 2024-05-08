from pprint import pprint

import requests
from sdamgia import SdamGIA

sdamgia = SdamGIA()
subject = "math"


def get_categories(topic_id="6") -> list[tuple[str, str]] | None:
    """Взять категории(category) для topic"""
    answer = []
    data = sdamgia.get_catalog(subject)
    for item in data:
        if item["topic_id"] == str(topic_id):
            for category in item["categories"]:
                answer.append((category["category_id"], category["category_name"]))
            return answer
    return [(0, 'Произошла ошибка')]


def get_category(category_id):
    """Взять задачи из category"""
    data = sdamgia.get_category_by_id(subject, str(category_id))
    return data


def get_problem(problem_id):
    data = sdamgia.get_problem_by_id(subject, str(problem_id))
    return data


def get_analogs(problem_id):
    data = sdamgia.get_problem_by_id(subject, str(problem_id))["analogs"]
    data = list(filter(lambda x: x != "...", data))
    return data
