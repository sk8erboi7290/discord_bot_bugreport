# 🐞 Discord Bug Report Bot (v1.0.1)

디스코드 서버에서 `/bug-report` 명령어를 통해 유저로부터 버그 리포트를 자동 수집하고,  
구글 시트에 자동으로 저장하는 슬래시 명령 기반 디스코드 봇입니다.

---

## 📌 주요 기능

- `/bug-report` 슬래시 명령어로 리포트 시작
- 이슈 유형 드롭다운 선택 → 모달 입력 폼 자동 표시
- Embed 형식으로 리포트 내용을 디스코드 채널에 출력
- 자동 스레드 생성 (공개 스레드 + 자동 archive 처리)
- 리포트 내용 구글 시트 연동 저장
- 메시지 링크도 구글 시트에 함께 기록
- 지정된 채널에서만 명령어 사용 가능 (채널 ID로 제한)
- 환경 변수(.env) 기반 설정

---

## 🗂️ 프로젝트 구조

```
discord_bug_bot/
├── main.py                     # 봇 실행 및 초기화
├── bot_commands/
│   └── bug_report_command.py   # 슬래시 명령어 핸들러
├── utils/
│   └── google_sheet.py         # 구글 시트 연동 모듈
├── requirements.txt            # 필요 라이브러리 목록
├── .env.example                # 환경 변수 예시 파일
└── secrets/
    └── (credentials.json 제외됨)
```

---

## ⚙️ 주요 기술 스택

- Python 3.10+
- discord.py 2.x
- gspread + Google API (서비스 계정 방식)
- Render, Replit, Railway 등 무료 배포 플랫폼 호환

---

## 🚀 사용법

1. `.env` 파일에 다음 항목 입력:

```
DISCORD_BOT_TOKEN=디스코드_봇_토큰
BUG_REPORT_CHANNEL_ID=버그_리포트_채널_ID
```

2. `secrets/credentials.json` 파일에 Google API 키 저장  
3. 봇 실행:

```bash
python main.py
```

---

## ☁️ 배포 팁

- Railway, Render 등 무료 호스팅 가능
- 슬래시 명령만 사용하는 경우 무료 플랜으로 충분

---

## 📝 버전 기록

- **v1.0.1**
  - 모듈화 구조 완성
  - 공개 스레드 + 자동 archive 처리
  - 메시지 링크 포함 저장
  - 구글 시트 연동 안정화

---

> 본 프로젝트는 실습 및 운영 자동화를 위해 제작된 슬래시 명령어 기반 디스코드 자동화 봇입니다.
