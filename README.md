# Личностный тест Майерс-Бриггс

Requirements:

- Python (v3.8.1)
- Django (v3.2.18)
- Pandas (v1.5.3)

### Быстрый старт

Установить пакеты через pip из файла:
```commandline
pip install -r requirements.txt
```

Осуществить миграции в базу данных:
```commandline
python manage.py migrate
```

Загрузить начальную информацию:
```commandline
python manage.py load_dummy_questions
python manage.py load_dummy_descriptor_info
```

Запустить приложение:
```commandline
python manage.py runserver
```

Результаты тестирования сохраняются в панели администратора, для входа в нее необходимо создать суперпользователя:
```commandline
python manage.py createsuperuser
```

И перейти в панель администратора по адресу:
```
/admin
```

### Структура приложения
    .
    ├── myers_briggs_personality_test   # Ресурсная папка сайта
    │   ├── apps                        # Каталог со всеми приложениями django
    │   │    └── personality_test       # Приложение тест
    │   │       ├── locale              # Каталог с локализацией
    │   │       ├── management          # Каталог с дополнительной функциональностью приложения
    │   │       │       ├──commands     # Каталог с консольными командами
    │   │       │       └──dummy        # Каталог с начальной информацией 
    │   │       ├── migrations          # Каталог с миграциями
    │   │       ├── templates           # Каталог с шаблонами Django
    │   │       ├── fields.py           # Файл с полями для форма Django
    │   │       ├── forms.py            # Файл с описанием форм Django
    │   │       └── utils.py            # Файл с утилитами для приложения
    │   ├── settings.py                 # Файл настроек проекта
    │   └── urls.py                     # Файл проекта с основными маршрутами
    ├── templates                       # Директория с базовыми шаблонами для сайта
    ├── manage.py                       # Основной файл django
    ├── requirements.txt                # Файл requirements.txt с модулями pip
    └── README.md             
