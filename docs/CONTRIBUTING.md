# ✍️ 에이전트 작성 규칙

## 파일 위치와 이름
- `<디비전>/<디비전>-<slug>.md` (예: `admin/admin-meeting-minutes.md`)
- 디비전은 `divisions.json`에 정의된 것만 사용합니다.

## 프론트매터 (순서 고정)
```yaml
---
name: meeting-minutes          # kebab-case ASCII. Claude Code 호출 식별자. 레포 전체에서 유일
title: 회의록 정리원             # 한글 표시명
description: 무엇을 하는지 + 언제 쓰는지. 한글 1~2문장. Claude Code가 자동 위임 판단에 사용
color: "#F59E0B"
emoji: 📋
vibe: 한 줄 성격 문구
audience: [행정직원, 사업단]     # 학생 · 대학원생 · 교수·연구자 · 사업단 · 행정직원 · 공공기관 중 선택
source: project-management/project-management-meeting-notes-specialist.md   # 원본 경로. 새로 만든 경우 "original"
---
```

## 본문 섹션 (제목 고정)
```
# {이모지} {title}
(한 문단 정체성 소개)
## 🧠 정체성과 기억
## 🎯 핵심 임무
## 🚨 반드시 지킬 규칙
## 📋 산출물
## 🔄 작업 절차
## 💭 소통 방식
## 🎯 성공 기준
## 💬 이렇게 요청하세요      ← 복사해 쓸 수 있는 예시 요청 3개
> 원본: agency-agents `{source}` (MIT) — nxt-agency에서 한국 대학·공공 환경에 맞게 재구성
```

## 원칙
- **전부 한글.** 고유명사·기술 용어·코드만 영어를 남깁니다.
- **한국 맥락.** 법령·기관·서식·용어는 한국 것으로. 조항 번호처럼 확실하지 않은 사실은 쓰지 않습니다.
- **250줄 이내.** 길면 쓰기 어렵습니다. 핵심 규칙과 산출물 템플릿을 남기고 줄입니다.
- **개인정보 보호.** 예시에 실명·학번·연락처를 넣지 않습니다.

## 검사
```bash
./scripts/lint-agents.sh                 # 전체
./scripts/lint-agents.sh admin/admin-*.md
```

---

# 🧑‍💼 직업군 스킬 작성 규칙

## 파일 위치
- `skills/<name>/SKILL.md` — 디렉터리명과 `name`이 같아야 합니다(소문자·숫자·하이픈).

## 프론트매터 — 이 키만 (claude.ai 업로드 제한)
```yaml
---
name: meeting-minutes
description: 무엇을 어떤 순서로 하는지 + 어떤 말이 나오면 쓰는지(트리거 단어). 한글 300자 이내.
license: MIT
compatibility: Claude Code, claude.ai, Kiro
metadata:
  title: 회의록 작성
  role: 행정                      # 사업단 | 행정 | 교수·연구자 | 학생
  agents: [meeting-minutes, document-generator]   # 사용하는 전문가 name
---
```

## 본문 섹션 (제목 고정, 150줄 이내)
```
# {이모지} {title}
## 시작할 때 물어볼 것        최대 3개, 기본값 명시
## 진행 단계                  3~5단계. 각 단계: 전문가 / 위임 규칙 / 요령 / 산출물 / 다음 단계로 넘길 것
## 최종 산출물
## 하지 말 것
## 이렇게 시작하세요          `/name …` 예시 3개
> nxt-agency 직업군 스킬 · 사용하는 전문가: …
```

## 원칙
- **혼자서도 동작.** claude.ai·Kiro에는 우리 전문가가 없을 수 있으니 각 단계에 "전문가가 있으면 위임, 없으면 아래 요령대로"를 쓰고 핵심 규칙·서식을 요약해 넣습니다.
- **초보자 톤.** 용어는 풀어 쓰고, 단계마다 "여기까지 확인할까요?"를 한 번만 묻습니다.
- 검사: `./scripts/lint-skills.sh`
