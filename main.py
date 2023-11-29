import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN, GUILD_ID
import logging

# Logging設定
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
                    filename='discordbot.log',
                    filemode='a')

# インテントの設定
intents = discord.Intents.all()

# ボットの設定
bot = commands.Bot(command_prefix="?", intents=intents, case_insensitive=True, help_command=None)

#スラッシュコマンド用のTreeを取得
tree = bot.tree


# スラッシュコマンドの定義

#testコマンド
@tree.command(name='test', description="テストコマンド")
async def hello(interaction: discord.Interaction, str: str):
    await interaction.response.send_message(f"Hello {str}!")

#挨拶コマンド
@tree.command(name='hello', description="あいさつをします")
async def hello(interaction: discord.Interaction):
    user_name = interaction.user.display_name   # ユーザーの表示名を取得
    await interaction.response.send_message(f"Hello {user_name}!")

#bot招待リンク
@tree.command(name='invite', description="botの招待リンク")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("https://discord.com/api/oauth2/authorize?client_id=889950735867969546&permissions=8&scope=bot")


#四則演算
@tree.command(name='add', description="二つの数を足します")
async def add(interaction: discord.Interaction, x: int, y: int):
    answer_add = x + y
    await interaction.response.send_message(f"{x} + {y} = {answer_add}")

@tree.command(name='sub', description="二つの数の差を求めます")
async def sub(interaction: discord.Interaction, x: int, y: int):
    answer_sub = x - y
    await interaction.response.send_message(f"{x} - {y} = {answer_sub}")

@tree.command(name='mul', description="二つの数を掛けます")
async def mul(interaction: discord.Interaction, x: int, y: int):
    answer_mul = x * y
    await interaction.response.send_message(f"{x} * {y} = {answer_mul}")

@tree.command(name='div', description="二つの数を割ります")
async def div(interaction: discord.Interaction, x: int, y: int):
    answer_div = x / y
    await interaction.response.send_message(f"{x} / {y} = {answer_div}")

@tree.command(name='mod', description="二つの数の剰余を求めます")
async def mod(interaction: discord.Interaction, x: int, y: int):
    answer_mod = x % y
    await interaction.response.send_message(f"{x} % {y} = {answer_mod}")

@tree.command(name='exp', description="数の累乗を求めます")
async def exp(interaction: discord.Interaction, x: int, y: int):
    answer_exp = x ** y
    await interaction.response.send_message(f"{x} ^ {y} = {answer_exp}")


#bot起動時の処理
@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild_count} servers"))
    logging.info(f'Logged in : {bot.user}')
    await tree.sync()
    await tree.sync(guild=discord.Object(id=GUILD_ID))

# エラーハンドリングとログ記録
@bot.event
async def on_command_completion(ctx):
    logging.info(f'コマンド実行: {ctx.command} by {ctx.author}')

# ボット起動
bot.run(TOKEN)