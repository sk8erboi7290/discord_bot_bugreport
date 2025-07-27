# bot_commands/bug_report_command.py

import discord
from discord import app_commands
from discord.ui import View, Select, Modal, TextInput
from utils.google_sheet import append_to_sheet

ISSUE_OPTIONS = [
    ("UI/UX 문제", "화면, 버튼, 인터페이스 문제"),
    ("기능 오류", "작동 안함, 잘못 작동 등"),
    ("텍스트/번역 오류", "오탈자, 번역 문제"),
    ("밸런스 이슈", "게임 내 수치 밸런스 관련"),
    ("기타", "그 외 기타 버그"),
]

class BugTypeSelect(Select):
    def __init__(self, channel_id):
        options = [
            discord.SelectOption(label=label, description=desc)
            for label, desc in ISSUE_OPTIONS
        ]
        super().__init__(placeholder="👇 신고할 문제 유형을 선택해주세요", options=options, min_values=1, max_values=1)
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.channel.id != self.channel_id:
            await interaction.response.send_message(
                f"이 명령어는 <#{self.channel_id}> 채널에서만 사용 가능합니다.",
                ephemeral=True
            )
            return

        selected_type = self.values[0]
        await interaction.response.send_modal(BugReportModal(selected_type, self.channel_id))


class BugReportModal(Modal):
    def __init__(self, issue_type, channel_id):
        super().__init__(title=f"🔧 버그 리포트 - {issue_type}")
        self.issue_type = issue_type
        self.channel_id = channel_id

        self.summary = TextInput(label="문제 요약", placeholder="예: 버튼 눌러도 반응 없음", required=True)
        self.occurred_at = TextInput(label="발생 날짜 및 시간", placeholder="예: 2025.07.01 14:30", required=True)
        self.device = TextInput(label="사용 기기 및 OS 버전", placeholder="예: 갤럭시 S21 / Android 13", required=True)
        self.server_info = TextInput(label="서버명 또는 국가", placeholder="예: 한국 / 일본 / 글로벌", required=True)
        self.details = TextInput(label="버그 사항 세부 내용", style=discord.TextStyle.paragraph, required=True)

        self.add_item(self.summary)
        self.add_item(self.occurred_at)
        self.add_item(self.device)
        self.add_item(self.server_info)
        self.add_item(self.details)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message("✅ 리포트가 제출되었습니다!", ephemeral=True)

            embed = discord.Embed(
                title=f"🔧 버그 리포트 - {self.issue_type}",
                color=discord.Color.red()
            )
            embed.add_field(name="문제 요약", value=self.summary.value, inline=False)
            embed.add_field(name="발생 날짜 및 시간", value=self.occurred_at.value, inline=False)
            embed.add_field(name="사용 기기 및 OS 버전", value=self.device.value, inline=False)
            embed.add_field(name="서버명 또는 국가", value=self.server_info.value, inline=False)
            embed.add_field(name="버그 사항 세부 내용", value=self.details.value, inline=False)

            channel = interaction.guild.get_channel(self.channel_id)
            if not channel:
                await interaction.followup.send("❌ 리포트 채널을 찾을 수 없습니다.", ephemeral=True)
                return

            message = await channel.send(embed=embed)

            # 🧵 공개 스레드 생성 + 즉시 접힘
            thread = await message.create_thread(
                name=f"{interaction.user.display_name}의 첨부자료",
                auto_archive_duration=60  # 1시간 이후 자동 아카이브
            )
            await thread.edit(archived=True)  # 즉시 접힘 상태로 설정
            await thread.send("📌 첨부파일이나 추가 정보는 이 메시지에 답글로 달아주세요.")

            message_link = f"https://discord.com/channels/{channel.guild.id}/{channel.id}/{message.id}"

            append_to_sheet({
                "문제 유형": self.issue_type,
                "문제 요약": self.summary.value,
                "발생 시점": self.occurred_at.value,
                "사용 기기": self.device.value,
                "서버 및 국가": self.server_info.value,
                "버그 세부 사항": self.details.value,
                "본문 링크": message_link,
            })

            print("✅ 구글 시트 저장 완료")

        except Exception as e:
            print(f"❌ 후속 처리 실패: {e}")


class BugReportView(View):
    def __init__(self, channel_id):
        super().__init__(timeout=None)
        self.add_item(BugTypeSelect(channel_id))


def register_bug_report_command(bot, channel_id):
    @bot.tree.command(name="bug-report", description="버그 리포트를 제출합니다.")
    async def bug_report(interaction: discord.Interaction):
        if interaction.channel.id != channel_id:
            await interaction.response.send_message(
                f"이 명령어는 <#{channel_id}> 채널에서만 사용 가능합니다.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "🔧 버그 신고 - 이슈 유형 선택\n다음 중 신고할 문제 유형을 선택해주세요.",
            view=BugReportView(channel_id),
            ephemeral=True
        )
