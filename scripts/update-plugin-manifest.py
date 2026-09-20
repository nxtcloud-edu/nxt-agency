#!/usr/bin/env python3
"""플러그인 매니페스트(.claude-plugin/plugin.json)의 agents 목록을 실제 에이전트 파일로 갱신한다.

플러그인 규격상 agents 에 디렉터리를 나열할 수 없어(파일 경로만 허용) 파일을 명시해야 한다.
에이전트를 추가·삭제·이동했으면 실행하고 lint 로 검증한다:
  python3 scripts/update-plugin-manifest.py && claude plugin validate .
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DIVISIONS = ['guide', 'research', 'education', 'admin', 'project', 'engineering']
p = ROOT / '.claude-plugin' / 'plugin.json'
d = json.loads(p.read_text())
d['agents'] = sorted('./' + str(f.relative_to(ROOT)) for div in DIVISIONS for f in (ROOT / div).glob('*.md'))
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print(f"agents {len(d['agents'])}개 갱신")
