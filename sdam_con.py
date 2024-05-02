import requests
from sdamgia import SdamGIA
from pprint import pprint

sdamgia = SdamGIA()
subject = 'math'
# data = sdamgia.get_catalog(subject)
# pprint(data)
{
  'Простейшие уравнения': '6',
  'Уравнения': '13',
}
def take_categories(topic_id='6'):
    """Взять категории(category) для topic"""
    answer = []
    data = sdamgia.get_catalog(subject)
    for item in data:
        if item['topic_id'] == str(topic_id):
            for category in item['categories']:
                answer.append((category['category_id'], category['category_name']))
            return answer
    return

def take_problems(categori_id):
    """Взять задачи из category"""
    data = sdamgia.get_category_by_id(subject, str(categori_id))
    return data

def get_problem(problem_id):
    data = sdamgia.get_problem_by_id(subject, str(problem_id))
    filename = get_file(data['condition']['images'][0])
    return {'filename': filename, 'data' : data}

def get_file(url):
    r = requests.get(url, allow_redirects=True)
    write_file(r)


def write_file(response):
    filename = response.url.split('/')[-1]
    with open(f'./static/img/{filename}', 'wb') as file:
        file.write(response.content)
    return filename

pprint(take_problems(14))

# '''СдамГИА
# └── Предмет (subject)
#     ├── Каталог заданий (catalog)
#     │   └── Задание (topic)
#     │       └── Категория (category)
#     │           └── Задача (problem)
#     └── Тест (test)
#         └── Задача (problem)'''
