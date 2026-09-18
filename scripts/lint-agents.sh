#!/usr/bin/env bash
#
# nxt-agency 에이전트 파일 검사
#   - 프론트매터 필수 키: name title description color emoji vibe audience source
#   - name 은 kebab-case ASCII, 레포 전체에서 유일
#   - 필수 섹션: 정체성과 기억 / 핵심 임무 / 반드시 지킬 규칙 / 이렇게 요청하세요
#   - CRLF 금지, 출처 표기(> 원본:) 필수
#
# 사용: ./scripts/lint-agents.sh [파일 ...]   (인자 없으면 전체 검사)

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIVISIONS=(guide research education admin project engineering)
REQUIRED_KEYS=(name title description color emoji vibe audience source)
REQUIRED_SECTIONS=("정체성과 기억" "핵심 임무" "반드시 지킬 규칙" "이렇게 요청하세요")

errors=0
declare -a seen_names=()

frontmatter() {  # 프론트매터 블록만 출력
  awk 'NR==1{ if($0!="---") exit; next } $0=="---"{ exit } { print }' "$1"
}

lint_file() {
  local file="$1"
  local fm
  if LC_ALL=C grep -q $'\r' "$file"; then
    echo "ERROR $file: CRLF 줄바꿈 — LF로 변환하세요"; errors=$((errors+1)); return
  fi
  if [[ "$(head -1 "$file")" != "---" ]]; then
    echo "ERROR $file: 프론트매터(---)가 없습니다"; errors=$((errors+1)); return
  fi
  fm="$(frontmatter "$file")"
  for key in "${REQUIRED_KEYS[@]}"; do
    if ! grep -q "^${key}:[[:space:]]*[^[:space:]]" <<<"$fm"; then
      echo "ERROR $file: 프론트매터 '$key' 누락"; errors=$((errors+1))
    fi
  done
  local name
  name="$(grep '^name:' <<<"$fm" | head -1 | sed 's/^name:[[:space:]]*//')"
  if [[ -n "$name" && ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "ERROR $file: name '$name' 은 kebab-case ASCII 여야 합니다"; errors=$((errors+1))
  fi
  for s in "${seen_names[@]:-}"; do
    [[ "$s" == "$name" && -n "$name" ]] && { echo "ERROR $file: name '$name' 중복"; errors=$((errors+1)); }
  done
  seen_names+=("$name")
  for sec in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "^## .*${sec}" "$file"; then
      echo "ERROR $file: 섹션 '## … $sec' 누락"; errors=$((errors+1))
    fi
  done
  if ! grep -q '^> 원본:' "$file"; then
    echo "ERROR $file: 출처 표기('> 원본: …') 누락"; errors=$((errors+1))
  fi
  if grep -qE '^## (🧠 )?Your Identity|^## .*Core Mission|^## .*Critical Rules' "$file"; then
    echo "ERROR $file: 영어 섹션 제목이 남아 있습니다"; errors=$((errors+1))
  fi
}

files=("$@")
if [[ ${#files[@]} -eq 0 ]]; then
  for div in "${DIVISIONS[@]}"; do
    for f in "$REPO_ROOT/$div"/*.md; do [[ -f "$f" ]] && files+=("$f"); done
  done
fi

for f in "${files[@]}"; do lint_file "$f"; done

echo
echo "검사 파일: ${#files[@]}개, 오류: ${errors}개"
[[ $errors -eq 0 ]]
