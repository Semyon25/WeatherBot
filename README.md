# Weather Telegram Bot

Телеграм-бот на базе aiogram 3, который показывает текущую погоду и прогноз на сегодня и завтра, а также присылает ежедневное уведомление в 10:00.

---

## Установка

1. Склонируйте репозиторий:

```bash
git clone <адрес_репозитория>
cd weather_bot
```

2. Создайте и активируйте виртуальное окружение (рекомендуется):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `.env.example` и заполните его своими данными:

```
BOT_TOKEN=ваш_токен_бота
WEATHER_API_KEY=ключ_сервиса_weatherapi.com
USER_ID=ваш_телеграм_id
DATABASE_URL=your_connection_string
```

5. Запустите бота:

```bash
python bot.py
```

---
