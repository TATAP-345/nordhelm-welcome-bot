import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# 1. КОНФИГУРАЦИЯ И НАСТРОЙКИ
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("ВНИМАНИЕ: Токен BOT_TOKEN не найден в .env файле! Пожалуйста, укажите его.")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "1532395109474238495"))

# Интенты
intents = disnake.Intents.default()
intents.members = True          # Важно! Должен быть включен в панели разработчика Discord
intents.message_content = True

bot = commands.Bot(command_prefix="w!", intents=intents)


@bot.event
async def on_ready():
    print(f"ПРИВЕТСТВЕННЫЙ БОТ [{bot.user}] успешно запущен и находится в сети!")


@bot.event
async def on_member_join(member: disnake.Member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is not None:
        welcome_text = (
            f"Приветствуем, {member.mention}!\n"
            f"```prolog\n"
            f"добро_пожаловать_в_нордхельм:\n\n"
            f"новый_житель_в_городе:\n"
            f"  - шлюзы Периметра открываются, и мы рады приветствовать тебя в нашем заснеженном городе-государстве! "
            f"Холод за стенами силен, но у нашего Очага тебя всегда ждет тепло и уютная атмосфера.\n\n"
            f"с чего_начать_свой_путь:\n"
            f"  1: загляни в канал #📜┊устав-города, чтобы узнать правила выживания на сервере.\n"
            f"  2: переходи в #🪪┊личные-дела и заполни свою гражданскую карту. Магистрат внимательно изучит твои навыки "
            f"и выдаст тебе уникальную роль, ТК и тепловой класс!\n"
            f"  3: согревайся и общайся с другими жителями в нашем главном чате #☕┊очаг.\n\n"
            f"  - помни: Нордхельм стоит на дисциплине, а каждый новый гражданин — это новая сила для защиты нашего города! "
            f"Обустраивайся побыстрее, уву.\n"
            f"```"
        )
        await channel.send(welcome_text)
        print(f"[Приветствие] Встретили нового участника: {member.name}")
    else:
        print(f"[Ошибка] Канал приветствий с ID {WELCOME_CHANNEL_ID} не найден.")


if __name__ == "__main__":
    bot.run(TOKEN)
