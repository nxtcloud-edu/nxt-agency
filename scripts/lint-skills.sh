#!/usr/bin/env bash
#
# nxt-agency 직업군 스킬 검사
#   - skills/<name>/SKILL.md 의 name 이 디렉터리명과 같아야 함 (소문자·숫자·하이픈)
#   - 프론트매터 키는 name description license compatibility metadata 만 허용 (claude.ai 업로드 제한)
#   - metadata.role 은 사업단 | 행정 | 교수·연구자 | 학생 | 공통(항상 설치되는 체험·안내 스킬)
#   - 공통이 아닌 스킬은 skills/nxt-demo/samples/<name>/README.md 샘플이 있어야 함
#   - metadata.agents 의 각 name 이 레포 에이전트로 존재해야 함
#   - 필수 섹션: 시작할 때 물어볼 것 / 진행 단계 / 최종 산출물 / 하지 말 것 / 이렇게 시작하세요
#   - 150줄 초과는 경고
#
# 사용: ./scripts/lint-skills.sh [skills/<name>/SKILL.md ...]

set -uo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALLOWED_KEYS="name description license compatibility metadata allowed-tools"
ROLES=("사업단" "행정" "교수·연구자" "학생" "공통")
REQUIRED_SECTIONS=("시작할 때 물어볼 것" "진행 단계" "최종 산출물" "하지 말 것" "이렇게 시작하세요")
errors=0; warnings=0

agent_exists() { grep -rqx "name: $1" "$REPO_ROOT"/{guide,research,education,admin,project,engineering} 2>/dev/null; }
frontmatter() { awk 'NR==1{ if($0!="---") exit; next } $0=="---"{ exit } { print }' "$1"; }

lint() {
  local f="$1" dir name fm
  dir="$(basename "$(dirname "$f")")"
  if [[ "$(head -1 "$f")" != "---" ]]; then echo "ERROR $f: 프론트매터 없음"; errors=$((errors+1)); return; fi
  fm="$(frontmatter "$f")"
  name="$(grep '^name:' <<<"$fm" | sed 's/^name:[[:space:]]*//')"
  [[ "$name" == "$dir" ]] || { echo "ERROR $f: name '$name' ≠ 디렉터리 '$dir'"; errors=$((errors+1)); }
  [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { echo "ERROR $f: name 은 소문자·숫자·하이픈만"; errors=$((errors+1)); }
  grep -q '^description:[[:space:]]*[^[:space:]]' <<<"$fm" || { echo "ERROR $f: description 누락"; errors=$((errors+1)); }
  while IFS= read -r key; do
    [[ " $ALLOWED_KEYS " == *" $key "* ]] || { echo "ERROR $f: 허용되지 않는 프론트매터 키 '$key' (claude.ai 업로드 불가)"; errors=$((errors+1)); }
  done < <(grep -oE '^[a-zA-Z-]+:' <<<"$fm" | tr -d ':')
  local role; role="$(awk '/^metadata:/{m=1;next} m&&/^[^ ]/{m=0} m&&/^  role:/{sub("^  role:[ ]*","");print;exit}' <<<"$fm")"
  local ok=0; for r in "${ROLES[@]}"; do [[ "$r" == "$role" ]] && ok=1; done
  [[ $ok -eq 1 ]] || { echo "ERROR $f: metadata.role '$role' 은 ${ROLES[*]} 중 하나여야 함"; errors=$((errors+1)); }
  local agents; agents="$(awk '/^metadata:/{m=1;next} m&&/^[^ ]/{m=0} m&&/^  agents:/{sub("^  agents:[ ]*","");print;exit}' <<<"$fm" | tr -d '[]' | tr ',' ' ')"
  [[ -n "$agents" ]] || { echo "ERROR $f: metadata.agents 누락"; errors=$((errors+1)); }
  for a in $agents; do agent_exists "$a" || { echo "ERROR $f: 에이전트 '$a' 가 레포에 없음"; errors=$((errors+1)); }; done
  for s in "${REQUIRED_SECTIONS[@]}"; do grep -q "^## .*$s" "$f" || { echo "ERROR $f: 섹션 '## $s' 누락"; errors=$((errors+1)); }; done
  grep -q '^> nxt-agency 직업군 스킬' "$f" || { echo "ERROR $f: 마지막 출처 줄 누락"; errors=$((errors+1)); }
  LC_ALL=C grep -q $'\r' "$f" && { echo "ERROR $f: CRLF"; errors=$((errors+1)); }
  if [[ "$role" != "공통" && ! -f "$REPO_ROOT/skills/nxt-demo/samples/$name/README.md" ]]; then
    echo "ERROR $f: 체험 샘플 skills/nxt-demo/samples/$name/README.md 없음"; errors=$((errors+1))
  fi
  local lines; lines=$(wc -l < "$f"); [[ $lines -le 150 ]] || { echo "WARN  $f: ${lines}줄 (150줄 권장)"; warnings=$((warnings+1)); }
}

files=("$@")
[[ ${#files[@]} -eq 0 ]] && for f in "$REPO_ROOT"/skills/*/SKILL.md; do [[ -f "$f" ]] && files+=("$f"); done
for f in "${files[@]}"; do lint "$f"; done
echo; echo "검사 스킬: ${#files[@]}개, 오류: ${errors}개, 경고: ${warnings}개"
[[ $errors -eq 0 ]]
