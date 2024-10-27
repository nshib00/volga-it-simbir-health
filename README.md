# volga-it-simbir-health


## Swagger

**Account:** http://localhost:8081/docs

**Hospital:** http://localhost:8082/docs

**Timetable:** http://localhost:8083/docs

**Document:** http://localhost:8084/docs

## Elasticsearch и Kibana

**Elasticsearch:** http://localhost:9200

**Kibana:** http://localhost:5601


## Конфигурация

Данные для подключения каждого из микросервисов к БД находятся соответственно в файлах:
- `account/.account-prod.env`
- `hospital/.hospital-prod.env`
- `timetable/.timetable-prod.env`
- `document/.document-prod.env`

В файлах указаны данные для подключения к PostgreSQL по умолчанию.

В этих файлах переменные с префиксом `DB_` нужны для работы приложения с БД, а с префиксом `POSTGRES_` - для подключения БД в контейнере.

## Сборка

`docker-compose up -d` 

## Отличия от исходного задания

Помимо API методов из задания, были также реализованы следующие методы:

1. Микросервис `account`: 
    - `GET /api/Accounts/Pacients` - возвращает список всех пациентов (пользователей с ролью User).
    Доступен администраторам, менеджерам и врачам.
    - `GET /api/Accounts/Pacients/{user_id}` - возвращает пациента с id=user_id.
    Доступен администраторам, менеджерам и врачам.
2. Микросервис `document`:
    - `POST /api/History/Search` - поиск по документам через Elasticsearch.

        В теле запроса для поиска должен быть один обязательный параметр: `dataQuery`- поисковой запрос по записям истории болезней, т.е. по полю `data`.
        Дополнительные опциональные параметры для поиска: `pacientId`, `historyDate`, `hospitalId`, `doctorId`.
        Метод доступен администраторам, менеджерам и врачам.