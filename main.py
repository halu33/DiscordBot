import discord
from discord.ext import commands
from discord import app_commands
from help_commands import commands_description, detailed_commands_description
import math
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')
INVITE = os.environ.get('INVITE')


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
@app_commands.describe(str="文字をここに打てyo！！")
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
    await interaction.response.send_message(f"よお{user_name}")

#bot招待リンク
@tree.command(name='invite', description="botの招待リンク")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'botの招待リンク:{INVITE}')

#関数電卓
math = app_commands.Group(name="math", description="数学計算コマンド")

@math.command(name="add", description="たし算")
@app_commands.describe(num1="第一項", num2="第二項", num3="第三項（任意）", num4="第四項（任意）", num5="第五項（任意）")
async def math_add(interaction: discord.Interaction, num1: int, num2: int, num3: int = None, num4: int = None, num5: int = None):
    numbers = [num1, num2] + [num for num in [num3, num4, num5] if num is not None]
    total = sum(numbers)
    numbers_str = " + ".join(map(str, numbers))
    await interaction.response.send_message(f"{numbers_str} = {total}")

@math.command(name="sub", description="ひき算")
@app_commands.describe(num1="第一項", num2="第二項", num3="第三項（任意）", num4="第四項（任意）", num5="第五項（任意）")
async def math_sub(interaction: discord.Interaction, num1: int, num2: int, num3: int = None, num4: int = None, num5: int = None):
    numbers = [num1, -num2] + [-num for num in [num3, num4, num5] if num is not None]
    result = sum(numbers)
    numbers_str = " - ".join(map(str, [num1] + [num2, num3, num4, num5]))
    await interaction.response.send_message(f"{numbers_str} = {result}")

@math.command(name="mul", description="かけ算")
@app_commands.describe(num1="第一項", num2="第二項", num3="第三項（任意）", num4="第四項（任意）", num5="第五項（任意）")
async def math_mul(interaction: discord.Interaction, num1: int, num2: int, num3: int = None, num4: int = None, num5: int = None):
    numbers = [num1, num2] + [num for num in [num3, num4, num5] if num is not None]
    result = math.prod(numbers)
    numbers_str = " * ".join(map(str, numbers))
    await interaction.response.send_message(f"{numbers_str} = {result}")

@math.command(name="div", description="わり算")
@app_commands.describe(num1="被除数", num2="除数", num3="除数（任意）", num4="除数（任意）", num5="除数（任意）")
async def math_div(interaction: discord.Interaction, num1: int, num2: int, num3: int = None, num4: int = None, num5: int = None):
    if num2 == 0 or (num3 == 0 and num3 is not None) or (num4 == 0 and num4 is not None) or (num5 == 0 and num5 is not None):
        await interaction.response.send_message("0で割ることはできません。")
        return
    numbers = [num1, num2] + [num for num in [num3, num4, num5] if num is not None]
    result = numbers[0]
    for num in numbers[1:]:
        result /= num
    await interaction.response.send_message(f"{' / '.join(map(str, numbers))} = {result}")

@math.command(name="mod", description="剰余")
@app_commands.describe(x="被除数", y="除数", x3="除数（任意）", x4="除数（任意）", x5="除数（任意）")
async def math_mod(interaction: discord.Interaction, x: int, y: int, x3: int = None, x4: int = None, x5: int = None):
    if y == 0 or (x3 == 0 and x3 is not None) or (x4 == 0 and x4 is not None) or (x5 == 0 and x5 is not None):
        await interaction.response.send_message("0で割ることはできません。")
        return
    numbers = [x, y] + [num for num in [x3, x4, x5] if num is not None]
    result = numbers[0] % numbers[1]
    for num in numbers[2:]:
        result %= num
    numbers_str = " % ".join(map(str, numbers))
    await interaction.response.send_message(f"{numbers_str} = {result}")

@math.command(name="exp", description="累乗")
@app_commands.describe(mode="基数の種類（自然対数の底、または他の実数）", exponent="指数", base="基数（他の実数の場合）")
@app_commands.choices(mode=[
    app_commands.Choice(name='自然対数の底 e', value='e'),
    app_commands.Choice(name='他の実数', value='other')
])
async def math_exp(interaction: discord.Interaction, mode: str, exponent: int, base: float = None):
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

@math.command(name="log", description="対数")
@app_commands.describe(mode="対数の種類（自然対数、常用対数、二進対数）", value="対数を取る値")
@app_commands.choices(mode=[
    app_commands.Choice(name='自然対数', value='natural'),
    app_commands.Choice(name='常用対数', value='common'),
    app_commands.Choice(name='二進対数', value='binary')
])
async def math_log(interaction: discord.Interaction, mode: str, value: float):
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

@math.command(name="root", description="平方根または累乗根")
@app_commands.describe(mode="計算モード（平方根または累乗根）", value="根を取る値", radical="累乗根の次数")
@app_commands.choices(mode=[
    app_commands.Choice(name='平方根', value='sqrt'),
    app_commands.Choice(name='累乗根', value='nroot')
])
async def math_root(interaction: discord.Interaction, mode: str, value: float, radical: int = 2):
    if mode == 'sqrt':
        result = math.sqrt(value)
    elif mode == 'nroot':
        if radical <= 0:
            await interaction.response.send_message("根の次数は正の整数でなければなりません。")
            return
        result = value ** (1 / radical)
    else:
        await interaction.response.send_message("無効なモードが指定されました。")
    await interaction.response.send_message(f"{value} の {radical} 乗根 = {result}")

@math.command(name="sin", description="正弦(sin)・逆正弦(arcsin)")
@app_commands.describe(mode="モード（sin or arcsin）", value="角度（度数法）または値")
@app_commands.choices(mode=[
    app_commands.Choice(name='sin', value='sin'),
    app_commands.Choice(name='arcsin', value='arcsin')
])
async def math_sin(interaction: discord.Interaction, mode: str, value: float):
    if mode == 'sin':
        result = math.sin(math.radians(value))
    elif mode == 'arcsin':
        result = math.degrees(math.asin(value))
    else:
        await interaction.response.send_message("無効なモードが指定されました。")
    await interaction.response.send_message(f"{mode}({value}) = {result}")

@math.command(name="cos", description="余弦(cos)・逆余弦(arccos)")
@app_commands.describe(mode="モード（cos or arccos）", value="角度（度数法）または値")
@app_commands.choices(mode=[
    app_commands.Choice(name='cos', value='cos'),
    app_commands.Choice(name='arccos', value='arccos')
])
async def math_cos(interaction: discord.Interaction, mode: str, value: float):
    if mode == 'cos':
        result = math.cos(math.radians(value))
    elif mode == 'arccos':
        result = math.degrees(math.acos(value))
    else:
        await interaction.response.send_message("無効なモードが指定されました。")
    await interaction.response.send_message(f"{mode}({value}) = {result}")

@math.command(name="tan", description="正接(tan)・逆正接(arctan)")
@app_commands.describe(mode="モード（tan or arctan）", value="角度（度数法）または値")
@app_commands.choices(mode=[
    app_commands.Choice(name='tan', value='tan'),
    app_commands.Choice(name='arctan', value='arctan')
])
async def math_tan(interaction: discord.Interaction, mode: str, value: float):
    if mode == 'tan':
        result = math.tan(math.radians(value))
    elif mode == 'arctan':
        result = math.degrees(math.atan(value))
    else:
        await interaction.response.send_message("無効なモードが指定されました。")
    await interaction.response.send_message(f"{mode}({value}) = {result}")

@math.command(name="sigma", description="数列Σの計算")
@app_commands.describe(k="シグマの下限値", n="シグマの上限値", sequence="計算する数列の式（'k'を変数として使用）例:k、k*k、k+3など")
async def math_sigma(interaction: discord.Interaction, k: int, n: int, sequence: str):
    try:
        total = sum(eval(sequence.replace("k", str(i))) for i in range(k, n + 1))
        await interaction.response.send_message(f"Σ({sequence}) from {k} to {n} = {total}")
    except Exception as e:
        await interaction.response.send_message(f"式の計算中にエラーが発生しました: {e}")

# 最後に、グループをボットのコマンドツリーに追加
bot.tree.add_command(math)

#statsbotのcalcコマンドフォーマット変換
@bot.tree.command(name='convert-calc', description='Convert to calc command format')
@app_commands.describe(
    format="ゲームの形式を選択",
    team1='Team 1 members (comma-separated)',
    team2='Team 2 members (comma-separated)',
    team3='Team 3 members (comma-separated, optional)',
    team4='Team 4 members (comma-separated, optional)',
    team5='Team 5 members (comma-separated, optional)',
    team6='Team 6 members (comma-separated, optional)'
)
@app_commands.choices(format=[
    app_commands.Choice(name='2v2', value='2'),
    app_commands.Choice(name='3v3', value='3'),
    app_commands.Choice(name='4v4', value='4'),
    app_commands.Choice(name='6v6', value='6')
])
async def convert_calc(interaction: discord.Interaction, format: str, team1: str, team2: str, team3: str = '', team4: str = '', team5: str = '', team6: str = ''):
    teams = [team1, team2, team3, team4, team5, team6]
    teams = [team for team in teams if team]

    player_names = ', '.join([name for team in teams for name in team.split(', ')])
    command_str = f'^calc {format}, ' + player_names
    await interaction.response.send_message(command_str)

# 投票コマンド
def create_poll_embed(poll, author):
    embed = discord.Embed(title=poll['title'], description=poll['description'], color=0x00ff4c, timestamp=datetime.now())
    embed.set_footer(text=f"作成者: {author.display_name}", icon_url=author.avatar.url if author.avatar else None)
    for choice, voters in zip(poll['choices'], poll['votes']):
        embed.add_field(name=choice, value="\n".join(voters) if voters else "まだ投票がありません", inline=True)
    return embed

class PollButton(discord.ui.Button):
    def __init__(self, label, poll_id, choice_index, is_end_button=False):
        super().__init__(style=discord.ButtonStyle.primary if not is_end_button else discord.ButtonStyle.red, label=label)
        self.poll_id = poll_id
        self.choice_index = choice_index
        self.is_end_button = is_end_button

    async def callback(self, interaction: discord.Interaction):
        global polls
        poll = polls[self.poll_id]
        user = interaction.user.display_name

        if not poll['allow_duplicate']:
            for vote_set in poll['votes']:
                vote_set.discard(user)

        if not self.is_end_button:
            poll['votes'][self.choice_index].add(user)
            await interaction.response.edit_message(embed=create_poll_embed(poll, interaction.user), view=PollView(self.poll_id))

class PollView(discord.ui.View):
    def __init__(self, poll_id):
        super().__init__()
        self.poll_id = poll_id
        poll = polls[poll_id]
        for i, choice in enumerate(poll['choices']):
            self.add_item(PollButton(label=choice, poll_id=poll_id, choice_index=i))

        end_button = PollButton(label="終了", poll_id=poll_id, choice_index=-1, is_end_button=True)
        end_button.style = discord.ButtonStyle.red
        self.add_item(end_button)

    async def on_button_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        if button.is_end_button:
            poll = polls[self.poll_id]
            embed = create_poll_embed(poll, interaction.user)
            embed.title = f"投票が終了しました: {poll['title']}"
            embed.description = f"結果が確定しました。"

            for item in self.children:
                item.disabled = True

            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await super().on_button_click(interaction, button)

@bot.tree.command(name='poll', description='投票を作成する')
@app_commands.describe(
    title='タイトル',
    description='投票の詳細（任意）',
    allow_duplicate='投票の重複を許可するか（true or false）',
    choices='選択肢 (カンマ区切りで最大10個)'
)
async def poll(interaction: discord.Interaction, title: str, description: str, allow_duplicate: bool, choices: str):
    choices_list = choices.split(',')
    if len(choices_list) > 10:
        await interaction.response.send_message("選択肢は10個までです。")
        return

    poll_id = len(polls)
    poll = {
        'title': title,
        'description': description,
        'choices': choices_list,
        'votes': [set() for _ in choices_list],
        'allow_duplicate': allow_duplicate,
        'author': interaction.user
    }
    polls.append(poll)

    await interaction.response.send_message(embed=create_poll_embed(poll, interaction.user), view=PollView(poll_id))

polls = []


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