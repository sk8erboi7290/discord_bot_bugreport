import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot_commands.bug_report_command import register_bug_report_command

# ✅ .env 로드
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BUG_REPORT_CHANNEL_ID = int(os.getenv("BUG_REPORT_CHANNEL_ID"))

if not TOKEN or not BUG_REPORT_CHANNEL_ID:
    raise ValueError("❌ TOKEN 또는 BUG_REPORT_CHANNEL_ID 환경 변수가 누락되었습니다.")

# ✅ 인텐트 설정
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 완료: {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"✅ 슬래시 명령어 동기화 완료 ({len(synced)}개)")
    except Exception as e:
        print(f"❌ 슬래시 명령어 동기화 실패: {e}")

# ✅ 명령어 등록
register_bug_report_command(bot, BUG_REPORT_CHANNEL_ID)

# ✅ 실행
bot.run(TOKEN)
