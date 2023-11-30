import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN, GUILD_ID, INVITE
from help_commands import commands_description, detailed_commands_description
import math
import logging

#Logging設定
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
                    filename='discordbot.log',
                    filemode='a')

#インテントの設定
intents = discord.Intents.all()

#ボットの設定
bot = commands.Bot(command_prefix="?", intents=intents, case_insensitive=True, help_command=None)

#スラッシュコマンド用のTreeを取得
tree = bot.tree


#スラッシュコマンドの定義

#テストコマンド
@tree.command(name='test', description="テストコマンド")
@app_commands.describe(str="文字")
async def test(interaction: discord.Interaction, str: str = None):
    if str:
        message = f"yo! {str}" #引数が入力された場合
    else:
        message = "yo!" #引数が入力されなかった場合
    await interaction.response.send_message(message)

#helpコマンド
@tree.command(name='help', description="helpコマンド")
@app_commands.describe(command="コマンド名（任意）")
@app_commands.choices(command=[
    app_commands.Choice(name=cmd, value=cmd) for cmd in commands_description.keys()
])
async def help(interaction: discord.Interaction, command: str = None):
    if command is None:
        messages = [f"/{cmd}: {desc}" for cmd, desc in commands_description.items()]
        await interaction.response.send_message("\n".join(messages))
    elif command in detailed_commands_description:
        await interaction.response.send_message(f"/{command}: {detailed_commands_description[command]}")
    else:
        await interaction.response.send_message(f"コマンド '{command}' は存在しません。")

#挨拶コマンド
@tree.command(name='hello', description="社会不適合者による残念な挨拶")
async def hello(interaction: discord.Interaction):
    user_name = interaction.user.display_name   #ユーザーの表示名を取得
    await interaction.response.send_message(f"よお{user_name}!")

#bot招待リンク
@tree.command(name='invite', description="botの招待リンク")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'botの招待リンク:{INVITE}')

#四則演算
@tree.command(name='add', description="たし算")
@app_commands.describe(num1="第一項", num2="第二項", num3="第三項（任意）", num4="第四項（任意）", num5="第五項（任意）")
async def add(interaction: discord.Interaction, num1: int, num2: int, num3: int = None, num4: int = None, num5: int = None):
    numbers = [num1, num2] + [num for num in [num3, num4, num5] if num is not None]
    total = sum(numbers)
    numbers_str = " + ".join(map(str, numbers))
    await interaction.response.send_message(f"{numbers_str} = {total}")

@tree.command(name='sub', description="ひき算")
@app_commands.describe(num1="第一項", num2="第二項", num3="第三項（任意）", num4="第四項（任意）", num5="第五項（任意）")
async def sub(interaction: discord.Interaction, num1: int, num2: int, num3: int = None, num4: int = None, num5: int = None):
    numbers = [num1, -num2] + [-num for num in [num3, num4, num5] if num is not None]
    result = sum(numbers)
    numbers_str = " - ".join(map(str, [num1] + [num2, num3, num4, num5]))
    await interaction.response.send_message(f"{numbers_str} = {result}")

@tree.command(name='mul', description="かけ算")
@app_commands.describe(num1="第一項", num2="第二項", num3="第三項（任意）", num4="第四項（任意）", num5="第五項（任意）")
async def mul(interaction: discord.Interaction, num1: int, num2: int, num3: int = None, num4: int = None, num5: int = None):
    numbers = [num1, num2] + [num for num in [num3, num4, num5] if num is not None]
    result = math.prod(numbers)
    numbers_str = " * ".join(map(str, numbers))
    await interaction.response.send_message(f"{numbers_str} = {result}")

@tree.command(name='div', description="わり算")
@app_commands.describe(num1="被除数", num2="除数", num3="除数（任意）", num4="除数（任意）", num5="除数（任意）")
async def div(interaction: discord.Interaction, num1: int, num2: int, num3: int = None, num4: int = None, num5: int = None):
    if num2 == 0 or (num3 == 0 and num3 is not None) or (num4 == 0 and num4 is not None) or (num5 == 0 and num5 is not None):
        await interaction.response.send_message("0で割ることはできません。")
        return
    numbers = [num1, num2] + [num for num in [num3, num4, num5] if num is not None]
    result = numbers[0]
    for num in numbers[1:]:
        result /= num
    await interaction.response.send_message(f"{' / '.join(map(str, numbers))} = {result}")

@tree.command(name='mod', description="剰余")
@app_commands.describe(x="被除数", y="除数", x3="除数（任意）", x4="除数（任意）", x5="除数（任意）")
async def mod(interaction: discord.Interaction, x: int, y: int, x3: int = None, x4: int = None, x5: int = None):
    if y == 0 or (x3 == 0 and x3 is not None) or (x4 == 0 and x4 is not None) or (x5 == 0 and x5 is not None):
        await interaction.response.send_message("0で割ることはできません。")
        return
    numbers = [x, y] + [num for num in [x3, x4, x5] if num is not None]
    result = numbers[0] % numbers[1]
    for num in numbers[2:]:
        result %= num
    numbers_str = " % ".join(map(str, numbers))
    await interaction.response.send_message(f"{numbers_str} = {result}")

@tree.command(name='exp', description="累乗")
@app_commands.describe(mode="基数の種類（自然対数の底、または他の実数）", exponent="指数", base="基数（他の実数の場合）")
@app_commands.choices(mode=[
    app_commands.Choice(name='自然対数の底 e', value='e'),
    app_commands.Choice(name='他の実数', value='other')
])
async def exp(interaction: discord.Interaction, mode: str, exponent: int, base: float = None):
    if mode == 'e':
        result = math.exp(exponent)
    elif mode == 'other':
        if base is None:
            await interaction.response.send_message("基数を入力してください。")
            return
        result = base ** exponent
    else:
        await interaction.response.send_message("無効なモードが指定されました。")
        return
    await interaction.response.send_message(f"{base if mode == 'other' else 'e'} ^ {exponent} = {result}")

@tree.command(name='log', description="対数")
@app_commands.describe(mode="対数の種類（自然対数、常用対数、二進対数）", value="対数を取る値")
@app_commands.choices(mode=[
    app_commands.Choice(name='自然対数', value='natural'),
    app_commands.Choice(name='常用対数', value='common'),
    app_commands.Choice(name='二進対数', value='binary')
])
async def log(interaction: discord.Interaction, mode: str, value: float):
    if mode == 'natural':
        result = math.log(value)
    elif mode == 'common':
        result = math.log10(value)
    elif mode == 'binary':
        result = math.log2(value)
    else:
        await interaction.response.send_message("無効なモードが指定されました。")
        return
    await interaction.response.send_message(f"{mode}({value}) = {result}")

@tree.command(name='root', description="平方根または累乗根")
@app_commands.describe(mode="計算モード（平方根または累乗根）", value="根を取る値", radical="累乗根の次数")
@app_commands.choices(mode=[
    app_commands.Choice(name='平方根', value='sqrt'),
    app_commands.Choice(name='累乗根', value='nroot')
])
async def root(interaction: discord.Interaction, mode: str, value: float, radical: int = 2):
    if mode == 'sqrt':
        result = math.sqrt(value)
        await interaction.response.send_message(f"√{value} = {result}")
    elif mode == 'nroot':
        if radical <= 0:
            await interaction.response.send_message("根の次数は正の整数でなければなりません。")
            return
        result = value ** (1 / radical)
        await interaction.response.send_message(f"{value} の {radical} 乗根 = {result}")
    else:
        await interaction.response.send_message("無効なモードが指定されました。")

@tree.command(name='sin', description="正弦(sin)・逆正弦(arcsin)")
@app_commands.describe(mode="モード（sin or arcsin）", value="角度（度数法）または値")
@app_commands.choices(mode=[
    app_commands.Choice(name='sin', value='sin'),
    app_commands.Choice(name='arcsin', value='arcsin')
])
async def sin(interaction: discord.Interaction, mode: str, value: float):
    if mode == 'sin':
        result = math.sin(math.radians(value))
        await interaction.response.send_message(f"sin({value}) = {result}")
    elif mode == 'arcsin':
        result = math.degrees(math.asin(value))
        await interaction.response.send_message(f"arcsin({value}) = {result} degrees")
    else:
        await interaction.response.send_message("無効なモードが指定されました。")

@tree.command(name='cos', description="余弦(cos)・逆余弦(arccos)")
@app_commands.describe(mode="モード（cos or arccos）", value="角度（度数法）または値")
@app_commands.choices(mode=[
    app_commands.Choice(name='cos', value='cos'),
    app_commands.Choice(name='arccos', value='arccos')
])
async def cos(interaction: discord.Interaction, mode: str, value: float):
    if mode == 'cos':
        result = math.cos(math.radians(value))
        await interaction.response.send_message(f"cos({value}) = {result}")
    elif mode == 'arccos':
        result = math.degrees(math.acos(value))
        await interaction.response.send_message(f"arccos({value}) = {result} degrees")
    else:
        await interaction.response.send_message("無効なモードが指定されました。")

@tree.command(name='tan', description="正接(tan)・逆正接(arctan)")
@app_commands.describe(mode="モード（tan or arctan）", value="角度（度数法）または値")
@app_commands.choices(mode=[
    app_commands.Choice(name='tan', value='tan'),
    app_commands.Choice(name='arctan', value='arctan')
])
async def tan(interaction: discord.Interaction, mode: str, value: float):
    if mode == 'tan':
        result = math.tan(math.radians(value))
        await interaction.response.send_message(f"tan({value}) = {result}")
    elif mode == 'arctan':
        result = math.degrees(math.atan(value))
        await interaction.response.send_message(f"arctan({value}) = {result} degrees")
    else:
        await interaction.response.send_message("無効なモードが指定されました。")


@tree.command(name='sigma', description="数列Σの計算")
@app_commands.describe(k="シグマの下限値", n="シグマの上限値", sequence="計算する数列の式（'k'を変数として使用）例:k、k*k、k+3など")
async def sigma(interaction: discord.Interaction, k: int, n: int, sequence: str):
    try:
        total = sum(eval(sequence.replace("k", str(i))) for i in range(k, n + 1))
        await interaction.response.send_message(f"Σ({sequence}) from {k} to {n} = {total}")
    except Exception as e:
        await interaction.response.send_message(f"式の計算中にエラーが発生しました: {e}")


#bot起動時の処理
@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild_count} servers"))
    logging.info(f'Logged in : {bot.user}')
    await tree.sync()
    await tree.sync(guild=discord.Object(id=GUILD_ID))

#エラーハンドリングとログ記録
@bot.event
async def on_command_completion(ctx):
    logging.info(f'コマンド実行: {ctx.command} by {ctx.author}')

#bot起動
bot.run(TOKEN)