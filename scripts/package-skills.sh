#!/usr/bin/env bash
#
# claude.ai 웹 업로드용 스킬 zip 생성
#   ./scripts/package-skills.sh            # dist/skills/<name>.zip (스킬마다 하나)
#   ./scripts/package-skills.sh --role 학생  # 그 직업군만
#
# 업로드: claude.ai → 설정 → 기능(Capabilities) → 스킬 → 스킬 추가 → zip 선택
# (claude.ai 는 프론트매터로 name/description/license/compatibility/metadata/allowed-tools 만 허용한다)

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$REPO_ROOT/dist/skills"
role=""
while [[ $# -gt 0 ]]; do case "$1" in --role) role="$2"; shift ;; *) echo "알 수 없는 옵션: $1" >&2; exit 1 ;; esac; shift; done

command -v zip >/dev/null || { echo "zip 명령이 필요합니다." >&2; exit 1; }
mkdir -p "$OUT"
count=0
for d in "$REPO_ROOT"/skills/*/; do
  [[ -f "$d/SKILL.md" ]] || continue
  name="$(basename "$d")"
  if [[ -n "$role" ]]; then
    r="$(awk '/^metadata:/{m=1;next} m&&/^[^ ]/{m=0} m&&/^  role:/{sub("^  role:[ ]*","");print;exit}' "$d/SKILL.md")"
    [[ "$r" == "$role" ]] || continue
  fi
  rm -f "$OUT/$name.zip"
  (cd "$REPO_ROOT/skills" && zip -qr "$OUT/$name.zip" "$name" -x '*.DS_Store')
  echo "생성 dist/skills/$name.zip"
  count=$((count+1))
done
echo
echo "완료: ${count}개. claude.ai → 설정 → 기능 → 스킬 → 스킬 추가 에서 zip 을 하나씩 올리세요."
