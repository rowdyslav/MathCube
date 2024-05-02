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
    data = sdamgia.get_catalog(subject)
    for i in data:
        if i['topic_id'] == str(topic_id):
            return i['categories']
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

pprint(take_categories(13))

# '''СдамГИА
# └── Предмет (subject)
#     ├── Каталог заданий (catalog)
#     │   └── Задание (topic)
#     │       └── Категория (category)
#     │           └── Задача (problem)
#     └── Тест (test)
#         └── Задача (problem)'''
