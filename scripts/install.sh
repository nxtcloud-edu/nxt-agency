#!/usr/bin/env bash
#
# nxt-agency 설치 — 전문가 에이전트(27)와 직업군 스킬(14)을 Claude Code / AWS Kiro 에 설치한다.
#
#   ./scripts/install.sh                          # 설치된 도구 자동 감지(~/.claude, ~/.kiro) 후 전부 설치
#   ./scripts/install.sh --tool claude-code       # Claude Code 만
#   ./scripts/install.sh --tool kiro              # AWS Kiro 만 (IDE·CLI 공통 경로 ~/.kiro)
#   ./scripts/install.sh --tool claude-code,kiro
#   ./scripts/install.sh --project                # 현재 폴더의 .claude/ 또는 .kiro/ 에 설치
#   ./scripts/install.sh --role 사업단              # 그 직업군 스킬 + 그 스킬이 쓰는 에이전트만
#   ./scripts/install.sh --skill meeting-minutes  # 스킬 하나 + 필요한 에이전트
#   ./scripts/install.sh --division admin,project # 디비전별 에이전트만
#   ./scripts/install.sh --agent meeting-minutes  # 에이전트 하나
#   ./scripts/install.sh --agents-only | --skills-only
#   ./scripts/install.sh --list                   # 목록
#   ./scripts/install.sh --dry-run                # 복사하지 않고 대상만 출력
#   ./scripts/install.sh --uninstall              # 이 레포에서 설치한 것만 제거
#
# claude.ai 웹에 올릴 zip 은 ./scripts/package-skills.sh 로 만든다.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIVISIONS=(guide research education admin project engineering)
ALL_TOOLS=(claude-code kiro)

scope="user"; tools=""; divisions=""; agents=""; skills=""; role=""
dry_run=0; uninstall=0; list_only=0; agents_only=0; skills_only=0

usage() { sed -n '2,19p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)     scope="project" ;;
    --user)        scope="user" ;;
    --tool)        tools="$2"; shift ;;
    --division)    divisions="$2"; shift ;;
    --agent)       agents="$2"; shift ;;
    --skill)       skills="$2"; shift ;;
    --role)        role="$2"; shift ;;
    --agents-only) agents_only=1 ;;
    --skills-only) skills_only=1 ;;
    --dry-run)     dry_run=1 ;;
    --uninstall)   uninstall=1 ;;
    --list)        list_only=1 ;;
    -h|--help)     usage; exit 0 ;;
    *) echo "알 수 없는 옵션: $1" >&2; usage; exit 1 ;;
  esac
  shift
done

# ---------- 공통 유틸 ----------
fm_value() {  # $1=file $2=key  (프론트매터 1단계 키)
  awk -v key="$2" '
    NR==1 && $0!="---" { exit }
    NR>1 && $0=="---" { exit }
    NR>1 && index($0, key":")==1 { sub("^"key":[ ]*", ""); print; exit }
  ' "$1"
}
fm_meta() {  # $1=file $2=metadata 하위 키 (예: role, agents)
  awk -v key="$2" '
    NR==1 && $0!="---" { exit }
    NR>1 && $0=="---" { exit }
    /^metadata:/ { inmeta=1; next }
    inmeta && /^[^ ]/ { inmeta=0 }
    inmeta && index($0, "  "key":")==1 { sub("^  "key":[ ]*", ""); print; exit }
  ' "$1"
}
body_after_fm() { awk 'NR==1 && $0=="---" {infm=1; next} infm && $0=="---" {infm=0; next} !infm {print}' "$1"; }
in_csv() { [[ -z "$2" ]] && return 0; local IFS=','; for i in $2; do [[ "$i" == "$1" ]] && return 0; done; return 1; }
list_has() { local n="$1"; shift; for i in "$@"; do [[ "$i" == "$n" ]] && return 0; done; return 1; }

# ---------- 도구 결정 ----------
detect_tools() {
  local found=()
  [[ -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" ]] && found+=(claude-code)
  [[ -d "$HOME/.kiro" ]] && found+=(kiro)
  [[ ${#found[@]} -eq 0 ]] && found=(claude-code)
  printf '%s\n' "${found[@]}"
}
if [[ -z "$tools" ]]; then
  TOOLS=()
  while IFS= read -r t; do TOOLS+=("$t"); done < <(detect_tools)
else
  IFS=',' read -r -a TOOLS <<<"$tools"
  for t in "${TOOLS[@]}"; do list_has "$t" "${ALL_TOOLS[@]}" || { echo "지원하지 않는 도구: $t (가능: ${ALL_TOOLS[*]})" >&2; exit 1; }; done
fi

tool_root() {  # $1=tool
  case "$1" in
    claude-code) [[ "$scope" == "project" ]] && echo "$(pwd)/.claude" || echo "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" ;;
    kiro)        [[ "$scope" == "project" ]] && echo "$(pwd)/.kiro"   || echo "$HOME/.kiro" ;;
  esac
}

# ---------- 스킬 선택 ----------
SEL_SKILLS=()   # "name|dir"
if [[ $agents_only -eq 0 ]]; then
  for d in "$REPO_ROOT"/skills/*/; do
    [[ -f "$d/SKILL.md" ]] || continue
    name="$(fm_value "$d/SKILL.md" name)"
    in_csv "$name" "$skills" || continue
    if [[ -n "$role" ]]; then [[ "$(fm_meta "$d/SKILL.md" role)" == "$role" ]] || continue; fi
    SEL_SKILLS+=("$name|${d%/}")
  done
fi

# 스킬이 쓰는 에이전트는 자동 포함
needed_agents=""
for entry in "${SEL_SKILLS[@]:-}"; do
  [[ -n "$entry" ]] || continue
  IFS='|' read -r _ d <<<"$entry"
  a="$(fm_meta "$d/SKILL.md" agents | tr -d '[]' | tr -d ' ')"
  needed_agents="${needed_agents:+$needed_agents,}$a"
done

# ---------- 에이전트 선택 ----------
SEL_AGENTS=()   # "division|name|file"
if [[ $skills_only -eq 0 ]]; then
  filter_agents="$agents"
  if [[ -n "$role" || -n "$skills" ]] && [[ -z "$agents" && -z "$divisions" ]]; then
    filter_agents="nxt-guide,$needed_agents"
  fi
  for div in "${DIVISIONS[@]}"; do
    [[ -d "$REPO_ROOT/$div" ]] || continue
    if [[ "$div" != "guide" ]] && ! in_csv "$div" "$divisions"; then continue; fi
    for f in "$REPO_ROOT/$div"/*.md; do
      [[ -f "$f" ]] || continue
      name="$(fm_value "$f" name)"
      [[ -n "$name" ]] || continue
      if [[ "$div" != "guide" ]] && ! in_csv "$name" "$filter_agents"; then continue; fi
      SEL_AGENTS+=("$div|$name|$f")
    done
  done
fi

# ---------- 목록 ----------
if [[ $list_only -eq 1 ]]; then
  echo "== 직업군 스킬 (/이름 으로 실행) =="
  printf '  %-20s %-10s %s\n' "name" "직업군" "title"
  for e in "${SEL_SKILLS[@]:-}"; do [[ -n "$e" ]] || continue; IFS='|' read -r n d <<<"$e"
    printf '  %-20s %-10s %s\n' "$n" "$(fm_meta "$d/SKILL.md" role)" "$(fm_meta "$d/SKILL.md" title)"; done
  echo; echo "== 전문가 에이전트 =="
  printf '  %-12s %-22s %s\n' "디비전" "name" "title"
  for e in "${SEL_AGENTS[@]:-}"; do [[ -n "$e" ]] || continue; IFS='|' read -r div n f <<<"$e"
    printf '  %-12s %-22s %s\n' "$div" "$n" "$(fm_value "$f" title)"; done
  exit 0
fi

if [[ ${#SEL_SKILLS[@]} -eq 0 && ${#SEL_AGENTS[@]} -eq 0 ]]; then
  echo "선택된 항목이 없습니다. --list 로 이름을 확인하세요." >&2; exit 1
fi

# ---------- Kiro 에이전트 변환 ----------
# Kiro 커스텀 에이전트(.md): 프론트매터(name/description/tools) + 본문 = 시스템 프롬프트
render_kiro_agent() {  # $1=division $2=file -> stdout
  local div="$1" f="$2" tools_line
  case "$div" in
    engineering) tools_line='["read", "write", "shell", "web"]' ;;
    *)           tools_line='["read", "write", "web"]' ;;
  esac
  printf -- '---\nname: %s\ndescription: %s\ntools: %s\n---\n' \
    "$(fm_value "$f" name)" "$(fm_value "$f" description | sed 's/"/\\"/g')" "$tools_line"
  printf '<!-- nxt-agency: %s -->\n' "$(fm_value "$f" source)"
  body_after_fm "$f"
}

# ---------- 설치 / 제거 ----------
do_file() {  # $1=동작(copy|render-kiro|copy-dir|remove) $2=src $3=dst [$4=division]
  local act="$1" src="$2" dst="$3" div="${4:-}"
  if [[ $dry_run -eq 1 ]]; then echo "[dry-run] $act  $dst"; return; fi
  case "$act" in
    copy)        mkdir -p "$(dirname "$dst")"; cp "$src" "$dst" ;;
    render-kiro) mkdir -p "$(dirname "$dst")"; render_kiro_agent "$div" "$src" > "$dst" ;;
    copy-dir)    rm -rf "$dst"; mkdir -p "$(dirname "$dst")"; cp -R "$src" "$dst" ;;
    remove)      rm -rf "$dst" ;;
  esac
}

is_ours() {  # 이 레포에서 설치한 파일인지 (출처 표기 검사)
  [[ -e "$1" ]] || return 1
  if [[ -d "$1" ]]; then grep -q 'nxt-agency' "$1/SKILL.md" 2>/dev/null
  else grep -qE '^source: |nxt-agency' "$1" 2>/dev/null; fi
}

for tool in "${TOOLS[@]}"; do
  root="$(tool_root "$tool")"
  echo "== $tool -> $root"
  n_a=0; n_s=0
  for e in "${SEL_AGENTS[@]:-}"; do [[ -n "$e" ]] || continue; IFS='|' read -r div name f <<<"$e"
    dst="$root/agents/$name.md"
    if [[ $uninstall -eq 1 ]]; then is_ours "$dst" && { do_file remove "$f" "$dst"; n_a=$((n_a+1)); }; continue; fi
    case "$tool" in
      claude-code) do_file copy "$f" "$dst" ;;
      kiro)        do_file render-kiro "$f" "$dst" "$div" ;;
    esac
    n_a=$((n_a+1))
  done
  for e in "${SEL_SKILLS[@]:-}"; do [[ -n "$e" ]] || continue; IFS='|' read -r name d <<<"$e"
    dst="$root/skills/$name"
    if [[ $uninstall -eq 1 ]]; then is_ours "$dst" && { do_file remove "$d" "$dst"; n_s=$((n_s+1)); }; continue; fi
    do_file copy-dir "$d" "$dst"
    n_s=$((n_s+1))
  done
  [[ $uninstall -eq 1 ]] && echo "   제거: 에이전트 ${n_a}개, 스킬 ${n_s}개" || echo "   설치: 에이전트 ${n_a}개, 스킬 ${n_s}개"
done

if [[ $uninstall -eq 0 && $dry_run -eq 0 ]]; then
  echo
  echo "이렇게 시작하세요:"
  echo "  /meeting-minutes          ← 스킬은 슬래시 명령으로 (Claude Code, Kiro 공통)"
  echo "  \"회의록 정리원으로 이 녹취록을 정리해줘\"   ← 전문가는 이름으로 부르기"
  echo "  claude.ai 웹에 올리려면: ./scripts/package-skills.sh"
fi
