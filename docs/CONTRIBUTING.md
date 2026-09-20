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

---

# 🎬 체험 샘플 작성 규칙 (skills/nxt-demo/samples/<name>/)

스킬 하나마다 샘플 폴더 하나가 필수입니다(`lint-skills.sh`가 검사). 입력 파일 1~3개와 `README.md`를 둡니다.

## README.md 형식 (고정 — 핸즈온 생성기가 이 형식을 읽습니다)
```
# /<name> 체험 — <제목>
**이 샘플로 해 볼 수 있는 것**: 한두 문장

**내용**:
- 불릿 딱 5개. 무엇을 다루는 자료인지 / 핵심 항목 3개(숫자 포함) / 정해지지 않은 것
**파일**: 파일명 — 설명        (파일마다 한 줄)
**이렇게 시작하세요**
```
/<name> <상황 한 줄>. 아래 자료를 붙여 넣습니다.
```
(어떤 파일을 붙여 넣는지 한 줄)
**기대 결과**: 산출물 설명 3줄 이내
```

## 원칙
- 전부 가상 데이터: 한빛대학교, (주)가온테크, 가상 인물. 입력 .md 첫 줄에 `# [샘플] 가상 데이터 — 체험용`. 연락처는 010-0000-0000·example.com만.
- 일부러 함정을 넣습니다(담당 미정, 개인정보 섞인 문의, 미달 지표, 부풀리고 싶은 경험). 스킬이 이를 처리하는 모습이 체험의 핵심입니다.
- 텍스트 40~120줄, CSV 15~40행. 파일명은 영문 kebab-case.
- 샘플을 바꾸면 `python3 scripts/build-handson.py`와 `python3 scripts/build-guide.py`를 다시 실행합니다.
