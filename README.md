# VK Data Scraper

Этот проект представляет собой CLI-инструмент для сбора данных (постов, комментариев и лайков) из группы VK за определенный период времени и сохранения их в Excel-файл.

## Стек технологий

- Python 3.10+
- [VK API](https://vk.com/dev/methods) — для получения данных
- [Pandas](https://pandas.pydata.org/) — для обработки и записи данных в Excel
- [httpx](https://www.python-httpx.org/) — для отправки HTTP-запросов

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/username/VKWallParser.git
cd VKWallParser
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate  # Для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории проекта и добавьте туда токен VK API и версию API:

```env
VK_TOKEN=your_vk_api_token
API_VERSION=5.199
```

## Использование

Для запуска скрипта используйте команду:

```bash
python main.py <group_url> <start_date> <output_file>
```
* <group_url> — URL группы VK, например: https://vk.com/public12345
* <start_date> — дата начала периода в формате YYYY-MM-DD, начиная с которой будут собираться данные
* <output_file> — путь до Excel-файла, куда будут сохранены данные, например: output.xlsx

## Пример:

```bash
python main.py https://vk.com/public12345 2024-01-01 vk_data.xlsx
```

## Описание процесса
1. Скрипт принимает URL группы VK, преобразует его в domain или owner_id для использования с VK API.
2. С указанной даты и до текущего момента собираются посты, комментарии и лайки.
3. Данные сохраняются в Excel-файл на 3 листа: Посты, Комментарии, Лайки.

## Структура данных

### Посты:

* post_id: ID поста
* text: Текст поста
* date: Дата публикации поста
* likes: Количество лайков
* comments: Количество комментариев

### Комментарии:

* post_id: ID поста, к которому относится комментарий
* user_id: ID пользователя, оставившего комментарий
* text: Текст комментария
* date: Дата публикации комментария

### Лайки:

* post_id: ID поста, к которому относятся лайки
* user_id: ID пользователя, поставившего лайк
