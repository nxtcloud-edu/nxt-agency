#!/usr/bin/env python3
"""docs/guide.html 생성기 — 스킬·에이전트 파일에서 데이터를 읽어 사용 안내서를 다시 만든다.

  python3 scripts/build-guide.py                 # docs/guide.html 갱신
  python3 scripts/build-guide.py --artifact out.html   # 아티팩트 발행용(문서 뼈대 없이 <title>부터) 본문도 함께 저장

스킬이나 에이전트를 바꾸면 반드시 다시 실행한다.
"""
import json, html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

def extract(root):
    def fm(text):
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S); return m.group(1), m.group(2)
    def val(f, key):
        m = re.search(r'^'+key+r':\s*(.*)$', f, re.M); return m.group(1).strip().strip('"') if m else ''
    skills = []
    for d in sorted(root.glob('skills/*/SKILL.md')):
        f, b = fm(d.read_text())
        role = re.search(r'^  role:\s*(.*)$', f, re.M).group(1).strip()
        title = re.search(r'^  title:\s*(.*)$', f, re.M).group(1).strip()
        agents = re.search(r'^  agents:\s*\[(.*)\]', f, re.M).group(1).replace(' ', '').split(',')
        steps = re.findall(r'^### \d+단계\. (.+?) — 전문가', b, re.M)
        ex = re.search(r'## 이렇게 시작하세요\n(.*?)(?:\n>|\Z)', b, re.S).group(1)
        examples = [re.sub(r'^-\s*', '', l).strip().strip('`') for l in ex.strip().splitlines() if l.strip().startswith('-')]
        skills.append(dict(name=val(f, 'name'), title=title, role=role, desc=val(f, 'description'), agents=agents, steps=steps, examples=examples[:3]))
    agents = []
    divs = {'guide': '안내', 'research': '연구', 'education': '교육·진로', 'admin': '행정', 'project': '사업단', 'engineering': '개발'}
    for div in divs:
        for p in sorted(root.glob(f'{div}/*.md')):
            f, b = fm(p.read_text())
            ex = re.search(r'## 💬 이렇게 요청하세요\n(.*?)(?:\n>|\Z)', b, re.S)
            exs = [re.sub(r'^-\s*', '', l).strip().strip('"') for l in ex.group(1).strip().splitlines() if l.strip().startswith('-')] if ex else []
            agents.append(dict(name=val(f, 'name'), title=val(f, 'title'), emoji=val(f, 'emoji'), division=divs[div], desc=val(f, 'description'), example=exs[0] if exs else ''))
    return dict(skills=skills, agents=agents)

data = extract(ROOT)
e = html.escape
ROLES = ['사업단', '행정', '교수·연구자', '학생']
ROLE_KEY = {'사업단': 'project', '행정': 'admin', '교수·연구자': 'research', '학생': 'student'}
ROLE_WHO = {'사업단': 'LINC 3.0 · RIS · BK21 · 글로컬 등 사업단 직원', '행정': '대학 행정직원 · 공공기관 담당자', '교수·연구자': '교수 · 연구원 · 대학원생', '학생': '대학생 · 대학원생'}
DIV_ORDER = ['안내', '연구', '교육·진로', '행정', '사업단', '개발']
agent_title = {a['name']: a['title'] for a in data['agents']}

CSS = r"""
:root{
  --paper:#F6F7F4; --panel:#ECEEE8; --panel-2:#E2E5DD; --ink:#1C2530; --muted:#5A6470; --line:#D3D8CF;
  --accent:#2B5C8A; --accent-ink:#1E4468; --accent-soft:#DCE7F1; --seal:#B23A2E;
  --r-project:#8A4B1F; --r-project-soft:#F1E3D6; --r-admin:#2B5C8A; --r-admin-soft:#DCE7F1;
  --r-research:#5B3E8C; --r-research-soft:#E6DEF3; --r-student:#2E7D5B; --r-student-soft:#DAEEE3;
  --code-bg:#1E2630; --code-ink:#E8ECE6;
  --font-display:"Nanum Myeongjo","Apple SD Gothic Neo","Malgun Gothic",serif;
  --font-body:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif;
  --font-mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  --radius:4px; --shadow:0 1px 2px rgba(28,37,48,.06);
  color-scheme:light;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#141A20; --panel:#1B222A; --panel-2:#232C36; --ink:#E6E9E4; --muted:#9AA4AE; --line:#2E3742;
    --accent:#7FB0DC; --accent-ink:#A9CCEC; --accent-soft:#1F3347; --seal:#E0665A;
    --r-project:#D9A47A; --r-project-soft:#3A2A1E; --r-admin:#7FB0DC; --r-admin-soft:#1F3347;
    --r-research:#B49BE0; --r-research-soft:#2E2540; --r-student:#7FC7A3; --r-student-soft:#1E3A2C;
    --code-bg:#0F141A; --code-ink:#DDE3DC; --shadow:none; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --paper:#141A20; --panel:#1B222A; --panel-2:#232C36; --ink:#E6E9E4; --muted:#9AA4AE; --line:#2E3742;
  --accent:#7FB0DC; --accent-ink:#A9CCEC; --accent-soft:#1F3347; --seal:#E0665A;
  --r-project:#D9A47A; --r-project-soft:#3A2A1E; --r-admin:#7FB0DC; --r-admin-soft:#1F3347;
  --r-research:#B49BE0; --r-research-soft:#2E2540; --r-student:#7FC7A3; --r-student-soft:#1E3A2C;
  --code-bg:#0F141A; --code-ink:#DDE3DC; --shadow:none; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font-body);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{color:var(--accent-ink)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:2px}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
code,kbd{font-family:var(--font-mono);font-size:.92em}
p code{background:var(--panel);padding:.1em .35em;border-radius:var(--radius)}
h1,h2,h3,h4{font-family:var(--font-display);font-weight:700;line-height:1.3;text-wrap:balance;margin:0}
h2{font-size:1.75rem;letter-spacing:-.01em}
h3{font-size:1.2rem}
.eyebrow{font-family:var(--font-body);font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}

.masthead{border-bottom:1px solid var(--line);background:var(--paper)}
.masthead__in{max-width:1180px;margin:0 auto;padding:22px 24px;display:flex;align-items:flex-start;justify-content:space-between;gap:16px;flex-wrap:wrap}
.brand{display:flex;flex-direction:column;gap:6px}
.brand h1{font-size:2.1rem}
.brand .sub{color:var(--muted);font-size:.95rem;max-width:56ch}
.doc-meta{display:flex;flex-direction:column;align-items:flex-end;gap:8px;font-size:.8rem;color:var(--muted);font-family:var(--font-mono)}
.stamp{display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;border:2px solid var(--seal);color:var(--seal);border-radius:50%;font-family:var(--font-display);font-weight:700;font-size:.95rem;letter-spacing:.05em;transform:rotate(-8deg);opacity:.85;line-height:1.1;text-align:center}
.theme-btn{font:inherit;font-size:.8rem;border:1px solid var(--line);background:var(--panel);color:var(--ink);padding:5px 10px;border-radius:999px;cursor:pointer}
.theme-btn:hover{border-color:var(--accent)}

.layout{max-width:1180px;margin:0 auto;padding:32px 24px 80px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:48px}
.toc{position:sticky;top:20px;align-self:start;display:flex;flex-direction:column;gap:4px;font-size:.9rem}
.toc .eyebrow{margin-bottom:8px}
.toc a{color:var(--muted);text-decoration:none;padding:5px 10px;border-left:2px solid var(--line);display:flex;gap:10px}
.toc a b{font-family:var(--font-mono);font-weight:500;color:var(--muted);min-width:1.4em}
.toc a:hover,.toc a.is-active{color:var(--ink);border-left-color:var(--accent)}
main{display:flex;flex-direction:column;gap:64px;min-width:0}
section{display:flex;flex-direction:column;gap:20px;scroll-margin-top:16px}
.sec-head{display:flex;flex-direction:column;gap:6px}
.sec-head .num{font-family:var(--font-mono);color:var(--seal);font-size:.85rem}
.prose{max-width:68ch}
.prose p{margin:0 0 .9em}
.prose ul,.prose ol{margin:0 0 .9em;padding-left:1.3em}
.prose li{margin:.25em 0}

.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line);max-width:640px}
.fact{background:var(--paper);padding:16px 18px;display:flex;flex-direction:column;gap:2px}
.fact b{font-family:var(--font-display);font-size:1.9rem;font-variant-numeric:tabular-nums;line-height:1.1}
.fact span{font-size:.85rem;color:var(--muted)}

[data-tabs]{display:flex;flex-direction:column;gap:20px}
.tabs{display:flex;gap:0;border-bottom:1px solid var(--line);flex-wrap:wrap}
.tab{font:inherit;background:none;border:0;border-bottom:2px solid transparent;margin-bottom:-1px;padding:10px 16px;color:var(--muted);cursor:pointer;font-weight:500}
.tab:hover{color:var(--ink)}
.tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--accent)}
.panel{display:flex;flex-direction:column;gap:16px}
.panel[hidden]{display:none}

.step-list{display:flex;flex-direction:column;gap:14px;counter-reset:step;max-width:720px}
.step{display:grid;grid-template-columns:32px minmax(0,1fr);gap:14px;align-items:start}
.step::before{counter-increment:step;content:counter(step);width:28px;height:28px;border:1px solid var(--accent);color:var(--accent);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--font-mono);font-size:.85rem;margin-top:3px}
.step h4{font-family:var(--font-body);font-weight:600;font-size:1rem;margin-bottom:4px}
.step p{margin:0;color:var(--muted);font-size:.95rem}
.note{border-left:3px solid var(--accent);background:var(--panel);padding:12px 16px;font-size:.95rem;max-width:720px}
.note--warn{border-left-color:var(--seal)}

pre.cmd{background:var(--code-bg);color:var(--code-ink);font-family:var(--font-mono);font-size:.88rem;line-height:1.6;padding:14px 16px;margin:0;border-radius:var(--radius);overflow-x:auto;position:relative;max-width:720px}
pre.cmd .c{color:#8A97A5}
.cmd-wrap{position:relative;max-width:720px}
.copy{position:absolute;top:8px;right:8px;font:inherit;font-size:.75rem;background:rgba(255,255,255,.08);color:var(--code-ink);border:1px solid rgba(255,255,255,.18);padding:3px 9px;border-radius:999px;cursor:pointer}
.copy:hover{background:rgba(255,255,255,.16)}

.chat{max-width:720px;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;font-size:.93rem}
.chat__bar{background:var(--panel);padding:8px 14px;font-family:var(--font-mono);font-size:.78rem;color:var(--muted);border-bottom:1px solid var(--line)}
.chat__body{display:flex;flex-direction:column;gap:12px;padding:16px}
.msg{display:grid;grid-template-columns:44px minmax(0,1fr);gap:12px;align-items:start}
.msg .who{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding-top:4px;font-family:var(--font-mono)}
.msg .bubble{background:var(--panel);padding:10px 14px;border-radius:var(--radius);white-space:pre-wrap}
.msg--me .bubble{background:var(--accent-soft);font-family:var(--font-mono);font-size:.88rem}

.role-tabs{display:flex;gap:8px;flex-wrap:wrap}
.role-tab{font:inherit;border:1px solid var(--line);background:var(--paper);color:var(--ink);padding:8px 14px;border-radius:999px;cursor:pointer;display:flex;flex-direction:column;align-items:flex-start;gap:0;line-height:1.3;text-align:left}
.role-tab small{color:var(--muted);font-size:.75rem}
.role-tab[aria-selected="true"]{border-color:var(--rc);background:var(--rs)}
.role-tab[aria-selected="true"] b{color:var(--rc)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.card{border:1px solid var(--line);border-radius:var(--radius);background:var(--paper);display:flex;flex-direction:column;box-shadow:var(--shadow)}
.card__head{padding:14px 16px 10px;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:4px}
.card__head .cmdname{font-family:var(--font-mono);color:var(--rc);font-weight:600;font-size:1.05rem}
.card__head h3{font-family:var(--font-body);font-weight:600;font-size:1rem}
.card__body{padding:12px 16px 14px;display:flex;flex-direction:column;gap:10px;font-size:.92rem;flex:1}
.card__body p{margin:0;color:var(--muted)}
.flow{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:.8rem}
.flow span{background:var(--rs);color:var(--rc);padding:2px 8px;border-radius:3px;white-space:nowrap}
.flow i{color:var(--muted);font-style:normal}
.ex{display:flex;flex-direction:column;gap:6px;margin-top:auto}
.ex .eyebrow{font-size:.68rem}
.exline{display:flex;gap:8px;align-items:flex-start;background:var(--panel);border-radius:3px;padding:6px 8px 6px 10px;font-family:var(--font-mono);font-size:.8rem;line-height:1.45}
.exline span{flex:1;min-width:0;word-break:break-all}
.exline button{font:inherit;font-size:.7rem;border:1px solid var(--line);background:var(--paper);color:var(--muted);padding:1px 7px;border-radius:999px;cursor:pointer;white-space:nowrap}
.exline button:hover{color:var(--ink);border-color:var(--accent)}
.uses{font-size:.8rem;color:var(--muted)}

.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius)}
table{border-collapse:collapse;width:100%;font-size:.9rem;min-width:640px}
th{text-align:left;font-weight:600;font-size:.78rem;letter-spacing:.06em;color:var(--muted);background:var(--panel);padding:10px 12px;border-bottom:1px solid var(--line)}
td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
td.div{font-weight:600;white-space:nowrap}
td .nm{font-family:var(--font-mono);font-size:.8rem;color:var(--muted)}
td .ask{font-size:.82rem;color:var(--muted);display:flex;gap:8px;align-items:flex-start}
td .ask button{font:inherit;font-size:.7rem;border:1px solid var(--line);background:var(--paper);color:var(--muted);padding:0 7px;border-radius:999px;cursor:pointer;white-space:nowrap}
td .ask button:hover{color:var(--ink);border-color:var(--accent)}

.faq{display:flex;flex-direction:column;gap:0;max-width:760px;border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;padding:14px 4px;font-weight:600;list-style:none;display:flex;gap:12px;align-items:baseline}
.faq summary::-webkit-details-marker{display:none}
.faq summary::before{content:"Q";font-family:var(--font-mono);color:var(--seal);font-weight:500}
.faq details[open] summary{color:var(--accent-ink)}
.faq .a{padding:0 4px 16px 30px;color:var(--muted);font-size:.95rem}
.faq .a p{margin:0 0 .6em}

footer{max-width:1180px;margin:0 auto;padding:24px;border-top:1px solid var(--line);color:var(--muted);font-size:.85rem;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:var(--ink);color:var(--paper);padding:8px 16px;border-radius:999px;font-size:.85rem;opacity:0;transition:opacity .2s;pointer-events:none}
.toast.show{opacity:1}
@media (max-width:860px){
  .layout{grid-template-columns:1fr;gap:28px;padding:24px 16px 60px}
  .toc{position:static;flex-direction:row;flex-wrap:wrap;gap:6px}
  .toc .eyebrow{width:100%}
  .toc a{border-left:0;border:1px solid var(--line);border-radius:999px;padding:4px 10px}
  .facts{grid-template-columns:1fr 1fr 1fr}
  .brand h1{font-size:1.7rem}
  .doc-meta{align-items:flex-start}
}
@media (max-width:480px){.facts{grid-template-columns:1fr}.cards{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
  var root=document.documentElement;
  try{var t=localStorage.getItem('nxt-guide-theme'); if(t) root.setAttribute('data-theme',t);}catch(e){}
  var tb=document.getElementById('theme-btn');
  function label(){var cur=root.getAttribute('data-theme'); tb.textContent = cur==='dark'?'☀ 밝게':(cur==='light'?'◐ 시스템':'☾ 어둡게');}
  tb.addEventListener('click',function(){
    var cur=root.getAttribute('data-theme'); var next = !cur?'dark':(cur==='dark'?'light':null);
    if(next) root.setAttribute('data-theme',next); else root.removeAttribute('data-theme');
    try{ next?localStorage.setItem('nxt-guide-theme',next):localStorage.removeItem('nxt-guide-theme'); }catch(e){}
    label();
  }); label();

  document.querySelectorAll('[data-tabs]').forEach(function(group){
    var tabs=group.querySelectorAll('[role="tab"]');
    tabs.forEach(function(tab){ tab.addEventListener('click',function(){
      tabs.forEach(function(t){ t.setAttribute('aria-selected','false'); var p=document.getElementById(t.getAttribute('aria-controls')); if(p) p.hidden=true; });
      tab.setAttribute('aria-selected','true'); var p=document.getElementById(tab.getAttribute('aria-controls')); if(p) p.hidden=false;
    });});
  });

  var toast=document.getElementById('toast'), timer;
  function show(msg){ toast.textContent=msg; toast.classList.add('show'); clearTimeout(timer); timer=setTimeout(function(){toast.classList.remove('show')},1400); }
  document.addEventListener('click',function(ev){
    var b=ev.target.closest('[data-copy]'); if(!b) return;
    var text=b.getAttribute('data-copy');
    if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(text).then(function(){show('복사했습니다')},function(){show('복사 실패 — 직접 선택해 복사하세요')}); }
    else { show('이 브라우저에서는 자동 복사가 안 됩니다'); }
  });

  var links=document.querySelectorAll('.toc a'), secs=[];
  links.forEach(function(a){ var s=document.querySelector(a.getAttribute('href')); if(s) secs.push([s,a]); });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ links.forEach(function(l){l.classList.remove('is-active')}); secs.forEach(function(p){ if(p[0]===en.target) p[1].classList.add('is-active'); }); } }); },{rootMargin:'-20% 0px -70% 0px'});
    secs.forEach(function(p){ io.observe(p[0]); });
  }
})();
"""

def copy_btn(text, label='복사', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<button type="button"{c} data-copy="{e(text)}">{label}</button>'

def role_cards(role):
    out = []
    for s in [x for x in data['skills'] if x['role'] == role]:
        flow = ' <i>→</i> '.join(f'<span>{e(st)}</span>' for st in s['steps'])
        exs = ''.join(f'<div class="exline"><span>{e(x)}</span>{copy_btn(x)}</div>' for x in s['examples'][:2])
        uses = ' · '.join(agent_title.get(a, a) for a in s['agents'])
        out.append(f'''
<article class="card">
  <div class="card__head"><div class="cmdname">/{e(s["name"])}</div><h3>{e(s["title"])}</h3></div>
  <div class="card__body">
    <p>{e(s["desc"].split(". ")[0].rstrip("."))}.</p>
    <div class="flow">{flow}</div>
    <div class="uses">함께 일하는 전문가: {e(uses)}</div>
    <div class="ex"><div class="eyebrow">이렇게 시작하세요</div>{exs}</div>
  </div>
</article>''')
    return ''.join(out)

role_tabs = ''.join(
    f'<button class="role-tab" role="tab" id="rt-{ROLE_KEY[r]}" aria-controls="rp-{ROLE_KEY[r]}" aria-selected="{"true" if i==0 else "false"}" style="--rc:var(--r-{ROLE_KEY[r]});--rs:var(--r-{ROLE_KEY[r]}-soft)"><b>{e(r)}</b><small>{e(ROLE_WHO[r])}</small></button>'
    for i, r in enumerate(ROLES))
role_panels = ''.join(
    f'<div class="panel" id="rp-{ROLE_KEY[r]}" role="tabpanel" aria-labelledby="rt-{ROLE_KEY[r]}" style="--rc:var(--r-{ROLE_KEY[r]});--rs:var(--r-{ROLE_KEY[r]}-soft)"{"" if i==0 else " hidden"}><div class="cards">{role_cards(r)}</div></div>'
    for i, r in enumerate(ROLES))

rows = []
for div in DIV_ORDER:
    for a in [x for x in data['agents'] if x['division'] == div]:
        when = a['desc'].split('. ')[-1].replace('사용.', '').rstrip('. ')
        ask = f'<div class="ask"><span>{e(a["example"])}</span>{copy_btn(a["example"])}</div>' if a['example'] else ''
        rows.append(f'<tr><td class="div">{e(div)}</td><td>{e(a["emoji"])} <b>{e(a["title"])}</b><br><span class="nm">{e(a["name"])}</span></td><td>{e(when)}</td><td>{ask}</td></tr>')
agent_table = ''.join(rows)

n_sk, n_ag = len(data['skills']), len(data['agents'])

BODY = f'''
<header class="masthead">
  <div class="masthead__in">
    <div class="brand">
      <div class="eyebrow">nxt-agency · 사용 안내</div>
      <h1>대학·공공기관 AI 업무 도우미</h1>
      <div class="sub">명령 하나로 업무 하나를 끝내는 한국어 워크플로우. 터미널이 낯선 분도 이 안내서만 보고 시작할 수 있습니다.</div>
    </div>
    <div class="doc-meta">
      <div class="stamp">사용<br>안내</div>
      <div>2026.09 · v0.1</div>
      <button class="theme-btn" id="theme-btn" type="button">☾ 어둡게</button>
    </div>
  </div>
</header>

<div class="layout">
<nav class="toc" aria-label="목차">
  <div class="eyebrow">목차</div>
  <a href="#s1"><b>1</b>무엇인가</a>
  <a href="#s2"><b>2</b>설치하기</a>
  <a href="#s3"><b>3</b>첫 명령 실행</a>
  <a href="#s4"><b>4</b>내 일에 맞는 명령</a>
  <a href="#s5"><b>5</b>전문가 직접 부르기</a>
  <a href="#s6"><b>6</b>자주 묻는 질문</a>
  <a href="#s7"><b>7</b>문제 해결</a>
</nav>

<main>
<section id="s1">
  <div class="sec-head"><div class="num">01</div><h2>무엇인가</h2></div>
  <div class="prose">
    <p>nxt-agency는 사업단·행정·교수·학생이 자주 하는 업무를 <b>슬래시 명령 하나</b>로 처리하게 해 주는 AI 도우미 묶음입니다. 예를 들어 <code>/meeting-minutes</code>를 치고 녹취록을 붙여 넣으면 결재용 회의록이 나옵니다.</p>
    <p>명령 하나는 여러 <b>전문가</b>를 순서대로 부릅니다. 사업계획서 명령은 동향 조사원, 제안서 작성가, 예산 관리자, 규정 검토관, 보고서 요약가를 차례로 거칩니다. 사용자는 순서를 몰라도 됩니다. 명령이 두세 가지만 묻고 알아서 진행합니다.</p>
    <p>모든 안내와 결과는 한국어이고, 법령·서식·용어는 한국 대학과 공공기관 기준입니다.</p>
  </div>
  <div class="facts">
    <div class="fact"><b>{n_sk}</b><span>직업군 명령(스킬)</span></div>
    <div class="fact"><b>{n_ag}</b><span>전문가 에이전트</span></div>
    <div class="fact"><b>3</b><span>쓸 수 있는 곳 · Claude Code, claude.ai, Kiro</span></div>
  </div>
</section>

<section id="s2">
  <div class="sec-head"><div class="num">02</div><h2>설치하기</h2></div>
  <div class="prose"><p>쓰는 도구를 고르세요. 회사에서 계정을 받았다면 그 도구가 맞습니다. 터미널이 없거나 낯설면 <b>claude.ai 웹</b>이 가장 쉽습니다.</p></div>
  <div data-tabs>
    <div class="tabs" role="tablist">
      <button class="tab" role="tab" id="it-cc" aria-controls="ip-cc" aria-selected="true">Claude Code</button>
      <button class="tab" role="tab" id="it-web" aria-controls="ip-web" aria-selected="false">claude.ai 웹</button>
      <button class="tab" role="tab" id="it-kiro" aria-controls="ip-kiro" aria-selected="false">AWS Kiro</button>
    </div>
    <div class="panel" id="ip-cc" role="tabpanel" aria-labelledby="it-cc">
      <div class="step-list">
        <div class="step"><div><h4>준비물</h4><p>Claude Code가 설치되어 있고 로그인이 되어 있어야 합니다. 터미널에서 <code>claude</code>를 쳤을 때 실행되면 됩니다.</p></div></div>
        <div class="step"><div><h4>레포를 받아 설치 명령 실행</h4><p>아래 세 줄을 터미널에 붙여 넣습니다. 홈 폴더의 <code>.claude</code> 아래에 명령과 전문가가 들어갑니다.</p></div></div>
        <div class="step"><div><h4>확인</h4><p>Claude Code를 새로 열고 <code>/</code>를 치면 <code>meeting-minutes</code> 같은 명령이 목록에 보입니다.</p></div></div>
      </div>
      <div class="cmd-wrap"><pre class="cmd">git clone https://github.com/nxtcloud-edu/nxt-agency.git
cd nxt-agency
./scripts/install.sh --tool claude-code</pre>{copy_btn("git clone https://github.com/nxtcloud-edu/nxt-agency.git && cd nxt-agency && ./scripts/install.sh --tool claude-code", cls="copy")}</div>
      <div class="note">내 직업군 것만 넣으려면 <code>./scripts/install.sh --role 행정</code> 처럼 씁니다. 사업단 · 행정 · 교수·연구자 · 학생 중 하나를 고르면 그 명령들과 필요한 전문가만 설치됩니다.</div>
    </div>
    <div class="panel" id="ip-web" role="tabpanel" aria-labelledby="it-web" hidden>
      <div class="step-list">
        <div class="step"><div><h4>zip 파일 받기</h4><p>담당자에게 <code>dist/skills</code> 폴더의 zip 파일을 받습니다. 명령 하나가 zip 하나입니다. 직접 만들려면 레포에서 <code>./scripts/package-skills.sh</code>를 실행합니다.</p></div></div>
        <div class="step"><div><h4>claude.ai에 올리기</h4><p>claude.ai 접속 → 설정 → 기능(Capabilities) → 스킬 → <b>스킬 추가</b> → zip 선택. 필요한 명령만 골라 올리면 됩니다.</p></div></div>
        <div class="step"><div><h4>확인</h4><p>새 대화에서 <code>/meeting-minutes</code>라고 치거나, 그냥 "회의록 만들어줘"라고 말해도 알아서 해당 스킬을 씁니다.</p></div></div>
      </div>
      <div class="note">웹에는 전문가 에이전트가 따로 없지만, 각 명령 안에 전문가의 핵심 규칙과 서식이 들어 있어 혼자서도 같은 결과를 냅니다.</div>
    </div>
    <div class="panel" id="ip-kiro" role="tabpanel" aria-labelledby="it-kiro" hidden>
      <div class="step-list">
        <div class="step"><div><h4>준비물</h4><p>회사에서 받은 Kiro 계정으로 Kiro IDE 또는 Kiro CLI에 로그인되어 있어야 합니다. 홈 폴더에 <code>.kiro</code> 폴더가 생겨 있으면 준비된 것입니다.</p></div></div>
        <div class="step"><div><h4>설치 명령 실행</h4><p>같은 설치 스크립트에 <code>--tool kiro</code>를 붙입니다. 명령은 그대로 들어가고, 전문가는 Kiro의 커스텀 에이전트 형식으로 바뀌어 들어갑니다.</p></div></div>
        <div class="step"><div><h4>확인</h4><p>Kiro 채팅에서 <code>/meeting-minutes</code>를 치면 스킬이 실행됩니다. 전문가는 <code>/agent</code>로 전환해 고를 수 있습니다.</p></div></div>
      </div>
      <div class="cmd-wrap"><pre class="cmd">git clone https://github.com/nxtcloud-edu/nxt-agency.git
cd nxt-agency
./scripts/install.sh --tool kiro</pre>{copy_btn("git clone https://github.com/nxtcloud-edu/nxt-agency.git && cd nxt-agency && ./scripts/install.sh --tool kiro", cls="copy")}</div>
      <div class="note note--warn">Kiro는 버전에 따라 에이전트 형식이 바뀐 적이 있습니다. 명령은 보이는데 전문가가 안 보이면 담당자에게 알려 주세요. 명령만으로도 업무는 끝낼 수 있습니다.</div>
    </div>
  </div>
</section>

<section id="s3">
  <div class="sec-head"><div class="num">03</div><h2>첫 명령 실행</h2></div>
  <div class="prose"><p>가장 많이 쓰는 회의록 명령으로 흐름을 보겠습니다. 명령 뒤에 상황을 한 줄 적고, 그다음 자료를 붙여 넣으면 됩니다. 단계가 끝날 때마다 한 번 확인을 묻고, "끝까지"라고 하면 멈추지 않고 진행합니다.</p></div>
  <div class="chat">
    <div class="chat__bar">Claude Code · 예시 대화</div>
    <div class="chat__body">
      <div class="msg msg--me"><div class="who">나</div><div class="bubble">/meeting-minutes 사업단 운영위원회 회의록, 결재용</div></div>
      <div class="msg"><div class="who">AI</div><div class="bubble">회의록을 만들기 전에 두 가지만 확인하겠습니다.
1. 회의 자료(녹취록·메모)를 붙여 넣어 주세요.
2. 일시·장소·참석자 중 자료에 없는 것이 있으면 알려 주세요. (없으면 "확인 필요"로 표시합니다)</div></div>
      <div class="msg msg--me"><div class="who">나</div><div class="bubble">(녹취록 붙여 넣기) 일시는 9월 12일 14시, 회의실 301호.</div></div>
      <div class="msg"><div class="who">AI</div><div class="bubble">1단계. 자료에서 안건 3건, 결정사항 4건, 조치사항 5건을 찾았습니다. 담당자가 없는 조치사항 1건은 "담당 미정"으로 두었습니다.
여기까지 확인하시겠어요? 아니면 끝까지 진행할까요?</div></div>
      <div class="msg msg--me"><div class="who">나</div><div class="bubble">끝까지</div></div>
      <div class="msg"><div class="who">AI</div><div class="bubble">2단계. 회의 개요 · 안건 · 논의내용 · 결정사항 · 조치사항(담당/기한) · 미결사항 순서로 회의록을 정리했습니다.
3단계. 결재란이 포함된 DOCX 파일로 저장했습니다: 운영위원회_회의록_0912.docx</div></div>
    </div>
  </div>
  <div class="note">무엇을 써야 할지 모르겠으면 안내 데스크에게 물어보세요. 상황을 말하면 맞는 명령과 뒤에 붙일 말까지 만들어 줍니다.<br><code>안내 데스크, 나는 사업단 행정 담당인데 연차평가 성과보고서를 처음 써야 해. 어디부터 시작하면 돼?</code></div>
</section>

<section id="s4">
  <div class="sec-head"><div class="num">04</div><h2>내 일에 맞는 명령</h2></div>
  <div class="prose"><p>직업군을 고르면 그 일에 맞는 명령이 나옵니다. 예시 문장은 복사해서 그대로 쓰고, 괄호 안 내용만 내 상황으로 바꾸면 됩니다.</p></div>
  <div data-tabs>
    <div class="role-tabs" role="tablist">{role_tabs}</div>
    {role_panels}
  </div>
</section>

<section id="s5">
  <div class="sec-head"><div class="num">05</div><h2>전문가 직접 부르기</h2></div>
  <div class="prose"><p>명령에 없는 일이거나 한 단계만 다시 하고 싶을 때는 전문가를 이름으로 부릅니다. "통계·연구설계 전문가로, …" 처럼 한글 이름을 앞에 붙이면 됩니다. Claude Code에서는 <code>@이름</code>으로도 부를 수 있습니다.</p></div>
  <div class="tbl-wrap"><table>
    <thead><tr><th>분야</th><th>전문가</th><th>이럴 때</th><th>예시 요청</th></tr></thead>
    <tbody>{agent_table}</tbody>
  </table></div>
</section>

<section id="s6">
  <div class="sec-head"><div class="num">06</div><h2>자주 묻는 질문</h2></div>
  <div class="faq">
    <details><summary>한글로 <code>/회의록</code>이라고 치면 안 되나요?</summary><div class="a"><p>안 됩니다. Claude Code와 Kiro 모두 명령 이름은 영문만 허용합니다. 대신 <code>/</code>만 치면 목록이 뜨고, 웹에서는 "회의록 만들어줘"처럼 말로 해도 맞는 스킬을 찾아 씁니다.</p></div></details>
    <details><summary>결과에 나온 법령·수치를 그대로 써도 되나요?</summary><div class="a"><p>확인 후에 쓰세요. 전문가들은 법령 조항 번호처럼 확실하지 않은 사실은 쓰지 않도록 만들어져 있지만, AI는 틀릴 수 있습니다. 규정·법령 검토관과 개인정보보호 담당관의 결과는 법률 자문이 아니며, 최종 판단은 법무·감사 부서와 확인해야 합니다.</p></div></details>
    <details><summary>학생 명단이나 연락처를 붙여 넣어도 되나요?</summary><div class="a"><p>가급적 넣지 마세요. 이름·학번·연락처·주민번호는 지운 뒤 붙여 넣고, 필요하면 "A학생"처럼 바꿔 쓰세요. 민원 답변 명령은 답변에 개인정보가 들어가지 않도록 점검하지만, 입력 단계에서 빼는 것이 가장 안전합니다.</p></div></details>
    <details><summary>한글(HWP) 파일로 받을 수 있나요?</summary><div class="a"><p>바로는 어렵습니다. 문서 생성기는 DOCX·PPTX·XLSX·PDF를 만듭니다. DOCX로 받은 뒤 한컴오피스에서 열어 HWP로 저장하면 됩니다. 서식이 어긋나면 표 부분만 다시 잡아 주세요.</p></div></details>
    <details><summary>웹에서 쓰는데 "전문가가 없다"고 나옵니다.</summary><div class="a"><p>정상입니다. claude.ai 웹에는 전문가 에이전트를 따로 설치할 수 없어, 각 명령이 전문가의 규칙과 서식을 안에 품고 혼자 동작합니다. 결과 품질은 같습니다.</p></div></details>
    <details><summary>명령을 몇 개만 골라 쓰고 싶어요.</summary><div class="a"><p>설치할 때 <code>--role 학생</code>(직업군) 또는 <code>--skill cover-letter</code>(명령 하나)를 붙이면 그것과 거기에 필요한 전문가만 들어갑니다. 웹은 zip을 골라 올리면 됩니다.</p></div></details>
  </div>
</section>

<section id="s7">
  <div class="sec-head"><div class="num">07</div><h2>문제 해결</h2></div>
  <div class="step-list">
    <div class="step"><div><h4>명령이 목록에 안 보여요</h4><p>도구를 완전히 닫고 다시 여세요. 그래도 없으면 설치 위치를 확인합니다: Claude Code는 <code>~/.claude/skills</code>, Kiro는 <code>~/.kiro/skills</code> 아래에 명령 이름 폴더가 있어야 합니다.</p></div></div>
    <div class="step"><div><h4>설치 스크립트가 "선택된 항목이 없습니다"라고 해요</h4><p><code>--role</code>이나 <code>--skill</code> 뒤의 이름이 틀린 경우입니다. <code>./scripts/install.sh --list</code>로 정확한 이름을 확인하세요. 직업군은 사업단 · 행정 · 교수·연구자 · 학생 네 가지입니다.</p></div></div>
    <div class="step"><div><h4>최신 버전으로 바꾸고 싶어요</h4><p>레포 폴더에서 <code>git pull</code> 후 설치 명령을 다시 실행하면 덮어씁니다. 지우려면 <code>./scripts/install.sh --uninstall</code>. 이 레포에서 설치한 것만 지우고 다른 파일은 건드리지 않습니다.</p></div></div>
    <div class="step"><div><h4>결과가 이상해요</h4><p>대부분 입력 자료가 부족한 경우입니다. 명령이 물어본 질문에 답을 채우고, 자료를 더 붙여 넣어 보세요. 그래도 이상하면 담당자에게 어떤 명령에 무엇을 넣었는지 알려 주세요.</p></div></div>
  </div>
</section>
</main>
</div>

<footer>
  <div>nxt-agency · NXT Cloud · MIT 라이선스. 전문가 원본은 msitarzewski/agency-agents(MIT).</div>
  <div>문의: glen.lee@nxtcloud.kr</div>
</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>{JS}</script>
'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700;800&family=IBM+Plex+Sans+KR:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'

full = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>nxt-agency 사용 안내</title>
{FONTS}
<style>{CSS}</style>
</head>
<body>{BODY}</body>
</html>
'''
(ROOT / 'docs' / 'guide.html').write_text(full)

artifact = f'''<title>nxt-agency 사용 안내</title>
{FONTS}
<style>{CSS}</style>
{BODY}'''
if '--artifact' in sys.argv:
    pathlib.Path(sys.argv[sys.argv.index('--artifact') + 1]).write_text(artifact)
print('docs/guide.html', len(full), 'bytes')
