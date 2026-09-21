# GOTCHAS

작업 중 만난 함정과 근본 원인. 우회하기 전에 여기에 먼저 기록한다.

## 에이전트 파일

- **Claude Code 서브에이전트 `name`은 kebab-case ASCII여야 한다.** 원본 agency-agents는 `name: Frontend Developer`처럼 공백 있는 이름을 쓰지만, 우리는 `name`을 식별자로, 한글 표시명은 `title`로 분리했다. 설치 스크립트는 `name`을 파일명으로 쓴다.
- **`description`이 자동 위임의 기준이다.** "무엇을 하는지"만 쓰면 Claude가 위임 시점을 못 잡는다. 반드시 "언제 쓰는지"를 함께 적는다.
- **HWP/HWPX는 코드로 직접 생성이 어렵다.** 문서 생성기는 DOCX로 만든 뒤 한컴오피스에서 변환하도록 안내한다.
- **법령 조항 번호를 지어내기 쉽다.** 규정·법령 검토관, 개인정보보호 담당관은 법령명 수준으로만 언급하고 "최종 판단은 법무·감사 부서 확인" 고지를 둔다.

## 스크립트

- `scripts/install.sh`는 `source:` 프론트매터가 있는 파일만 `--uninstall` 대상으로 삼는다. 사용자가 직접 만든 다른 에이전트를 지우지 않기 위한 안전장치다.

## 스킬 (SKILL.md)

- **claude.ai 업로드는 프론트매터 키를 `name description license compatibility metadata allowed-tools`로 제한한다.** Claude Code 전용 키(`disable-model-invocation`, `context: fork`, `arguments` 등)를 넣으면 업로드가 거부된다. 세 플랫폼 공통을 위해 스킬은 표준 키만 쓰고, 직업군·사용 에이전트는 `metadata` 아래에 넣는다. `lint-skills.sh`가 검사한다.
- **스킬 이름은 ASCII kebab-case만 가능하다.** `/회의록` 같은 한글 명령은 Claude Code·Kiro 모두 지원하지 않는다. 대신 `metadata.title`에 한글 이름을 두고 README에서 한글로 안내한다.
- **claude.ai·Kiro에는 우리 서브에이전트가 없을 수 있다.** 스킬은 각 단계에 "에이전트가 있으면 위임, 없으면 아래 요령대로 직접"을 명시하고 핵심 규칙·서식을 스킬 안에 요약해 둔다.

## Kiro

- **Kiro 커스텀 에이전트는 `~/.kiro/agents/<name>.json`으로 넣는다.** 문서에는 마크다운(프론트매터+본문) 형식도 있지만 Kiro CLI 2.x(확인: 2.21.1)는 JSON만 읽고 마크다운은 무시한다(`agent validate`가 "invalid JSON"으로 거부). JSON은 `name`·`description`·`prompt`·`tools`·`resources: ["skill://~/.kiro/skills/*/SKILL.md"]`이며 unknown field는 거부되므로 출처 표기는 `prompt` 안 주석으로 넣는다. `install.sh`는 JSON으로 변환하고 예전 `.md`를 정리한다(2026-09-21 검증·목록·실행 확인).
- **Kiro 스킬은 `~/.kiro/skills/<name>/SKILL.md`로 Agent Skills 표준을 그대로 쓴다.** 변환 없이 디렉터리 복사.
- **Kiro Crew는 스킬을 `~/.kiro/crew/skills`(와 프로젝트 `.kiro/skills`, 설정 `skills.extra_paths`)에서만 읽는다.** `~/.kiro/skills`는 보지 않으므로 Crew에서 쓰려면 복사하거나 extra_paths에 추가한다.
- **Kiro "Powers"(IDE 플러그인, Agent Plugins 규격 루트 `plugin.json`)는 스킬과 MCP만 담고 에이전트는 담지 못한다.** 그래서 지원하지 않기로 함(2026-09-21). 다시 검토한다면 `.claude-plugin/plugin.json`과 다른 파일이라 공존 가능하고, 규격이 `additionalProperties: false`라 정해진 키만 써야 하며, 설치는 IDE Powers 패널(GitHub/폴더)뿐이고 CLI·Crew에는 없다.

## 스크립트

- **macOS 기본 bash는 3.2다.** `mapfile`, 연관 배열(`declare -A`)을 쓰면 실패한다. `while read` 루프와 일반 배열만 쓴다.

## 사용 안내서 (docs/guide.html)

- **생성 스크립트로 만든다.** 스킬·에이전트 프론트매터와 "이렇게 시작하세요" 예시를 읽어 HTML에 박아 넣으므로, 스킬이나 에이전트를 바꾸면 안내서도 다시 생성해야 한다. 핸즈온 4쪽(`docs/handson/`)도 같은 방식으로 `build-handson.py`가 샘플 README(체험할 수 있는 것·파일·시작 문장·기대 결과)와 SKILL.md(질문·단계)에서 체크리스트를 만든다. **샘플 README 형식을 바꾸면 정규식이 깨진다** — 형식은 SAMPLE 규칙(docs/CONTRIBUTING.md) 그대로 유지. 생성기는 `scripts/build-guide.py`. 스킬·에이전트 수정 후 `python3 scripts/build-guide.py` 실행.
- **긴 한 줄 명령은 복사 버튼과 겹친다.** `pre.cmd`에 오른쪽 여백 72px을 둔 이유. 버튼을 옮기지 말고 여백을 유지한다.
- **Claude in Chrome 확장은 아티팩트 프레임을 캡처하지 못한다.** 아티팩트 화면이 비어 보여도 `read`로 저장 내용을 확인하고, 렌더링 검증은 로컬 `python3 -m http.server`로 한다(file:// 은 확장이 차단).

- **핸즈온 페르소나 상자의 오른쪽 열에 `white-space:nowrap`을 주면 좁은 화면에서 왼쪽 글이 한 글자씩 세로로 늘어진다.** 그리드 `auto` 열이 줄바꿈 금지된 긴 명령 순서(`/a → /b → /c → /d`) 폭만큼 커지면서 `minmax(0,1fr)` 열이 0에 가깝게 눌린 것. 긴 문자열이 있는 열은 `overflow-wrap:anywhere`와 `max-width`를 주고, 900px 아래에서는 한 열로 쌓는다. 모바일 폭(390·700px) 캡처로 확인.

## Codex

- **Codex 커스텀 에이전트는 `~/.codex/agents/<name>.toml`** (`name`, `description`, `developer_instructions`). 본문은 TOML 다중행 리터럴 `'''…'''`로 넣으므로 **에이전트 본문에 `'''`가 들어가면 깨진다.** 현재 0건. 서브에이전트로 쓰려면 Codex 설정에서 `agents.enabled`를 켜야 한다.
- **Codex 스킬은 `~/.codex/skills/<name>/SKILL.md`** (프로젝트 스코프는 문서 기준 `.agents/skills/`). 호출은 `/`가 아니라 `$skill-name` 또는 `/skills`. 안내서·README에 이 차이를 적어 두었다.
- **설치 예시는 Claude Code · Codex · Kiro 세 가지만 명시한다.** 그 밖의 도구(claude.ai 웹 등)는 "Agent Skills 표준이라 가능"으로만 언급하고 zip 패키징 스크립트를 안내한다(Glen 결정, 2026-09-20).

## 체험 샘플 (skills/nxt-demo/samples/)

- **샘플은 `/nxt-demo` 스킬 폴더 안에 둔다.** 레포 루트 `samples/`에 두면 설치·zip 시 따라가지 않는다. 스킬 폴더 안에 있어야 Claude Code·Codex·Kiro·claude.ai 어디서든 스킬이 상대 경로로 읽는다.
- **스킬 하나마다 샘플 폴더 하나가 필수다.** `lint-skills.sh`가 공통 역할이 아닌 스킬에 `samples/<name>/README.md`가 없으면 오류를 낸다. 스킬을 추가하면 샘플도 같이 만든다.
- **샘플은 전부 가상 데이터.** 넥클대학교·(주)가온테크·가상 인물만 쓰고, 입력 .md 첫 줄에 `# [샘플] 가상 데이터 — 체험용`, 연락처는 010-0000-0000·example.com만. 실제 번호·주민번호 패턴은 grep으로 검사한다.
- **일부러 함정을 넣는다.** 담당 미정, 개인정보 섞인 문의, 미달 지표, 부풀리고 싶은 경험 등. 스킬이 이를 처리하는 모습이 체험의 핵심이므로 "깨끗한" 샘플로 고치지 않는다.
- **체험 결과만 보여 주면 이해가 안 된다(Glen 피드백, 2026-09-20).** `/nxt-demo`는 실행 전에 "자료 소개"(무슨 자료, 안건별 내용, 함정)를 먼저 보여 주고, 결과 아래에 "이렇게 처리했습니다"를 붙인다. 샘플 README의 `**내용**:` 줄이 그 재료이며 핸즈온 페이지의 "자료에 들어 있는 것"에도 쓰인다. 새 샘플을 만들 때 이 줄을 빠뜨리지 않는다.

## 발표자료 캡처 (제작도구/capture)

- **`script -q <file> bash -lc <cmd>`는 표준입력이 없으면 아무것도 기록하지 않고 종료 코드 1로 끝난다.** 에이전트 셸(Bash 도구)처럼 stdin이 닫힌 환경에서 그렇다. 반드시 `</dev/null`을 붙인다. 또 기록 파일 앞에 `^D` 두 글자와 백스페이스가 남으므로 지운다.
- **Claude Code 화면은 `claude -p`로 실제 출력을 받아 렌더링한다.** 비대화 모드에서는 스킬의 "시작할까요?" 확인 없이 끝까지 진행되므로, 중간 장면(자료 소개)이 필요하면 프롬프트에 "여기까지만 보여 주고 멈춰 줘"를 붙여 따로 받는다.
- **Claude CLI 진행 표시는 바뀐 글자만 덮어쓴다(diff 렌더링).** `claude plugin install` 출력은 `CSI 1A`(한 줄 위로)·`CSI nG`(열 이동)로 이전 줄 위에 바뀐 글자만 찍으므로, 커서 이동을 무시하고 이어 붙이면 "Successful y  stalled plugi :"처럼 깨진다. `capture/render.mjs`의 `cleanTerminal`이 셀 버퍼로 흉내 내 실제 화면과 같게 만든다(한글은 2칸).
- **발표 서버 API 업로드는 `Host: 127.0.0.1:<포트>` 헤더와 `.pptx`로 끝나는 `name`이 필요하다.** `localhost`로 부르면 403("이 컴퓨터의 편집 화면에서만"), 이름에 확장자가 없으면 400. 서버는 `data/catalog.json`을 시작할 때와 자기 API로 바꿀 때만 읽으므로, 이전 버전을 파일에서 지웠으면 서버를 재시작해야 목록에서 사라진다.
- **발표 서버 importer는 메모를 '설명' 한 구간으로만 저장한다.** `[화면 진행]` 등 네 구간으로 보이려면 등록 직후 `제작도구/서버등록/split-notes.py <서버> <덱ID>`로 data/manifest/notes.json의 sections를 나눠야 한다(GIST 4주차도 publish 파이프라인에서 같은 처리를 했음). 메모 편집 후에는 실행 금지(revision>0이면 스크립트가 거부).


## Claude Code 플러그인

- **plugin.json의 `agents`에는 디렉터리를 나열할 수 없다.** `["./admin/", …]`는 "Invalid input"으로 거부되고 파일 경로 배열만 통과한다(문자열 하나로 디렉터리 하나는 가능). 우리 에이전트는 디비전 폴더 6개에 흩어져 있어 파일 27개를 명시하며, `scripts/update-plugin-manifest.py`가 생성하고 lint가 동기화를 검사한다.
- **플러그인으로 설치하면 스킬·에이전트 이름에 접두어가 붙는다.** `/nxt-agency:meeting-minutes`, `@nxt-agency:statistician`. 설명(description) 기반 자동 위임은 접두어와 무관하게 동작하므로 초보자에게는 "말로 요청" 안내가 더 중요하다. install.sh 설치(접두어 없음)와 플러그인 설치를 함께 쓰면 같은 이름이 두 벌 생기니 한쪽만 쓴다.
- **`claude plugin details`는 매니페스트 `agents`에 파일로 나열한 에이전트를 "Agents (0)"로 표시한다.** 인벤토리가 `agents/` 폴더만 세는 듯하다. 실제 세션(`claude -p`)에서는 27개가 모두 `nxt-agency:<name>`으로 잡히므로 표시 문제일 뿐이다. 동작 확인은 details가 아니라 세션에서 Agent 도구 목록을 물어봐서 한다(2026-09-20 확인).
- **플러그인 설치·마켓플레이스 등록은 GitHub에 푸시된 커밋 기준이다.** 로컬만 바꾸고 `/plugin install`을 하면 옛 버전이 들어간다. 갱신 순서: 커밋·푸시 → `claude plugin marketplace update nxt-agency` → 재설치.
