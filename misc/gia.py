from pprint import pprint

import requests
from sdamgia import SdamGIA

sdamgia = SdamGIA()
subject = "math"
# data = sdamgia.get_catalog(subject)
# pprint(data)
{
    "Простейшие уравнения": "6",
    "Уравнения": "13",
}


def take_categories(topic_id="6"):
    """Взять категории(category) для topic"""
    answer = []
    data = sdamgia.get_catalog(subject)
    for item in data:
        if item["topic_id"] == str(topic_id):
            for category in item["categories"]:
                answer.append((category["category_id"], category["category_name"]))
            return answer
    return


def take_problems(category_id):
    """Взять задачи из category"""
    data = sdamgia.get_category_by_id(subject, str(category_id))
    return data


def get_problem(problem_id):
    data = sdamgia.get_problem_by_id(subject, str(problem_id))
    return data

def get_analogs(problem_id):
    data = sdamgia.get_problem_by_id(subject, str(problem_id))['analogs']
    data = list(filter(lambda x: x != '...', data))
    return data


def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return write_file(r)


def write_file(response):
    filename = response.url.split("/")[-1]
    with open(f"./static/img/{filename}", "wb") as file:
        file.write(response.content)
    return filename

if __name__ == '__main__':
    pprint(get_analogs(9921))
    # pprint(get_problem(get_problem(26662)['analogs'][3])['id'])


# '''СдамГИА
# └── Предмет (subject)
#     ├── Каталог заданий (catalog)
#     │   └── Задание (topic)
#     │       └── Категория (category)
#     │           └── Задача (problem)
#     └── Тест (test)
#         └── Задача (problem)'''
#         └── Задача (problem)'''
