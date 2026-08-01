import sys
import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

# Настройка UTF-8 вывода для Windows консоли
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

# ID канала, куда бот будет отправлять приветствия
WELCOME_CHANNEL_ID = 1532395109474238495

intents = disnake.Intents.default()
intents.members = True          # Важно! Проверь этот тумблер в панели ИМЕННО ЭТОГО бота
intents.message_content = True

bot = commands.Bot(command_prefix="w!", intents=intents)

@bot.event
async def on_ready():
    print(f"ПРИВЕТСТВЕННЫЙ БОТ [{bot.user}] успешно запущен и в сети!")

@bot.event
async def on_member_join(member: disnake.Member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        try:
            channel = await bot.fetch_channel(WELCOME_CHANNEL_ID)
        except Exception:
            channel = None

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
            f"  2: переходи в #🪪┊личные-дела и заполни свою гражданскую карту. Магистрата внимательно изучит твои навыки "
            f"и выдаст тебе уникальную роль, ТК и тепловой класс!\n"
            f"  3: согревайся и общайся с другими жителями в нашем главном чате #☕┊очаг.\n\n"
            f"  - помни: Нордхельм стоит на дисциплине, а каждый новый гражданин — это новая сила для защиты нашего города! "
            f"Обустраивайся побыстрее, уву.\n"
            f"```"
        )
        await channel.send(welcome_text)
        print(f"[Приветствие] Встретили участника {member.name}")
    else:
        print(f"[Ошибка] Канал приветствий {WELCOME_CHANNEL_ID} не найден.")

# Токен ПЕРВОГО бота (приветственного)
bot.run(os.getenv('BOT_TOKEN'))
