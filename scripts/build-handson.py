#!/usr/bin/env python3
"""docs/handson/<role>.html 생성기 — 직업군별 핸즈온 시나리오 4쪽.

  python3 scripts/build-handson.py

스킬(SKILL.md)과 체험 샘플(skills/nxt-demo/samples/<name>/README.md)에서 실습 내용을 뽑고,
아래 SCENARIOS 의 페르소나·상황·순서로 엮는다. 스킬이나 샘플을 바꾸면 다시 실행한다.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs' / 'handson'
CSS = (ROOT / 'scripts' / 'guide_theme.css').read_text()
e = html.escape

# ---------- 시나리오 정의 ----------
SCENARIOS = {
    'project': dict(
        role='사업단', key='project', title='사업단 핸즈온', minutes=90,
        persona='박지훈 팀장 · 넥클대학교 LINC 3.0 사업단',
        situation='10월 마지막 주. 연차 종료까지 넉 달 남았는데 장비비 집행률이 한 자릿수다. 다음 달에는 캡스톤디자인 성과발표회가 있고, 교육부에서 차년도 사업 공고가 떴다. 연차평가 성과보고서도 슬슬 시작해야 한다. 이 네 가지를 오늘 오후에 한 번씩 돌려 본다.',
        steps=[
            ('budget-check', '집행 현황부터 본다', '단장님이 "돈 얼마나 남았어?"라고 물을 때 바로 답할 수 있어야 한다.', 20,
             '우리 사업단의 세목별 집행 현황을 엑셀에서 CSV로 저장해 붙여 넣어 보세요. 담당자 메모는 걱정되는 점 세 가지만 적으면 충분합니다.'),
            ('event-prep', '성과발표회 준비를 표로 만든다', '담당이 정해지지 않은 일이 무엇인지 드러내는 것이 목표다.', 25,
             '다음 행사 개요를 붙여 넣으세요. 미정인 항목은 지우지 말고 "미정"이라고 그대로 두는 것이 좋습니다.'),
            ('performance-report', '연차 성과보고서 초안을 뽑는다', '미달 지표를 감추지 않고 원인과 보완 계획으로 바꾸는 법을 본다.', 25,
             'KPI 실적 대장과 만족도 조사 결과를 CSV로 붙여 넣으세요. 자유응답에 교수 실명이나 학번이 있으면 먼저 지웁니다.'),
            ('business-plan', '차년도 계획서 초안까지', '공고 평가지표에 맞춰 우리 강점을 배치하고, "전국 최초" 같은 표현이 걸러지는지 본다.', 20,
             '실제 공고 요강의 평가지표 표와 사업단 현황 자료를 붙여 넣으세요. 예산은 협약 금액 기준으로.'),
        ]),
    'admin': dict(
        role='행정', key='admin', title='행정 핸즈온', minutes=60,
        persona='최수아 주무관 · 넥클대학교 산학협력단 행정팀',
        situation='월요일 아침. 지난주 운영위원회 회의록 결재가 밀려 있고, 주말 사이 문의가 네 건 들어왔다. 취업역량 설문을 이번 주에 열어야 해서 동의서도 필요하고, 오후에는 중간평가 보고서를 처장님께 요약해 드려야 한다. 점심 전에 넷 다 초안을 만든다.',
        steps=[
            ('meeting-minutes', '회의록부터 결재 올린다', '결정된 것과 논의만 된 것을 구분하는 것이 회의록의 전부다.', 15,
             '녹음 자동 자막이나 손메모를 그대로 붙여 넣으세요. 일시·장소는 따로 적어 주면 됩니다.'),
            ('inquiry-reply', '문의 네 건에 답한다', '학부모의 성적 문의에 "알려 드릴 수 없다"를 정중하게 쓰는 법을 본다.', 15,
             '실제 문의는 이름·연락처를 지우고 붙여 넣으세요. 근거 규정이 있으면 규정명만 같이 적어 주면 답변에 반영됩니다.'),
            ('consent-form', '설문 동의서를 만든다', '수집 항목을 줄이는 것이 동의서보다 먼저다.', 15,
             '설문 계획서나 구글 폼 문항 목록을 붙여 넣으세요. 외부에 결과를 넘길 예정이면 그 사실을 꼭 적습니다.'),
            ('report-summary', '처장님 보고 1페이지', '40쪽을 1쪽으로 줄일 때 무엇을 남기는지 본다.', 15,
             '긴 보고서를 통째로 붙여 넣고, 보고 대상과 목적(결재용인지 참고용인지)만 알려 주세요.'),
        ]),
    'research': dict(
        role='교수·연구자', key='research', title='교수·연구자 핸즈온', minutes=75,
        persona='김서연 교수 · 넥클대학교 경영학과',
        situation='학기 초. 한국연구재단 중견연구 공고 마감이 3주 남았고, 지도 중인 석사생은 2장 문헌고찰이 막혀 있다. 지난 학기 강의평가가 좋지 않았던 전공 과목도 이번 학기에 손봐야 한다. 연구실에서 오후 내내 세 가지를 차례로 돌린다.',
        steps=[
            ('literature-review', '학생의 선행연구 정리를 같이 본다', '같은 데이터를 재사용한 논문 두 편이 근거 하나로 묶이는지 본다.', 25,
             '연구 주제와 검색 범위만 알려 줘도 시작됩니다. 이미 모은 문헌이 있으면 저자·연도·제목·설계를 목록으로 붙여 넣으세요.'),
            ('research-proposal', '공고 분석부터 계획서 초안까지', '배점표에 맞춰 계획서 목차를 짜고 예산 세목을 채운다.', 30,
             '공고문 PDF의 평가 항목·배점 표와 제출 서류 목록을 복사해 붙여 넣으세요. 내 실적은 최근 5년 요약이면 됩니다.'),
            ('syllabus', '강의평가를 반영해 강의계획서를 다시 짠다', '자유응답의 불만이 주차별 계획과 평가 기준에 실제로 반영되는지 본다.', 20,
             '과목 개요와 지난 강의평가(문항 평균 + 자유응답)를 붙여 넣으세요. 학과 전공역량 이름을 같이 주면 매핑까지 됩니다.'),
        ]),
    'student': dict(
        role='학생', key='student', title='학생 핸즈온', minutes=60,
        persona='이도윤 · 넥클대학교 경영학과 4학년',
        situation='2학기가 시작됐다. 18학점에 주 15시간 아르바이트, 캡스톤 중간 발표는 2주 뒤, 공공기관 채용 마감은 11일 뒤. 뭐부터 해야 할지 모르겠어서 셋 다 한 번씩 돌려 본다.',
        steps=[
            ('semester-plan', '이번 학기 시간부터 계산한다', '목표 세 개가 주당 가용 시간에 들어가는지 숫자로 본다.', 15,
             '시간표, 고정 일정, 목표를 적어 붙여 넣으세요. 지난 학기에 왜 무너졌는지 한 줄 적으면 계획이 달라집니다.'),
            ('capstone', '캡스톤 범위를 세 개로 줄인다', '기능 12개를 3개로 줄이고 2주 안에 돌아가는 시제품 계획을 받는다.', 25,
             '아이디어 메모와 팀원 역량, 발표일, 지도교수 요구사항을 붙여 넣으세요. 코드가 있으면 저장소 구조도 같이.'),
            ('cover-letter', '자기소개서 항목 초안', '"부풀려도 될까?"에 어떻게 답하는지 본다. 없는 경험은 절대 만들지 않는다.', 20,
             '채용공고(직무기술서·자소서 항목)와 내 경험 목록을 붙여 넣으세요. 숫자가 기억 안 나면 "약"이라고 쓰고 나중에 확인합니다.'),
        ]),
}

APPLY_HEAD = '내 자료로 하려면'

# ---------- 데이터 추출 ----------
def fm_body(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    return m.group(1), m.group(2)

def load_skill(name):
    f, b = fm_body((ROOT / 'skills' / name / 'SKILL.md').read_text())
    title = re.search(r'^  title:\s*(.*)$', f, re.M).group(1).strip()
    agents = re.search(r'^  agents:\s*\[(.*)\]', f, re.M).group(1).replace(' ', '').split(',')
    steps = re.findall(r'^### \d+단계\. (.+?) — 전문가: `([a-z0-9-]+)`\(([^)]+)\)', b, re.M)
    qsec = re.search(r'## 시작할 때 물어볼 것\n(.*?)\n(?:\n[^\d]|## )', b, re.S)
    questions = re.findall(r'^\d+\.\s*(.+)$', qsec.group(1), re.M) if qsec else []
    return dict(name=name, title=title, agents=agents, steps=steps, questions=questions)

def load_sample(name):
    t = (ROOT / 'skills' / 'nxt-demo' / 'samples' / name / 'README.md').read_text()
    can = re.search(r'\*\*이 샘플로 해 볼 수 있는 것\*\*:\s*(.+)', t).group(1).strip()
    cm = re.search(r'\*\*내용\*\*:\s*\n((?:- .*\n?)+)', t)
    content = [re.sub(r'^- ', '', l).strip() for l in cm.group(1).strip().splitlines()] if cm else []
    files = [(m.group(1).strip(), m.group(2).strip()) for m in re.finditer(r'\*\*파일\*\*:\s*([^\s—]+)\s*—\s*(.+)', t)]
    cmd = re.search(r'\*\*이렇게 시작하세요\*\*\s*```\n(.*?)\n```', t, re.S).group(1).strip()
    after = re.search(r'```\n(?:.*?)\n```\n(.*?)\n\*\*기대 결과\*\*', t, re.S)
    paste_note = after.group(1).strip() if after else ''
    expect = re.search(r'\*\*기대 결과\*\*:\s*(.+)$', t, re.S).group(1).strip()
    expect = re.sub(r'\n+', ' ', expect)
    return dict(can=can, content=content, files=files, cmd=cmd, paste_note=paste_note, expect=expect)

# ---------- 렌더링 ----------
EXTRA_CSS = r"""
.hero{border:1px solid var(--line);border-radius:var(--radius);padding:20px 22px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,max-content);gap:20px;align-items:start;background:var(--panel)}
.hero .persona{font-family:var(--font-display);font-size:1.25rem;margin-bottom:6px}
.hero .situation{color:var(--muted);max-width:66ch;margin:0}
.hero .meta{display:flex;flex-direction:column;gap:6px;font-size:.85rem;color:var(--muted);font-family:var(--font-mono);text-align:right;max-width:34ch;overflow-wrap:anywhere}
.hero .meta b{font-family:var(--font-display);font-size:1.6rem;color:var(--ink);display:block;line-height:1.1}
.progress{position:sticky;top:0;z-index:5;background:var(--paper);padding:10px 0;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:14px;font-size:.85rem;color:var(--muted)}
.progress .bar{flex:1;height:6px;background:var(--panel-2);border-radius:999px;overflow:hidden}
.progress .bar i{display:block;height:100%;width:0;background:var(--accent);transition:width .2s}
.progress button{font:inherit;font-size:.75rem;border:1px solid var(--line);background:var(--paper);color:var(--muted);padding:3px 9px;border-radius:999px;cursor:pointer}
.lab{border:1px solid var(--line);border-radius:var(--radius);display:grid;grid-template-columns:56px minmax(0,1fr);overflow:hidden}
.lab__no{background:var(--rs);color:var(--rc);font-family:var(--font-display);font-size:1.4rem;display:flex;align-items:flex-start;justify-content:center;padding-top:18px}
.lab__body{padding:18px 20px 20px;display:flex;flex-direction:column;gap:14px;min-width:0}
.lab__head{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap}
.lab__head h3{font-family:var(--font-body);font-weight:600;font-size:1.15rem}
.lab__head .cmdname{font-family:var(--font-mono);color:var(--rc);font-weight:600}
.lab__head .time{font-family:var(--font-mono);font-size:.8rem;color:var(--muted)}
.lab .story{margin:0;color:var(--muted);font-size:.95rem}
.lab .goal{margin:0;font-weight:500}
.block{display:flex;flex-direction:column;gap:8px}
.block .eyebrow{font-size:.7rem}
.files{margin:0;padding-left:1.2em;font-size:.92rem}
.files code{font-size:.85em}
.content{margin:0;font-size:.92rem;background:var(--panel);padding:10px 14px;border-radius:var(--radius)}
.content b{color:var(--rc);display:block;margin-bottom:4px;font-size:.8rem;letter-spacing:.04em}
.content ul{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:2px}
.expect{border-left:3px solid var(--rc);background:var(--panel);padding:10px 14px;font-size:.92rem;margin:0}
.apply{font-size:.9rem;color:var(--muted);margin:0}
.apply b{color:var(--ink)}
.done{border:1px dashed var(--line);border-radius:var(--radius);padding:16px 20px;display:flex;flex-direction:column;gap:8px}
.role-nav{display:flex;gap:8px;flex-wrap:wrap;font-size:.85rem}
.role-nav a{border:1px solid var(--line);border-radius:999px;padding:4px 12px;text-decoration:none;color:var(--muted)}
.role-nav a.is-here{border-color:var(--rc);color:var(--rc);background:var(--rs)}
@media (max-width:900px){.hero{grid-template-columns:1fr}.hero .meta{text-align:left;max-width:none}.hero .meta span{display:block}}
@media (max-width:700px){.lab{grid-template-columns:40px minmax(0,1fr)}.lab__body{padding:14px}.role-nav{flex-wrap:wrap}}
@media print{.progress,.theme-btn,.copy,.exline button{display:none!important}.lab{break-inside:avoid}}
"""

JS = r"""
(function(){
  var root=document.documentElement, KEY='nxt-handson-'+document.body.getAttribute('data-role');
  try{var t=localStorage.getItem('nxt-guide-theme'); if(t) root.setAttribute('data-theme',t);}catch(e){}
  var tb=document.getElementById('theme-btn');
  function label(){var cur=root.getAttribute('data-theme'); tb.textContent = cur==='dark'?'☀ 밝게':(cur==='light'?'◐ 시스템':'☾ 어둡게');}
  tb.addEventListener('click',function(){ var cur=root.getAttribute('data-theme'); var next=!cur?'dark':(cur==='dark'?'light':null);
    if(next) root.setAttribute('data-theme',next); else root.removeAttribute('data-theme');
    try{ next?localStorage.setItem('nxt-guide-theme',next):localStorage.removeItem('nxt-guide-theme'); }catch(e){} label(); }); label();

  var boxes=Array.prototype.slice.call(document.querySelectorAll('.check input')), bar=document.querySelector('.progress .bar i'), txt=document.getElementById('progress-text');
  var saved={}; try{ saved=JSON.parse(localStorage.getItem(KEY)||'{}'); }catch(e){}
  boxes.forEach(function(b){ if(saved[b.id]) b.checked=true; b.addEventListener('change',function(){ saved[b.id]=b.checked; try{localStorage.setItem(KEY,JSON.stringify(saved));}catch(e){} update(); }); });
  function update(){ var n=boxes.filter(function(b){return b.checked}).length; bar.style.width=(boxes.length?100*n/boxes.length:0)+'%'; txt.textContent=n+' / '+boxes.length+' 확인'; }
  update();
  document.getElementById('reset').addEventListener('click',function(){ boxes.forEach(function(b){b.checked=false}); saved={}; try{localStorage.removeItem(KEY);}catch(e){} update(); });

  var toast=document.getElementById('toast'), timer;
  function show(m){ toast.textContent=m; toast.classList.add('show'); clearTimeout(timer); timer=setTimeout(function(){toast.classList.remove('show')},1400); }
  document.addEventListener('click',function(ev){ var b=ev.target.closest('[data-copy]'); if(!b) return;
    if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function(){show('복사했습니다')},function(){show('복사 실패 — 직접 선택해 복사하세요')}); } else show('이 브라우저에서는 자동 복사가 안 됩니다'); });
})();
"""

def copy_btn(text, cls='copy'):
    return f'<button type="button" class="{cls}" data-copy="{e(text)}">복사</button>'

def render_lab(i, sc, step):
    name, headline, story, minutes, apply = step
    sk, sm = load_skill(name), load_sample(name)
    files = ''.join(f'<li><code>{e(fn)}</code> — {e(desc)}</li>' for fn, desc in sm['files'])
    checks = []
    for q in sk['questions']:
        q = re.sub(r'\s*\(기본값:.*\)\s*$', '', q)
        checks.append(f'명령이 먼저 물어본 것에 답했다: {q}')
    for st, ag, agt in sk['steps']:
        checks.append(f'{st} 결과를 받았다 (담당 전문가: {agt})')
    checks.append('"여기까지 확인하시겠어요?"에서 멈추거나 "끝까지"로 진행했다')
    checks.append('결과에 지어낸 사실이 없는지, 빈 값이 "[확인 필요]"로 남았는지 봤다')
    check_html = ''.join(
        f'<li><input type="checkbox" id="{sc["key"]}-{i}-{k}"><label for="{sc["key"]}-{i}-{k}">{e(c)}</label></li>'
        for k, c in enumerate(checks))
    paste = f'<p class="apply">{e(sm["paste_note"])}</p>' if sm['paste_note'] else ''
    content = ('<div class="content"><b>자료에 들어 있는 것</b><ul>' + ''.join(f'<li>{e(b)}</li>' for b in sm['content']) + '</ul></div>') if sm['content'] else ''
    return f'''
<article class="lab" id="lab-{i}">
  <div class="lab__no">{i}</div>
  <div class="lab__body">
    <div class="lab__head"><h3>{e(headline)}</h3><span class="cmdname">/{e(name)} · {e(sk["title"])}</span><span class="time">약 {minutes}분</span></div>
    <p class="story">{e(story)}</p>
    <p class="goal">{e(sm["can"])}</p>
    <div class="block"><div class="eyebrow">준비 · 샘플 파일 (skills/nxt-demo/samples/{e(name)}/)</div><ul class="files">{files}</ul>{content}</div>
    <div class="block"><div class="eyebrow">실행</div>
      <div class="cmd-wrap"><pre class="cmd">{e(sm["cmd"])}</pre>{copy_btn(sm["cmd"])}</div>{paste}</div>
    <div class="block"><div class="eyebrow">진행하며 확인</div><ul class="check">{check_html}</ul></div>
    <div class="block"><div class="eyebrow">기대 결과</div><p class="expect">{e(sm["expect"])}</p></div>
    <p class="apply"><b>{APPLY_HEAD}.</b> {e(apply)}</p>
  </div>
</article>'''

def render_page(sc):
    key = sc['key']
    total = sum(s[3] for s in sc['steps'])
    labs = ''.join(render_lab(i + 1, sc, s) for i, s in enumerate(sc['steps']))
    nav = ''.join(
        f'<a href="{e(k)}.html" class="{"is-here" if k == key else ""}">{e(v["role"])}</a>'
        for k, v in SCENARIOS.items())
    order = ' → '.join(f'/{s[0]}' for s in sc['steps'])
    body = f'''
<header class="masthead">
  <div class="masthead__in">
    <div class="brand">
      <div class="eyebrow">nxt-agency · 핸즈온 시나리오</div>
      <h1>{e(sc["title"])}</h1>
      <div class="sub">{e(sc["role"])} 담당자가 실제 업무 순서대로 명령 {len(sc["steps"])}개를 샘플 데이터로 따라 해 봅니다. 체크한 항목은 이 브라우저에 저장됩니다.</div>
    </div>
    <div class="doc-meta">
      <div class="stamp">실습</div>
      <div><a href="../guide.html">사용 안내로</a></div>
      <button class="theme-btn" id="theme-btn" type="button">☾ 어둡게</button>
    </div>
  </div>
</header>
<div class="layout" style="grid-template-columns:1fr;max-width:920px">
<main style="--rc:var(--r-{key});--rs:var(--r-{key}-soft);gap:28px">
  <nav class="role-nav" aria-label="직업군 선택">{nav}</nav>
  <section class="hero">
    <div><div class="eyebrow">페르소나</div><div class="persona">{e(sc["persona"])}</div><p class="situation">{e(sc["situation"])}</p></div>
    <div class="meta"><span><b>{total}분</b>총 소요</span><span>{e(order)}</span></div>
  </section>
  <div class="progress"><span>진행률</span><div class="bar"><i></i></div><span id="progress-text">0 / 0 확인</span><button type="button" id="reset">초기화</button></div>
  <div class="note">시작 전 확인: 설치가 되어 있어야 합니다. <code>/</code>(Codex는 <code>$</code>)를 쳤을 때 <code>nxt-demo</code>가 목록에 보이면 준비된 것입니다. Claude Code 플러그인으로 넣었다면 <code>nxt-agency:nxt-demo</code>처럼 접두어가 붙어 보이며, 아래 실행 명령 앞에도 <code>nxt-agency:</code>를 붙여 치거나 그냥 말로 요청하면 됩니다. 샘플 파일은 레포의 <code>skills/nxt-demo/samples/</code> 또는 설치된 스킬 폴더 안에 있습니다. 붙여 넣기가 번거로우면 <code>/nxt-demo</code>에게 "{e(sc["steps"][0][0])} 샘플로 해 줘"라고 해도 됩니다.</div>
  {labs}
  <section class="done">
    <div class="eyebrow">마무리</div>
    <p style="margin:0">네 가지 결과를 나란히 놓고 보면 공통점이 있습니다. 명령은 자료에 없는 것을 지어내지 않고 <b>[확인 필요]</b>로 남기며, 담당·기한·근거가 빠진 자리를 드러냅니다. 실제 업무에서는 그 빈칸을 채우는 것이 사람의 일입니다.</p>
    <p style="margin:0" class="apply">다음 단계: 오늘 만든 결과 중 하나를 골라 내 자료로 다시 돌려 보세요. 이름·학번·연락처는 지우고 넣습니다. 어떤 명령을 쓸지 모르겠으면 <b>안내 데스크</b>에게 상황을 말하면 됩니다.</p>
  </section>
</main>
</div>
<footer><div>nxt-agency · NXT Cloud · 모든 샘플은 가상 기관·가상 인물의 데이터입니다.</div><div><a href="../guide.html">사용 안내</a> · <a href="https://github.com/nxtcloud-edu/nxt-agency">GitHub</a></div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>{JS}</script>'''
    fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700;800&family=IBM+Plex+Sans+KR:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(sc["title"])} · nxt-agency</title>
{fonts}
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body data-role="{key}">{body}</body>
</html>
'''

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for key, sc in SCENARIOS.items():
        p = OUT / f'{key}.html'
        p.write_text(render_page(sc))
        print(p.relative_to(ROOT), len(p.read_text()), 'bytes')
