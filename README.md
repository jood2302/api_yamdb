# Яндекс.Практикум

# курс Python-разработчик

## Учебный проект sprint_10.  Проект YaMDb.

***
Цель работы над проектом - получить опыт командной работы.

***

### Задание. ###

Изначально в репозиторий api_yamdb сохранён пустой Django-проект.

К проекту по адресу ht<span>tp://127.0</span>.0.1:8000/redoc/ подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

**Задача**: — написать бэкенд проекта (приложение reviews) и API для него (приложение api) так, чтобы они полностью соответствовали документации.

**Обязательно**: заполнение описания проекта в файле README.md.

### Техническое описание проекта YaMDb. ###

Проект **YaMDb** собирает отзывы (*Review*) пользователей на произведения (*Titles*).

Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (*Category*) может быть расширен администратором.

Произведению может быть присвоен жанр (*Genre*) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (*Review*) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — *рейтинг* (целое число). На одно произведение пользователь может оставить только один отзыв.

Отзыв может быть прокомментирован (*Сomment*) пользователями.




* **Пользовательские роли**
	* Аноним — может просматривать описания произведений, читать отзывы и комментарии.
	* Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
	* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
	* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
	* Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

* **Самостоятельная регистрация новых пользователей**
	* Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
	* Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
	* Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
	* В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
	* После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

* **Создание пользователя администратором**
	* Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт api/v1/users/ (описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.
	* После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему должно прийти письмо с кодом подтверждения.
	* Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.

* **Ресурсы API YaMDb**
	* Ресурс auth: аутентификация.
	* Ресурс users: пользователи.
	* Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
	* Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
	* Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
	* Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
	* Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
	* Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

* **Связанные данные и каскадное удаление**
	* При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
	* При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
	* При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.
	* При удалении объекта категории Category не нужно удалять связанные с этой категорией произведения.
	* При удалении объекта жанра Genre не нужно удалять связанные с этим жанром произведения.

* **База данных**
	* В репозитории с заданием, в директории /api_yamdb/static/data, подготовлены несколько файлов в формате csv с контентом для ресурсов Users, Titles, Categories, Genres, Review и Comments.
	* Для тестирования работы проекта можно наполнить БД данным контентом из приложенных csv-файлов.
	* Процедура импорта из CSV - на усмотрение исполнителя. Неплохо получить опыт по написанию собственной managment-команды.

* **Распределение задач в команде**
	* Вариант распределения работы между участниками:
		* Первый разработчик пишет всю часть, касающуюся управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с токеном, систему подтверждения через e-mail.
		* Второй разработчик пишет категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.
		* Третий разработчик занимается отзывами (Review) и комментариями (Comments): описывает модели, представления, настраивает эндпойнты, определяет права доступа для запросов. Рейтинги произведений тоже достаются третьему разработчику.

***


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.dev/coherentus/api_yamdb
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

Для *nix-систем:
```bash
source venv/bin/activate
```

Для windows-систем:
```bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```bash
cd api_yamdb
python3 manage.py migrate
```

Создать суперпользователя (для раздачи прав админам):

```bash
python manage.py createsuperuser
```

Запустить проект:

```bash
python manage.py runserver
```

Сам проект и админ-панель искать по адресам:
```bash
http://127.0.0.1:8000

http://127.0.0.1:8000/admin
```
***

<a name="Описание"></a>

### Описание эндпоинтов:

- [Auth](api_yamdb/static/readme_files/README_Auth.md)
- [Categories](api_yamdb/static/readme_files/README_Categories.md)
- [Genres](api_yamdb/static/readme_files/README_Genres.md)
- [Titles](api_yamdb/static/readme_files/README_Titles.md)
- [Reviews](api_yamdb/static/readme_files/README_Reviews.md)
- [Comments](api_yamdb/static/readme_files/README_Comments.md)
- [Users](api_yamdb/static/readme_files/README_Users.md)

***

### Примечания:


* ### Authentication

    jwt-token

    Используется аутентификация с использованием JWT-токенов

    Security Scheme Type: `API Key`

    Header parameter name: `Bearer`


* ### *Импорт csv-файлов*

    ```bash
    python manage.py import_csv
    ```
***

***Над проектом работали:***
* Евгений Анохин | Github:https://github.com/Evgen4567 | Разработчик, кастомная модель User, регистрация и аутентификация пользователей.
* Роман Романенко| Github:https://github.com/roman7373 | Разработчик, контент Администратора.
* Леонид Славутин | Github:https://github.com/jood2302 | Тимлид,, контент пользователей.