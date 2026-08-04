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
intents.members = True
intents.message_content = True

# sync_commands=True принудительно регистрирует слэш-команды в Discord
bot = commands.Bot(
    command_prefix="w!",
    intents=intents,
    sync_commands=True,
    sync_commands_debug=True
)

@bot.event
async def on_ready():
    print(f"ПРИВЕТСТВЕННЫЙ БОТ [{bot.user}] успешно запущен и в сети!")
    print(f"Зарегистрировано команд: {[cmd.name for cmd in bot.slash_commands]}")

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

# --- СЛЭШ-КОМАНДА: /сказать ---
@bot.slash_command(
    name="сказать",
    description="Отправить сообщение/объявление с несколькими картинками от лица бота (Только Админы)",
    default_member_permissions=disnake.Permissions(administrator=True)
)
async def say_slash(
    inter: disnake.ApplicationCommandInteraction,
    channel: disnake.TextChannel = commands.Param(description="Канал, куда отправить сообщение"),
    text: str = commands.Param(description="Текст сообщения (поддерживает \\n для переноса строк)"),
    title: str = commands.Param(default=None, description="Заголовок (если нужно отправить цветным embed)"),
    image_url: str = commands.Param(default=None, description="Прямая ссылка на картинку (https://...)"),
    file1: disnake.Attachment = commands.Param(default=None, description="Первая картинка / файл"),
    file2: disnake.Attachment = commands.Param(default=None, description="Вторая картинка / файл"),
    file3: disnake.Attachment = commands.Param(default=None, description="Третья картинка / файл"),
    file4: disnake.Attachment = commands.Param(default=None, description="Четвертая картинка / файл"),
    file5: disnake.Attachment = commands.Param(default=None, description="Пятая картинка / файл"),
    as_embed: bool = commands.Param(default=False, description="Отправить в виде цветного Embed блока?")
):
    formatted_text = text.replace("\\n", "\n")

    try:
        attachments_list = [f for f in [file1, file2, file3, file4, file5] if f is not None]
        disnake_files = []
        for att in attachments_list:
            disnake_files.append(await att.to_file())

        if as_embed or title:
            embed_title = title if title else "📢 Сообщение"
            embed = disnake.Embed(title=embed_title, description=formatted_text, color=disnake.Color.blue())
            
            if image_url:
                embed.set_image(url=image_url)
            elif attachments_list and attachments_list[0].content_type and attachments_list[0].content_type.startswith("image/"):
                embed.set_image(url=f"attachment://{attachments_list[0].filename}")

            if disnake_files:
                await channel.send(embed=embed, files=disnake_files)
            else:
                await channel.send(embed=embed)
        else:
            msg = formatted_text
            if image_url:
                msg += f"\n{image_url}"

            if disnake_files:
                await channel.send(content=msg, files=disnake_files)
            else:
                await channel.send(content=msg)

        await inter.response.send_message(f"✅ Сообщение с фотографиями успешно отправлено от лица бота в {channel.mention}", ephemeral=True)
    except disnake.Forbidden:
        await inter.response.send_message(f"❌ У бота нет прав для отправки сообщений в канал {channel.mention}", ephemeral=True)
    except Exception as e:
        await inter.response.send_message(f"❌ Ошибка отправки: `{e}`", ephemeral=True)

# --- ПРЕФИКС-КОМАНДА: w!say или w!сказать ---
@bot.command(name="сказать", aliases=["say"])
@commands.has_permissions(administrator=True)
async def say_prefix(ctx: commands.Context, channel: disnake.TextChannel, *, text: str = ""):
    formatted_text = text.replace("\\n", "\n")
    try:
        files_to_send = []
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                files_to_send.append(await attachment.to_file())
        
        if files_to_send:
            await channel.send(content=formatted_text, files=files_to_send)
        else:
            await channel.send(content=formatted_text)

        try:
            await ctx.message.delete()
        except Exception:
            pass
    except Exception as e:
        await ctx.send(f"❌ Ошибка отправки: {e}", delete_after=5)

bot.run(os.getenv('BOT_TOKEN'))
