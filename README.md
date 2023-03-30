## Порядок команд для запуска
```
docker compose up -d
docker compose exec web /bin/sh
poetry install
poetry shell
make migrate head
make run
```

## Ниже все команды по работе с репозиторием

### Требования

Необходимо, чтобы были установлены следующие компоненты:

- `Docker` и `docker-compose`
- `Python 3.10`
- `Poetry`

### Установка

1. Создание виртуального окружения и установка зависимостей:
```commandline
poetry install
```

2. Активация виртуального окружения:

```commandline
poetry shell
```


### Запуск

0. Создание `.env` файла с необходимыми переменными:
```commandline
make env
```

1. Создание базы в docker-контейнере (чтобы не работать с локальной базой):
```commandline
make db
```
2. Выполнение миграций:
```commandline
make migrate head
```
3. Запуск приложения:
```commandline
make run
```

### Тестирование

- Запуск тестов со всеми необходимыми флагами:
```commandline
make test
```

- Запуск тестов с генерацией отчета о покрытии:
```commandline
make test-cov
```

### Статический анализ

- Запуск линтеров:
```commandline
make lint
```

- Запуск форматирования кода:
```commandline
make format
```

### Дополнительные команды

- Создание новой ревизии:
```commandline
make revision
```
- Открытие базы данных внутри Docker-контейнера:
```commandline
make open_db
```

- Вывести список всех команд и их описание:
```commandline
make help
```
