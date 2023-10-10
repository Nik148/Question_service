# Question_service
Веб-сервис для работы с вопросами

После запуска сервиса документацию можно посмотреть по url: http://localhost:8000/docs
## Инструкция к запуску сервиса
### Запуск с помощью Docker:
```
docker-compose build
docker-compose up
```
### Запуск в локальной системе:

Нужно сначала создать файл .env и в нем прописать ваши парамертры (тестовую бд можно не создавать, она создастся сама при тестировании):
```
DB_URL=postgresql+asyncpg://postgres:admin@localhost:5432/question_service
TEST_DB_URL=postgresql+asyncpg://postgres:admin@localhost:5432/test_question_service
TEST_DB_NAME=test_question_service
```
Подготовка к запуску:
```
python virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```
Запуск сервиса:
```
python main.py
```
## Тестирование
```
pytest test
```
