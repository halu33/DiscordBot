#ライブラリ
from typing import Optional, Union
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord import app_commands
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, View
import math
import math as math_module
import statistics
import random
import logging
import time
from datetime import datetime, timedelta
import os
import asyncio
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

#help_commands.py
from help_commands import commands_description, detailed_commands_description

#test 環境変数読み込み
load_dotenv()

#heroku 環境変数の読み込み
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

#botの設定
bot = commands.Bot(command_prefix="?", intents=intents, case_insensitive=True, help_command=None)

#スラッシュコマンド用のTreeを取得
tree = bot.tree



"""
********************************************************************************
コマンド処理
********************************************************************************
"""
#テストコマンド
@tree.command(name='test', description="テストコマンド")
@app_commands.describe(str="文字をここに打ってくださいね！")
async def test(interaction: discord.Interaction, str: str = None):
    if str:
        message = f"yo! {str}"
    else:
        message = "yoo!!"
    await interaction.response.send_message(message)

#挨拶コマンド
@tree.command(name='hello', description="社会不適合者による残念な挨拶")
async def hello(interaction: discord.Interaction):
    user_name = interaction.user.display_name
    await interaction.response.send_message(f"よお{user_name}")

#bot招待リンク
@bot.command(name='invite')
async def invite(ctx):
    await ctx.send(f'botの招待リンク:{INVITE}')

#bot開発用
@bot.command(name='dev')
async def dev_command(ctx):
    embed = discord.Embed(
        title="開発者用",
        description="いろんなURL",
        color=0x00ff4c
    )
    embed.add_field(name="__** Discord Developer Portal **__", value="https://discord.com/developers/applications", inline=False)
    embed.add_field(name="__** Discord.py 公式ドキュメント **__", value="https://discordpy.readthedocs.io/ja/latest/", inline=False)
    embed.add_field(name="__** このbotのリポジトリ **__", value="https://github.com/halu33/DiscordBot", inline=False)
    embed.add_field(name="__** heroku **__", value="https://dashboard.heroku.com/apps", inline=False)
    embed.add_field(name="__** embed builder **__", value="https://autocode.com/tools/discord/embed-builder/", inline=False)
    embed.add_field(name="__** Discord 文字装飾 **__", value="https://qiita.com/xero/items/6026ed007d5d34623a50", inline=False)
    embed.add_field(name="__** unixタイムスタンプ **__", value="https://hammertime.cyou/ja", inline=False)
    embed.add_field(name="__** 参考サイト **__", value=">>> bot作成 : https://zenn.dev/king/articles/4201f4ee821a27\nスラッシュコマンド実装 : https://zenn.dev/952490802574164/articles/b8b0232b29e79b", inline=False)
    embed.set_footer(text="@HALU_33", icon_url="https://halu33.net/img/epril_icon.png")
    await ctx.send(embed=embed)


"""
********************************************************************************
helpコマンド
********************************************************************************
"""
#help_commands.pyに定義されたコマンドの説明を取得
def get_command_description(command_name):
    return detailed_commands_description.get(command_name, "コマンドの説明が見つかりませんでした。")

#helpコマンド詳細のEmbedを作成
def create_detailed_help_embed(command_name):
    description = get_command_description(command_name)
    embed = discord.Embed(
        title=f"{command_name}コマンドの詳細",
        description=description,
        color=discord.Color.green()
    )
    embed.add_field(name="", value=f"`/{command_name}` とチャットで入力してみてください。", inline=False)
    embed.set_footer(text="@HALU_33", icon_url="https://halu33.net/img/epril_icon.png")
    return embed

#helpコマンド詳細を表示するボタン
async def detailed_help_button_callback(interaction: discord.Interaction, command_name: str):
    embed = create_detailed_help_embed(command_name)
    await interaction.response.send_message(embed=embed)

#helpコマンドの定義
@bot.tree.command(name='help', description="helpコマンド")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="helpコマンド",
        description="このbotのコマンド一覧と説明",
        color=discord.Color.green()
    )
    for command, description in commands_description.items():
        embed.add_field(name=command, value=description, inline=True)
    view = View()
    for cmd in commands_description.keys():
        button = Button(label=cmd, style=discord.ButtonStyle.primary)
        button.callback = lambda interaction, cmd=cmd: detailed_help_button_callback(interaction, cmd)
        view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view)


"""
********************************************************************************
支援値計算
********************************************************************************
"""
@bot.tree.command(name='sien', description="支援値の計算")
@app_commands.describe(total_power="編成の総合演技力", multiplier="リーダーのSAの倍率", sa="SAの回数")
async def sien(interaction: discord.Interaction, *, total_power: int, multiplier: float, sa: int):
    try:
        #支援値の計算式
        support_value = (total_power * multiplier * sa) / 2

        #計算結果をembedで出力
        embed = discord.Embed(
            type="rich",
            title="支援値の計算",
            description=f"総合力 {total_power} * 倍率 {multiplier} * SA回数 {sa} / 2 = **支援値：{support_value}**",
            color=0x00ff08,
            url="https://gamerch.com/world-dai-star/entry/841244"
        )

        #embedを送信
        await interaction.response.send_message(embed=embed)

    except (TypeError, ValueError):
        await interaction.response.send_message("引数に不正な値が含まれています。正しい値を入力してください。")


"""
********************************************************************************
pollコマンド
********************************************************************************
"""
@tree.command(name="poll", description="投票を作成します")
@app_commands.describe(
    title="投票のタイトル (必須)",
    allow_duplicate="重複投票を許可するか (True/False)",
    choice_list="選択肢 (半角カンマ区切り、最大19択まで)"
)
async def poll(
    interaction: discord.Interaction,
    title: str,
    allow_duplicate: bool,
    choice_list: str,
    description: str = ""
):
    try:
        # 選択肢の分割
        choices = choice_list.split(',')

        #選択肢の数が20以上の場合はエラーを返す
        if len(choices) > 19:
            await interaction.response.send_message("選択肢は19個以下にしてください")
            return

        #投票データの作成
        poll_data = create_poll_data(interaction, title, description, allow_duplicate, choices)
        embed = create_poll_embed(interaction, title, description, choices, poll_data["votes"], poll_data["voters"])
        if interaction.channel is None:
            logging.error("interaction.channel is None")
            return
        response = await interaction.response.send_message(f"{interaction.user.mention}が投票を作成しました")
        poll_message = await interaction.channel.send(embed=embed)

        #投票選択肢に対するリアクション追加
        for idx in range(len(choices)):
            await poll_message.add_reaction(chr(0x1F1E6 + idx))
        await poll_message.add_reaction("❌")
        poll_data["message_id"] = poll_message.id
        bot.active_polls[poll_message.id] = poll_data

    except Exception as e:
        logging.error(f"投票コマンドのエラー: {e}")
        raise e

#投票用embedを作成
def create_poll_embed(author_name, title, description, choices, votes, voters):
    embed = discord.Embed(title=title, description=description, color=0x00ff84)
    for idx, (choice, vote, voter) in enumerate(zip(choices, votes, voters)):
        voter_names = ', '.join([f'<@{v}>' for v in voter])
        embed.add_field(name=f"{chr(ord('A') + idx)}. {choice}", value=f"{vote} 票 ({voter_names})", inline=False)
    embed.set_footer(text=f"作成者: {author_name}")
    return embed

#投票データ作成
def create_poll_data(interaction, title, description, allow_duplicate, choices):
    return {
        "title": title,
        "description": description,
        "allow_duplicate": allow_duplicate,
        "choices": choices,
        "votes": [0] * len(choices),
        "voters": [set() for _ in choices],
        "channel_id": interaction.channel.id,
        "author_id": interaction.user.id
    }

bot.active_polls = {}

#投票結果のembed作成
def create_final_result_embed(poll_data, user):
    result = "\n".join(f"{choice}: {votes}" for choice, votes in zip(poll_data["choices"], poll_data["votes"]))
    return discord.Embed(title="投票結果", description=result, color=0x00ff00)

#投票結果の表示
def remove_previous_vote(poll_data, user):
    if not poll_data["allow_duplicate"]:
        for idx, voters in enumerate(poll_data["voters"]):
            if user.id in voters:
                voters.remove(user.id)
                poll_data["votes"][idx] -= 1

#新規投票の追加
def add_new_vote(poll_data, vote_idx, user):
    if user.id not in poll_data["voters"][vote_idx]:
        poll_data["voters"][vote_idx].add(user.id)
        poll_data["votes"][vote_idx] += 1

#投票の削除
def remove_vote(poll_data, vote_idx, user):
    if user.id in poll_data["voters"][vote_idx]:
        poll_data["votes"][vote_idx] -= 1
        poll_data["voters"][vote_idx].remove(user.id)

#リアクション追加時の処理
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.id not in bot.active_polls or user.bot:
        return

    poll_data = bot.active_polls[reaction.message.id]
    author_name = bot.get_user(poll_data["author_id"]).name

    #投票終了の処理
    if str(reaction.emoji) == "❌":
        if user.id == poll_data["author_id"]:
            del bot.active_polls[reaction.message.id]
            result_embed = create_final_result_embed(poll_data, user)
            await reaction.message.channel.send(embed=result_embed)
            await reaction.message.delete()
            return

    #投票の更新
    vote_idx = ord(str(reaction.emoji)) - 0x1F1E6
    if 0 <= vote_idx < len(poll_data["choices"]):
        if user.id in poll_data["voters"][vote_idx]:
            remove_vote(poll_data, vote_idx, user)
        else:
            remove_previous_vote(poll_data, user)
            add_new_vote(poll_data, vote_idx, user)

        embed = create_poll_embed(author_name, poll_data["title"], poll_data["description"], poll_data["choices"], poll_data["votes"], poll_data["voters"])
        await reaction.message.edit(embed=embed)

        await reaction.remove(user)

#投票結果のembed作成
def create_final_result_embed(poll_data, user):
    result = "\n".join(f"{choice}: {votes} 票 ({', '.join([f'<@{v}>' for v in voters])})" for choice, votes, voters in zip(poll_data["choices"], poll_data["votes"], poll_data["voters"]))
    return discord.Embed(title=f"投票結果: {poll_data['title']}", description=f"{poll_data['description']}\n\n{result}", color=0x0ff0000)


"""
********************************************************************************
挙手コマンド
********************************************************************************
"""
#状態管理（確定・仮・補欠）
class Recruitment:
    def __init__(self):
        self.confirmed = set()
        self.tentative = set()
        self.standby = set()

    def update_member_status(self, member, new_status):
        if new_status != 'c':
            self.confirmed.discard(member)
        if new_status != 'r':
            self.tentative.discard(member)
        if new_status != 's':
            self.standby.discard(member)

        if new_status == 'c':
            self.confirmed.add(member)
        elif new_status == 'r':
            self.tentative.add(member)
        elif new_status == 's':
            self.standby.add(member)

recruitment_status = {}

#挙手ボタン
class RecruitmentButton(discord.ui.Button):
    def __init__(self, label, custom_id):
        super().__init__(style=discord.ButtonStyle.primary, label=label, custom_id=custom_id)
    async def callback(self, interaction: discord.Interaction):
        global recruitment_status
        time = self.label
        user = interaction.user
        await interaction.response.defer(ephemeral=True)
        if time not in recruitment_status:
            recruitment_status[time] = Recruitment()
        recruitment = recruitment_status[time]
        action = ''
        if user in recruitment.confirmed or user in recruitment.tentative or user in recruitment.standby:
            recruitment.update_member_status(user, 'drop')
            action = '挙手取り下げ'
        else:
            recruitment.update_member_status(user, 'c')
            action = '挙手'
        role = await create_role_for_time(interaction.guild, time)
        if action == '挙手':
            await user.add_roles(role)
        elif action == '挙手取り下げ':
            await user.remove_roles(role)
        await update_recruitment_message(interaction.channel)

#募集状況メッセージの更新
async def update_recruitment_message(channel, target_member=None, action='', times=None):
    global recruitment_status
    embed = discord.Embed(title="募集状況", description="", color=0x00ff4c, timestamp=datetime.now())
    view = discord.ui.View()
    sorted_times = sorted(recruitment_status.keys(), key=lambda x: int(x))
    for time in sorted_times:
        recruitment = recruitment_status[time]
        confirmed_count = len(recruitment.confirmed)
        total_members = len(recruitment.confirmed) + len(recruitment.tentative) + len(recruitment.standby)
        max_members = 12 if confirmed_count >= 7 else 6
        remaining_slots = max(0, max_members - confirmed_count)
        remaining_including_tentative = max(0, max_members - total_members)
        confirmed_members = ">>> 確定：" + " ".join([f"<@{member.id}>" for member in recruitment.confirmed]) or "なし"
        tentative_members = "仮：" + " ".join([f"<@{member.id}>" for member in recruitment.tentative]) or "なし"
        standby_members = "補欠：" + " ".join([f"<@{member.id}>" for member in recruitment.standby]) or "なし"
        if max_members == 6:
            remaining_text = f"@{remaining_slots}"
        else:
            remaining_text_6 = max(0, 6 - confirmed_count)
            remaining_text = f"@{remaining_text_6}/@{remaining_slots}"
        if total_members > confirmed_count:
            remaining_text += f" ({remaining_including_tentative})"
        embed.add_field(name=f"__{time}時 {remaining_text}__", value=f"{confirmed_members}\n{tentative_members}\n{standby_members}", inline=False)
        view.add_item(RecruitmentButton(label=time, custom_id=f"recruit_{time}"))
    async for message in channel.history(limit=10):
        if message.embeds and message.author.id == bot.user.id:
            await message.delete()
            break
    await channel.send(embed=embed, view=view)

#最後のメッセージ取得
async def get_last_message(channel):
    async for message in channel.history(limit=1):
        return message
    return None

#ロール作成
async def create_role_for_time(guild, time):
    """指定された時間に対応するロールを作成または取得"""
    role_name = str(time)
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        role = await guild.create_role(name=role_name)
    return role

#ロール削除
async def delete_role_for_time(guild, time):
    """指定された時間のロールを削除"""
    role_name = str(time)
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        await role.delete()

#コマンド
kyosyu = app_commands.Group(name="kyosyu", description="挙手コマンド")

#can
@kyosyu.command(name='can', description='メンバーを募集or挙手をする')
@app_commands.choices(type=[
    app_commands.Choice(name='確定', value='c'),
    app_commands.Choice(name='仮', value='r'),
    app_commands.Choice(name='補欠', value='s')
])
async def can(interaction: discord.Interaction, time: str, type: str = 'c', member: discord.Member = None):
    await interaction.response.send_message(f"<@{interaction.user.id}>が挙手しました")
    target_member = member or interaction.user
    new_times = time.split()
    sorted_times = sorted(set(new_times), key=lambda x: int(x))
    times_str = " ".join(sorted_times)
    roles = await asyncio.gather(*[create_role_for_time(interaction.guild, t) for t in sorted_times])
    await asyncio.gather(*[update_member_and_assign_role(interaction, t, target_member, type) for t in sorted_times])
    await update_recruitment_message(interaction.channel)
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(f"<@{target_member.id}>が{times_str}時に挙手しました。", ephemeral=True)
async def update_member_and_assign_role(interaction, time, member, type):
    if time not in recruitment_status:
        recruitment_status[time] = Recruitment()
    recruitment_status[time].update_member_status(member, type)
    role = await create_role_for_time(interaction.guild, time)
    await member.add_roles(role)

#drop
@kyosyu.command(name='drop', description='挙手を取り下げる')
async def drop(interaction: discord.Interaction, time: str, member: discord.Member = None):
    target_member = member or interaction.user
    new_times = time.split()
    sorted_times = sorted(set(new_times), key=lambda x: int(x))
    times_str = " ".join(sorted_times)
    for t in sorted_times:
        if t in recruitment_status:
            recruitment = recruitment_status[t]
            recruitment.update_member_status(target_member, 'drop')
            role = discord.utils.get(interaction.guild.roles, name=str(t))
            if role:
                await target_member.remove_roles(role)
            else:
                print(f"Role {t} not found for removal.")
    await update_recruitment_message(interaction.channel)
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(f"<@{target_member.id}>が{times_str}時の挙手を取り下げました。")


#now
@kyosyu.command(name='now', description='現在の募集状況を表示する')
async def now(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    if not recruitment_status:
        await interaction.followup.send("現在の募集はありません。")
    else:
        await interaction.followup.send("現在の募集状況を表示")
        await update_recruitment_message(interaction.channel)

#clear
@kyosyu.command(name='clear', description='募集状況をリセットする')
async def clear(interaction: discord.Interaction):
    global recruitment_status
    for time in list(recruitment_status.keys()):
        await delete_role_for_time(interaction.guild, time)
    recruitment_status.clear()
    await interaction.response.send_message("募集状況をリセットしました。")

#グループをbotのコマンドツリーに追加
bot.tree.add_command(kyosyu)


"""
********************************************************************************
対話しようぜ
********************************************************************************
"""
#初期状態 False
learning_mode_active = False
chat_mode_active = False
active_chat_channel_id = None
active_learning_channel_id = None

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

#DB接続
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_DATABASE
        )
        print("MySQL Database connection successful")
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")
    return connection

#DBからメッセージをランダムで選択
def get_random_response():
    connection = create_db_connection()
    response = None
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT content FROM chats ORDER BY RAND() LIMIT 1")
            result = cursor.fetchone()
            if result:
                response = result[0].replace("\\n", "\n")
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            cursor.close()
            connection.close()
    return response

#指定したインデックスの行を編集
def edit_learning_content(index, new_text):
    new_text = new_text.replace("\n", "\\n")
    connection = create_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE chats SET content = %s WHERE id = %s", (new_text, index))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"編集中にエラーが発生しました: {err}")
        finally:
            cursor.close()
            connection.close()

#指定したインデックスの行を削除
def delete_learning_content(index):
    connection = create_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM chats WHERE id = %s", (index,))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"削除中にエラーが発生しました: {err}")
        finally:
            cursor.close()
            connection.close()

#DBからテーブル全体を取得
def list_learning_content():
    connection = create_db_connection()
    responses_str = ""
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, content FROM chats")
            results = cursor.fetchall()
            responses_str = "\n".join(["{}: {}".format(id, content.replace('\\n', '\n')) for id, content in results])
        except mysql.connector.Error as err:
            print(f"リスト取得中にエラーが発生しました: {err}")
        finally:
            cursor.close()
            connection.close()
    return responses_str

#コマンド
@bot.tree.command(name='chat', description='対話モードの開始・終了')
@app_commands.describe(mode='play または end')
@app_commands.choices(mode=[
    app_commands.Choice(name='play', value='play'),
    app_commands.Choice(name='end', value='end')
])
async def chat(interaction: discord.Interaction, mode: str):
    global chat_mode_active, active_chat_channel_id
    if mode == 'play':
        chat_mode_active = True
        active_chat_channel_id = interaction.channel_id
        await interaction.response.send_message("よおお社不ども")
    elif mode == 'end':
        chat_mode_active = False
        await interaction.response.send_message("ばいばーい！！カス！！！")
    else:
        await interaction.response.send_message("そんなコマンドないよwwwwwwwwwwwwwwww")

@bot.tree.command(name='learning', description='学習モードの開始・終了・学習内容の表示')
@app_commands.describe(mode='start, end, list, edit, delete', index='編集or削除する行の番号', new_text='edit:新しいテキスト')
@app_commands.choices(mode=[
    app_commands.Choice(name='start', value='start'),
    app_commands.Choice(name='end', value='end'),
    app_commands.Choice(name='list', value='list'),
    app_commands.Choice(name='edit', value='edit'),
    app_commands.Choice(name='delete', value='delete')
])
async def learning(interaction: discord.Interaction, mode: str, index: int = None, new_text: str = None):
    global learning_mode_active, active_learning_channel_id
    if mode == 'start':
        learning_mode_active = True
        active_learning_channel_id = interaction.channel_id
        await interaction.response.send_message("勉強タイム開始")
    elif mode == 'end':
        learning_mode_active = False
        active_learning_channel_id = None
        await interaction.response.send_message("勉強タイム終了")
    elif mode == 'list':
        responses_str = list_learning_content()
        if responses_str:
            await interaction.response.send_message(f"__**現在の学習内容:**__\n{responses_str}")
        else:
            await interaction.response.send_message("ノー勉状態です、知能指数0wwwwwwww")
    elif mode == 'edit':
        if index is not None and new_text is not None:
            edit_learning_content(index, new_text)
            await interaction.response.send_message(f"{index}番の記憶を改変したぜ")
        else:
            await interaction.response.send_message("は？？？？？どれだよwwwwwwwwwwww")
    elif mode == 'delete':
        if index is not None:
            delete_learning_content(index)
            await interaction.response.send_message(f"{index}番の記憶をなかったことにしたぜ")
        else:
            await interaction.response.send_message("は？？？？？どれだよwwwwwwwwwwww")
    else:
        await interaction.response.send_message("そんなコマンドないよwwwwwwwwwwwwwwww")

#メッセージ応答と学習
@bot.event
async def on_message(message):
    global chat_mode_active, learning_mode_active, active_chat_channel_id, active_learning_channel_id
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        response = get_random_response()
        if response:
            await message.channel.send(response)
    if not (message.channel.id == active_chat_channel_id or message.channel.id == active_learning_channel_id):
        return
    if learning_mode_active and message.channel.id == active_learning_channel_id:
        connection = create_db_connection()
        if connection is not None:
            try:
                content = message.content.replace("\n", "\\n")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO chats (content) VALUES (%s)", (content,))
                connection.commit()
            except mysql.connector.Error as err:
                print(f"学習モードの処理中にエラーが発生しました: {err}")
            finally:
                cursor.close()
                connection.close()
        await message.channel.send(message.content.replace("\\n", "\n"))
    elif chat_mode_active and message.channel.id == active_chat_channel_id:
        response = get_random_response()
        if response:
            await message.channel.send(response)
    await bot.process_commands(message)


"""
********************************************************************************
bot起動時の処理
********************************************************************************
"""
@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{guild_count} servers"))
    logging.info(f'Logged in : {bot.user}')
    await tree.sync()
    await tree.sync(guild=discord.Object(id=GUILD_ID))

#ロール処理
README_CHANNEL_ID = os.getenv('README_CHANNEL_ID')
MEMBER_ROLE_ID = os.getenv('MEMBER_ROLE_ID')
TEMP_ROLE_ID = os.getenv('TEMP_ROLE_ID')
INFO_CHANNEL_ID = os.getenv('INFO_CHANNEL_ID')

@bot.command(name='autorole', help='READMEチャンネルにメッセージを設定します。')
@commands.has_permissions(administrator=True)
async def setup_readme_channel(ctx):
    channel = bot.get_channel(int(README_CHANNEL_ID))
    embed = discord.Embed(title="README", description=f"**<#{INFO_CHANNEL_ID}>チャンネルのルールを読んだら、このメッセージにリアクションしてください。**", color=0x00ff4c)
    embed.set_footer(text="@HALU_33", icon_url="https://halu33.net/img/epril_icon.png")
    message = await channel.send(embed=embed)
    await message.add_reaction('✅')

@bot.event
async def on_member_join(member):
    try:
        temp_role = member.guild.get_role(int(TEMP_ROLE_ID))
        if temp_role:
            await member.add_roles(temp_role)
            #print(f"{member}にtempロールが付与")
    except Exception as e:
        print(f'新しいメンバーへのロール付与中にエラーが発生しました: {e}')

@bot.event
async def on_raw_reaction_add(payload):
    try:
        if payload.channel_id == int(README_CHANNEL_ID) and str(payload.emoji) == '✅':
            guild = bot.get_guild(int(GUILD_ID))
            member = guild.get_member(payload.user_id)
            temp_role_id = int(TEMP_ROLE_ID)
            member_role_id = int(MEMBER_ROLE_ID)
            if temp_role_id in [role.id for role in member.roles]:
                temp_role = guild.get_role(temp_role_id)
                member_role = guild.get_role(member_role_id)
                await member.remove_roles(temp_role)
                await member.add_roles(member_role)
                #print(f"メンバーロールが{member}に付与、Tempロール削除")
    except Exception as e:
        print(f'リアクションによるロール処理中にエラーが発生しました: {e}')


#ワードに反応してメンション
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    developer_trigger_words = ['はる', 'halu', 'HALU_33']
    special_response_words = {
        'ゆうんぬ': 'んぬ～><',
        'んぬ': 'んぬ～><'
    }
    response_sent = False
    if any(word in message.content for word in developer_trigger_words):
        user_id = os.getenv('HALU_33_USER_ID')
        mention = f'<@{user_id}>'
        await message.channel.send(f'{mention}')
        response_sent = True
    for trigger_word, response in special_response_words.items():
        if trigger_word in message.content:
            await message.channel.send(response)
            response_sent = True
            break
    if not response_sent:
        await bot.process_commands(message)


"""
********************************************************************************
エラーハンドリングとログ記録
********************************************************************************
"""
@bot.event
async def on_command_completion(ctx):
    logging.info(f'コマンド実行: {ctx.command} by {ctx.author}')


"""
********************************************************************************
bot起動
********************************************************************************
"""
bot.run(TOKEN)