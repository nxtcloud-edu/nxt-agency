# nxt-agency

대학·공공기관용 한국어 Claude Code 서브에이전트 모음. 원본은 msitarzewski/agency-agents (MIT).

## 구조
- `skills/<name>/SKILL.md` — 직업군 워크플로우 14개. 프론트매터는 표준 5키만(claude.ai 업로드 제한). `metadata.role`·`metadata.agents` 필수
- `guide/ research/ education/ admin/ project/ engineering/` — 에이전트 마크다운 (디비전 = `divisions.json`)
- `scripts/install.sh` — Claude Code(`~/.claude`)·Codex(`~/.codex`)·Kiro(`~/.kiro`) 설치. Codex 에이전트는 TOML, Kiro 에이전트는 JSON 커스텀 에이전트(CLI·IDE 공통)로 변환
- `scripts/package-skills.sh` — 그 밖의 도구(claude.ai 웹 등)용 스킬 zip
- `scripts/lint-skills.sh` — 스킬 검사. 스킬 수정 후 반드시 실행
- `scripts/build-guide.py` — `docs/guide.html`(사용 안내서 + 데모 핸즈온) 생성. 스킬·에이전트 수정 후 재실행
- `scripts/build-handson.py` — `docs/handson/{project,admin,research,student}.html` 직업군별 핸즈온 시나리오 생성. 시나리오(페르소나·순서)는 스크립트 안 SCENARIOS. 스킬·샘플 수정 후 재실행
- `scripts/guide_theme.css` — 두 생성기가 공유하는 디자인 토큰. 색·폰트는 여기서만 바꾼다
- `scripts/lint-agents.sh` — 프론트매터·섹션·출처 표기 검사 + 플러그인 매니페스트 동기화 검사. 에이전트 수정 후 반드시 실행
- `.claude-plugin/plugin.json`·`marketplace.json` — Claude Code 플러그인 매니페스트. 에이전트 추가·삭제 시 `python3 scripts/update-plugin-manifest.py` 후 `claude plugin validate .`
- `docs/CONTRIBUTING.md` — 에이전트 작성 규칙(프론트매터 순서, 섹션 제목, 250줄 제한)

## 규칙
- 에이전트 본문은 전부 한글. 고유명사·기술 용어·코드만 영어
- `name`은 kebab-case ASCII, `title`이 한글 표시명. 둘을 섞지 않는다
- 법령 조항 번호 등 확인 안 된 사실은 쓰지 않는다
- 각 파일 끝에 `> 원본: agency-agents \`<경로>\` (MIT) …` 출처 한 줄 유지
- 스킬은 에이전트 없이도 동작하도록 요령·서식을 안에 요약한다
- 설치 예시는 Claude Code·Codex·Kiro만 명시, 나머지 도구는 "가능"으로만 언급
- macOS bash 3.2 호환 유지(mapfile·declare -A 금지)
- 함정은 GOTCHAS.md에 먼저 기록
