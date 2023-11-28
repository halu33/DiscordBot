import discord
from config import TOKEN
from discord.ext import commands
import logging


# Logging設定
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
                    filename='discordbot.log',
                    filemode='a')


# インテントの設定
intents = discord.Intents.all()

# ボットの設定
prefix = "?"
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True, help_command=None)

#bot起動時の処理 サーバー数を取得しステータスに表示、logにログインを記録
@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild_count} servers"))
    logging.info(f'Logged in : {bot.user}')

#エラーをログに記録
@bot.event
async def on_command_error(ctx, error):
    logging.error(f'コマンドエラー発生: {ctx.command} caused by {ctx.author}: {error}')
    await ctx.send(f'エラーが発生しました: {error}')


#コマンド設定

#test 挨拶
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")
    logging.info(f'helloコマンド実行: {ctx.author}')

#helpコマンド
@bot.command()
async def help(ctx):
    await ctx.send("https://halu33.net")
    logging.info(f'helpコマンド実行: {ctx.author}')


#bot起動
bot.run(TOKEN)
