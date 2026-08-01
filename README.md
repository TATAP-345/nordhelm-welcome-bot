# ❄️ Nordhelm Welcome Bot

Discord бот для автоматического приветствия новых участников на сервере **Nordhelm RP**.

## 📌 Функционал
- 👋 Отслеживает событие входа нового участника на сервер (`on_member_join`).
- 📜 Отправляет атмосферное, красиво форматированное сообщение в блок-коде `prolog` с указанием путеводителя по серверу (устав города, заполнение паспорта, главный чат).

## 🛠️ Установка и запуск

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/TATAP-345/nordhelm-welcome-bot.git
   cd nordhelm-welcome-bot
   ```

2. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте переменные окружения**:
   Переименуйте `.env.example` в `.env` и укажите данные вашего бота:
   ```env
   BOT_TOKEN=ваш_токен_бота
   WELCOME_CHANNEL_ID=1532395109474238495
   ```

4. **Запустите бота**:
   ```bash
   python main.py
   ```

## ⚙️ Важно перед запуском!
В **Discord Developer Portal** для данного бота ОБЯЗАТЕЛЬНО должен быть включен следующий тумблер:
- **Server Members Intent** (в разделе `Bot` -> `Privileged Gateway Intents`).
