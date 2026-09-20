# 🏫 nxt-agency — 대학·공공기관을 위한 AI 업무 도우미

> 대학생 · 교수 · 사업단 · 행정직원 · 공공기관 담당자가 **명령 하나로 업무 하나를 끝내는** 한국어 AI 워크플로우.
> Claude Code, Codex, AWS Kiro에 한 줄로 설치됩니다. Agent Skills 표준을 따르는 다른 도구(claude.ai 웹 등)에도 쓸 수 있습니다.
> [agency-agents](https://github.com/msitarzewski/agency-agents)(MIT)에서 필요한 전문가만 골라 한국어로 옮기고, 그 위에 직업군별 워크플로우를 얹었습니다.

---

## ⚡ 3분 시작

```bash
git clone https://github.com/nxtcloud-edu/nxt-agency.git
cd nxt-agency
./scripts/install.sh          # 설치된 도구(Claude Code, Codex, Kiro)를 찾아서 전부 설치
```

그다음 슬래시 명령을 치면 됩니다. 필요한 것 두세 가지만 물어보고 알아서 진행합니다.

```
/meeting-minutes          ← 녹취록을 붙여 넣으면 회의록으로
/business-plan            ← 사업계획서 초안을 단계별로
/cover-letter             ← 채용공고와 내 경험으로 자기소개서
```

**처음이라 뭘 넣어야 할지 모르겠다면** 샘플로 먼저 체험해 보세요. 자기 자료 없이 가상 데이터로 명령을 끝까지 돌려 결과를 보여 줍니다.

```
/nxt-demo
```

무엇을 써야 할지 모르겠으면 안내 데스크에게 물어보세요.

```
안내 데스크, 나는 사업단 행정 담당인데 연차평가 성과보고서를 처음 써야 해. 어디부터 시작하면 돼?
```

---

> 📖 그림과 함께 보는 안내서: [docs/guide.html](docs/guide.html) — 설치부터 데모 핸즈온까지. 초보 사용자에게 이 파일 하나만 보내도 됩니다.
> 🧪 직업군별 핸즈온 시나리오: [사업단](docs/handson/project.html) · [행정](docs/handson/admin.html) · [교수·연구자](docs/handson/research.html) · [학생](docs/handson/student.html) — 페르소나 상황에 따라 명령 3~4개를 순서대로 실습

## 🧑‍💼 직업군별 워크플로우 (스킬)

한 명령이 여러 전문가를 순서대로 부릅니다. 초보자는 이것만 알면 됩니다.

### 🎯 사업단 (LINC 3.0 · RIS · BK21 · 글로컬 등)

| 명령 | 하는 일 | 순서 |
|---|---|---|
| [`/business-plan`](skills/business-plan/SKILL.md) | 사업계획서 작성 | 동향 조사 → 계획서 → 예산표 → 규정 점검 → 1페이지 요약 |
| [`/performance-report`](skills/performance-report/SKILL.md) | 성과보고서 작성 | KPI 달성률 → 만족도·정성 성과 → 개조식 요약 → DOCX/PPTX |
| [`/event-prep`](skills/event-prep/SKILL.md) | 행사 준비 | 일정표 → 공고문·카드뉴스 → 보도자료 → 결과 회의록 |
| [`/budget-check`](skills/budget-check/SKILL.md) | 예산 집행 점검 | 세목별 집행률 → 부정 집행 위험 점검 → 보고 요약 |

### 🗂️ 행정직원 · 공공기관

| 명령 | 하는 일 | 순서 |
|---|---|---|
| [`/meeting-minutes`](skills/meeting-minutes/SKILL.md) | 회의록 작성 | 빠진 정보 확인 → 회의록 서식 → DOCX |
| [`/report-summary`](skills/report-summary/SKILL.md) | 보고 요약 | 보고 대상 확인 → 1페이지 개조식 → 결재용 DOCX |
| [`/inquiry-reply`](skills/inquiry-reply/SKILL.md) | 민원·문의 답변 | 분류·이관 판단 → 답변 초안 → 규정·개인정보 점검 |
| [`/consent-form`](skills/consent-form/SKILL.md) | 개인정보 동의서 | 항목 최소화 → 동의서 초안 → 규정 점검 → DOCX |

### 🎓 교수 · 연구자

| 명령 | 하는 일 | 순서 |
|---|---|---|
| [`/literature-review`](skills/literature-review/SKILL.md) | 선행연구 정리 | 범위 확정 → 정리표(근거 수준) → 연구 공백 |
| [`/research-proposal`](skills/research-proposal/SKILL.md) | 연구계획서 작성 | 공고 분석 → 필요성 근거 → 계획서 → 예산 |
| [`/syllabus`](skills/syllabus/SKILL.md) | 강의계획서 작성 | 학습성과 → 주차별 계획 → 평가·CQI |

### 📚 학생

| 명령 | 하는 일 | 순서 |
|---|---|---|
| [`/cover-letter`](skills/cover-letter/SKILL.md) | 자기소개서 작성 | 공고·경험 확인 → 항목별 초안 → 다듬기·이력서 |
| [`/semester-plan`](skills/semester-plan/SKILL.md) | 학기 계획 | 목표·제약 → 주간 계획·습관 → 중간 점검 |
| [`/capstone`](skills/capstone/SKILL.md) | 캡스톤 프로젝트 | 범위 축소 → 시제품 → 구조 정리 → 코드 리뷰 |

### 🎬 체험 (항상 함께 설치)

| 명령 | 하는 일 |
|---|---|
| [`/nxt-demo`](skills/nxt-demo/SKILL.md) | 샘플 데이터로 위 명령들을 체험. 명령마다 가상 데이터(녹취록, KPI 실적표, 공고문, 문의 목록 등)가 [`skills/nxt-demo/samples/`](skills/nxt-demo/samples/)에 들어 있고, 고른 샘플로 실제 명령을 끝까지 실행해 결과를 보여 줍니다 |

---

## 👥 전문가 에이전트 (27명)

스킬이 부품으로 쓰는 전문가들입니다. 익숙해지면 이름으로 직접 부를 수 있습니다: `"통계·연구설계 전문가로 이 설문 결과의 분석 방법을 골라줘"`

| 디비전 | 전문가 (`name`) |
|---|---|
| 🧭 안내 | 안내 데스크 (`nxt-guide`) |
| 🎓 연구 | 문헌조사 전문가 (`literature-reviewer`) · 통계·연구설계 전문가 (`statistician`) · 연구과제·사업 제안서 작성가 (`proposal-writer`) · 연구·산업 동향 조사원 (`trend-researcher`) |
| 📚 교육·진로 | 교육과정 설계자 (`course-designer`) · 학습·진로 멘토 (`study-career-mentor`) · 자기소개서·이력서 코치 (`resume-coach`) · 유학·교환학생 상담가 (`study-abroad-advisor`) |
| 🗂️ 행정 | 회의록 정리원 (`meeting-minutes`) · 보고서 요약가 (`report-summarizer`) · 문서 생성기 (`document-generator`) · 규정·법령 검토관 (`compliance-checker`) · 개인정보보호 담당관 (`privacy-officer`) · 업무 프로세스 개선가 (`process-improver`) · 민원·문의 응대원 (`inquiry-responder`) |
| 🎯 사업단 | 사업 관리자 (`program-manager`) · 성과 분석가 (`performance-analyst`) · 설문·의견 분석가 (`survey-analyst`) · 홍보·보도자료 담당 (`pr-manager`) · 홍보 콘텐츠 제작자 (`content-creator`) · 예산·집행 관리자 (`budget-manager`) |
| 💻 개발 | 빠른 시제품 개발자 (`rapid-prototyper`) · 프론트엔드 개발자 (`frontend-developer`) · 백엔드 설계자 (`backend-architect`) · 코드 리뷰어 (`code-reviewer`) · AI 엔지니어 (`ai-engineer`) |

각 파일 끝에 **이렇게 요청하세요** 예시 3개가 있습니다. 전체 목록과 설명은 [docs/agents.md](docs/agents.md).

---

## 🛠️ 설치

### Claude Code

```bash
./scripts/install.sh --tool claude-code            # ~/.claude/agents, ~/.claude/skills
./scripts/install.sh --tool claude-code --project  # 현재 프로젝트 .claude/ 에
```

### Codex

에이전트는 Codex 커스텀 에이전트 TOML로 변환되어 `~/.codex/agents/`에, 스킬은 `~/.codex/skills/`에 들어갑니다.

```bash
./scripts/install.sh --tool codex
```

Codex에서는 `$meeting-minutes` 또는 `/skills`로 스킬을 부릅니다. 전문가를 서브에이전트로 쓰려면 Codex 설정에서 멀티에이전트(`agents.enabled`)를 켜야 합니다.

### AWS Kiro (IDE · CLI 공통)

회사에서 Kiro 계정을 받은 경우. 에이전트는 Kiro 커스텀 에이전트 형식으로 변환되어 들어가고, 스킬은 그대로 복사됩니다.

```bash
./scripts/install.sh --tool kiro                   # ~/.kiro/agents, ~/.kiro/skills
```

Kiro에서도 `/meeting-minutes` 처럼 스킬을 부르고, 에이전트는 `/agent` 로 전환합니다.

### Claude Code 플러그인으로 설치 (마켓플레이스)

레포를 clone하지 않고 Claude Code 안에서 바로 설치·업데이트하는 방법입니다. 명령과 전문가 이름 앞에 `nxt-agency:` 접두어가 붙습니다.

```
/plugin marketplace add nxtcloud-edu/nxt-agency
/plugin install nxt-agency@nxt-agency
```

그 다음 `/nxt-agency:nxt-demo`처럼 부르거나, 그냥 "회의록 만들어줘"라고 말하면 됩니다. 설치 스크립트 방식과 플러그인 방식을 같이 쓰면 이름이 두 벌 생기니 한쪽만 쓰세요.

### 그 밖의 도구

스킬은 Agent Skills 표준(SKILL.md)이라 이를 지원하는 다른 도구에서도 쓸 수 있습니다. 예를 들어 claude.ai 웹은 zip 업로드로, 다른 CLI는 스킬 폴더 복사로 됩니다. 스킬은 전문가 없이도 혼자 동작하도록 만들어져 있습니다.

```bash
./scripts/package-skills.sh          # dist/skills/<name>.zip 생성
```

### 필요한 것만

```bash
./scripts/install.sh --role admin                 # 행정 스킬 4개 + 그 스킬이 쓰는 전문가
./scripts/install.sh --skill meeting-minutes      # 스킬 하나 + 필요한 전문가
./scripts/install.sh --division research          # 연구 전문가만
./scripts/install.sh --list                       # 전체 목록
./scripts/install.sh --dry-run                    # 설치하지 않고 대상만 보기
./scripts/install.sh --uninstall                  # 이 레포에서 설치한 것만 제거
```

직업군은 네 가지이며 `--role`에는 영문 별칭을 쓰면 됩니다.

| `--role` | 대상 | 한글 값 |
|---|---|---|
| `project` | 사업단 | 사업단 |
| `admin` | 행정직원·공공기관 | 행정 |
| `research` | 교수·연구자·대학원생 | 교수·연구자 |
| `student` | 학생 | 학생 |

---

## 📁 파일 구조

```
nxt-agency/
├── skills/<name>/SKILL.md   직업군 워크플로우 14개 (Agent Skills 표준, Claude Code · Codex · Kiro 공통)
├── skills/nxt-demo/         체험 스킬 + samples/<name>/ 샘플 데이터 14세트
├── guide/ research/ education/ admin/ project/ engineering/   전문가 에이전트 27개
├── docs/
│   ├── guide.html           사용 안내서 + 데모 핸즈온 (브라우저로 열기)
│   ├── handson/             직업군별 핸즈온 시나리오 4쪽
│   ├── agents.md            전문가 목록
│   └── CONTRIBUTING.md      작성 규칙
├── scripts/
│   ├── install.sh           설치 (Claude Code, Codex, Kiro)
│   ├── package-skills.sh    그 밖의 도구용 스킬 zip
│   ├── lint-agents.sh       에이전트 형식 검사
│   ├── lint-skills.sh       스킬 형식 검사
│   ├── build-guide.py       docs/guide.html 생성
│   ├── build-handson.py     docs/handson/*.html 생성
│   └── guide_theme.css      두 생성기가 공유하는 디자인 토큰·스타일
└── divisions.json           디비전 정의
```

## ✍️ 추가·수정

- 스킬: `skills/<name>/SKILL.md`. 프론트매터는 claude.ai 업로드 제한 때문에 `name description license compatibility metadata` 다섯 키만 씁니다.
- 에이전트: `<디비전>/<디비전>-<slug>.md`. 규칙은 [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).
- 검사: `./scripts/lint-agents.sh && ./scripts/lint-skills.sh`

## 📜 라이선스와 출처

MIT. 전문가 에이전트의 원본은 [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)(MIT, AgentLand Contributors)이며 각 파일 끝에 원본 경로를 표기했습니다. [LICENSE](LICENSE)
