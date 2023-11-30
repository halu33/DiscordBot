import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN, GUILD_ID, INVITE
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

#全コマンドの簡単な説明の辞書
commands_description = {
    'test': 'テストコマンド',
    'help': 'helpコマンド',
    'hello': '社会不適合者による残念な挨拶',
    'invite': 'botの招待リンク',
    'add': 'たし算',
    'sub': 'ひき算',
    'mul': 'かけ算',
    'div': 'わり算',
    'mod': '剰余',
    'exp': '累乗',
    'log': '対数',
    'sqrt': '平方根',
    'sin': '正弦(sin)',
    'cos': '余弦(cos)',
    'tan': '正接(tan)',
    'sigma': '数列Σの計算'
}

#helpコマンドの実装
@tree.command(name='help', description="helpコマンド")
@app_commands.describe(command="コマンド名（任意）")
async def help(interaction: discord.Interaction, command: str = None):
    if command is None:
        #全コマンドの説明を表示
        messages = [f"/{cmd}: {desc}" for cmd, desc in commands_description.items()]
        await interaction.response.send_message("\n".join(messages))
    elif command in commands_description:
        #特定のコマンドの詳細を表示
        await interaction.response.send_message(f"/{command}: {commands_description[command]}")
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
@app_commands.describe(x="被除数", y="除数")
async def mod(interaction: discord.Interaction, x: int, y: int):
    result = x % y
    await interaction.response.send_message(f"{x} % {y} = {result}")

@tree.command(name='exp', description="累乗")
@app_commands.describe(base="基数", exponent="指数")
async def exp(interaction: discord.Interaction, base: int, exponent: int):
    result = base ** exponent
    await interaction.response.send_message(f"{base} ^ {exponent} = {result}")

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


@tree.command(name='sqrt', description="平方根")
@app_commands.describe(value="平方根を取る値")
async def sqrt(interaction: discord.Interaction, value: float):
    result = math.sqrt(value)
    await interaction.response.send_message(f"√{value} = {result}")

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