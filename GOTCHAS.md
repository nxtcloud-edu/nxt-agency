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

- **Kiro 커스텀 에이전트는 `~/.kiro/agents/<name>.md`(프론트매터 + 본문 = 시스템 프롬프트).** IDE와 CLI가 같은 경로·형식을 문서화하고 있으나, 과거에 형식이 달랐던 이슈(kirodotdev/Kiro#8040)가 있었다. `install.sh`는 문서 기준 마크다운 형식(`name`, `description`, `tools`)으로 변환한다. 문제가 생기면 `tools`를 `["@builtin"]`으로 바꿔 시험한다.
- **Kiro 스킬은 `~/.kiro/skills/<name>/SKILL.md`로 Agent Skills 표준을 그대로 쓴다.** 변환 없이 디렉터리 복사.

## 스크립트

- **macOS 기본 bash는 3.2다.** `mapfile`, 연관 배열(`declare -A`)을 쓰면 실패한다. `while read` 루프와 일반 배열만 쓴다.

## 사용 안내서 (docs/guide.html)

- **생성 스크립트로 만든다.** 스킬·에이전트 프론트매터와 "이렇게 시작하세요" 예시를 읽어 HTML에 박아 넣으므로, 스킬이나 에이전트를 바꾸면 안내서도 다시 생성해야 한다. 생성기는 `scripts/build-guide.py`. 스킬·에이전트 수정 후 `python3 scripts/build-guide.py` 실행.
- **Claude in Chrome 확장은 아티팩트 프레임을 캡처하지 못한다.** 아티팩트 화면이 비어 보여도 `read`로 저장 내용을 확인하고, 렌더링 검증은 로컬 `python3 -m http.server`로 한다(file:// 은 확장이 차단).
