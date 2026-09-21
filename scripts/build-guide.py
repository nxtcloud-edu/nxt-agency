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

CSS = (pathlib.Path(__file__).resolve().parent / 'guide_theme.css').read_text()

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

  var boxes=Array.prototype.slice.call(document.querySelectorAll('.check input')), saved={};
  try{ saved=JSON.parse(localStorage.getItem('nxt-guide-demo')||'{}'); }catch(e){}
  boxes.forEach(function(b){ if(saved[b.id]) b.checked=true; b.addEventListener('change',function(){ saved[b.id]=b.checked; try{localStorage.setItem('nxt-guide-demo',JSON.stringify(saved));}catch(e){} }); });

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
  <a href="#s3"><b>3</b>샘플로 체험하기</a>
  <a href="#s4"><b>4</b>첫 명령 실행</a>
  <a href="#s5"><b>5</b>내 일에 맞는 명령</a>
  <a href="#s6"><b>6</b>전문가 직접 부르기</a>
  <a href="#s7"><b>7</b>자주 묻는 질문</a>
  <a href="#s8"><b>8</b>문제 해결</a>
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
    <div class="fact"><b>3</b><span>설치 지원 도구 · Claude Code, Codex, Kiro</span></div>
  </div>
</section>

<section id="s2">
  <div class="sec-head"><div class="num">02</div><h2>설치하기</h2></div>
  <div class="prose"><p>쓰는 도구를 고르세요. 회사에서 계정을 받았다면 그 도구가 맞습니다. 세 도구 모두 설치 명령 한 줄이면 됩니다. 이 밖의 도구도 쓸 수 있으며 아래에 설명합니다.</p></div>
  <div data-tabs>
    <div class="tabs" role="tablist">
      <button class="tab" role="tab" id="it-cc" aria-controls="ip-cc" aria-selected="true">Claude Code</button>
      <button class="tab" role="tab" id="it-codex" aria-controls="ip-codex" aria-selected="false">Codex</button>
      <button class="tab" role="tab" id="it-kiro" aria-controls="ip-kiro" aria-selected="false">AWS Kiro</button>
    </div>
    <div class="panel" id="ip-cc" role="tabpanel" aria-labelledby="it-cc">
      <div class="step-list">
        <div class="step"><div><h4>준비물</h4><p>Claude Code가 설치되어 있고 로그인이 되어 있어야 합니다. 터미널에서 <code>claude</code>를 쳤을 때 실행되면 됩니다.</p></div></div>
        <div class="step"><div><h4>레포를 받아 설치 명령 실행</h4><p>아래 세 줄을 터미널에 붙여 넣습니다. 홈 폴더의 <code>.claude</code> 아래에 명령과 전문가가 들어갑니다.</p></div></div>
        <div class="step"><div><h4>확인</h4><p>Claude Code를 새로 열고 <code>/</code>를 치면 <code>meeting-minutes</code> 같은 명령이 목록에 보입니다. 플러그인으로 넣었다면 <code>nxt-agency:meeting-minutes</code>로 보입니다.</p></div></div>
      </div>
      <div class="cmd-wrap"><pre class="cmd">git clone https://github.com/nxtcloud-edu/nxt-agency.git
cd nxt-agency
./scripts/install.sh --tool claude-code</pre>{copy_btn("git clone https://github.com/nxtcloud-edu/nxt-agency.git && cd nxt-agency && ./scripts/install.sh --tool claude-code", cls="copy")}</div>
      <div class="note">내 직업군 것만 넣으려면 <code>./scripts/install.sh --role admin</code> 처럼 씁니다. 직업군은 네 가지입니다: <code>project</code>(사업단), <code>admin</code>(행정), <code>research</code>(교수·연구자), <code>student</code>(학생). 고른 직업군의 명령과 거기에 필요한 전문가만 설치됩니다.</div>
      <h4 class="alt-head">또는 플러그인으로 (레포를 받지 않고)</h4>
      <div class="prose"><p>Claude Code 안에서 아래 두 줄을 차례로 치면 명령과 전문가가 한 번에 들어가고, 업데이트도 Claude Code가 알아서 합니다. 대신 이름 앞에 <code>nxt-agency:</code>가 붙어 <code>/nxt-agency:meeting-minutes</code>처럼 부릅니다. "회의록 만들어줘"처럼 말로 하면 접두어 없이도 알아서 찾습니다.</p></div>
      <div class="cmd-wrap"><pre class="cmd">/plugin marketplace add nxtcloud-edu/nxt-agency
/plugin install nxt-agency@nxt-agency</pre>{copy_btn("/plugin marketplace add nxtcloud-edu/nxt-agency", cls="copy")}</div>
      <div class="note note--warn">설치 스크립트와 플러그인을 같이 쓰면 같은 명령이 두 벌 보입니다. 한쪽만 쓰세요. 플러그인을 지우려면 <code>/plugin uninstall nxt-agency@nxt-agency</code>.</div>
    </div>
    <div class="panel" id="ip-codex" role="tabpanel" aria-labelledby="it-codex" hidden>
      <div class="step-list">
        <div class="step"><div><h4>준비물</h4><p>Codex CLI 또는 Codex 앱이 설치되어 있고 로그인이 되어 있어야 합니다. 홈 폴더에 <code>.codex</code> 폴더가 있으면 준비된 것입니다.</p></div></div>
        <div class="step"><div><h4>설치 명령 실행</h4><p>같은 설치 스크립트에 <code>--tool codex</code>를 붙입니다. 명령은 <code>~/.codex/skills</code>에 그대로 들어가고, 전문가는 Codex 커스텀 에이전트 형식(TOML)으로 바뀌어 <code>~/.codex/agents</code>에 들어갑니다.</p></div></div>
        <div class="step"><div><h4>확인</h4><p>Codex에서 <code>/skills</code>를 치면 명령 목록이 보이고, <code>$meeting-minutes</code>처럼 <code>$</code>를 붙여 부릅니다. 전문가를 서브에이전트로 쓰려면 Codex 설정에서 멀티에이전트 기능을 켜야 합니다.</p></div></div>
      </div>
      <div class="cmd-wrap"><pre class="cmd">git clone https://github.com/nxtcloud-edu/nxt-agency.git
cd nxt-agency
./scripts/install.sh --tool codex</pre>{copy_btn("git clone https://github.com/nxtcloud-edu/nxt-agency.git && cd nxt-agency && ./scripts/install.sh --tool codex", cls="copy")}</div>
      <div class="note">Codex는 명령을 <code>/</code>가 아니라 <code>$</code>로 부릅니다. <code>/meeting-minutes</code> 대신 <code>$meeting-minutes</code>라고 치세요.</div>
    </div>
    <div class="panel" id="ip-kiro" role="tabpanel" aria-labelledby="it-kiro" hidden>
      <div class="step-list">
        <div class="step"><div><h4>준비물</h4><p>회사에서 받은 Kiro 계정으로 Kiro IDE 또는 Kiro CLI에 로그인되어 있어야 합니다. 홈 폴더에 <code>.kiro</code> 폴더가 생겨 있으면 준비된 것입니다.</p></div></div>
        <div class="step"><div><h4>설치 명령 실행</h4><p>같은 설치 스크립트에 <code>--tool kiro</code>를 붙입니다. 명령은 그대로 들어가고, 전문가는 Kiro 커스텀 에이전트 JSON으로 바뀌어 <code>~/.kiro/agents</code>에 들어갑니다. Kiro CLI와 Kiro IDE가 같은 폴더를 읽습니다.</p></div></div>
        <div class="step"><div><h4>확인</h4><p>Kiro 채팅에서 <code>/meeting-minutes</code>를 치면 스킬이 실행됩니다. 전문가는 <code>kiro-cli chat --agent statistician</code>처럼 시작하거나 대화 중 <code>/agent</code>로 전환합니다.</p></div></div>
      </div>
      <div class="cmd-wrap"><pre class="cmd">git clone https://github.com/nxtcloud-edu/nxt-agency.git
cd nxt-agency
./scripts/install.sh --tool kiro</pre>{copy_btn("git clone https://github.com/nxtcloud-edu/nxt-agency.git && cd nxt-agency && ./scripts/install.sh --tool kiro", cls="copy")}</div>
      <div class="note note--warn">Kiro는 버전에 따라 에이전트 형식이 바뀐 적이 있습니다. 명령은 보이는데 전문가가 안 보이면 담당자에게 알려 주세요. 명령만으로도 업무는 끝낼 수 있습니다.</div>
    </div>
  </div>
  <div class="prose"><p><b>그 밖의 도구.</b> 명령은 Agent Skills 표준 형식이라 이를 지원하는 다른 도구에서도 쓸 수 있습니다. 예를 들어 claude.ai 웹은 설정 → 기능 → 스킬에서 zip을 올리면 되고, 다른 CLI는 스킬 폴더를 복사하면 됩니다. zip은 레포에서 <code>./scripts/package-skills.sh</code>로 만듭니다. 명령 안에 전문가의 규칙과 서식이 들어 있어 전문가 없이도 같은 결과를 냅니다.</p></div>
</section>

<section id="s3">
  <div class="sec-head"><div class="num">03</div><h2>샘플로 체험하기 · 데모 핸즈온</h2></div>
  <div class="prose"><p>자기 자료를 넣기 부담스럽거나 무엇을 넣어야 할지 모르겠다면 여기서 시작하세요. 15분이면 명령 하나를 끝까지 경험할 수 있습니다. 모든 샘플은 가상 대학(넥클대학교)과 가상 인물의 자료입니다. 체크한 항목은 이 브라우저에 저장됩니다.</p></div>
  <div class="step-list">
    <div class="step"><div><h4>준비 확인 <span class="time-tag">1분</span></h4><p><code>/</code>(Codex는 <code>$</code>)를 쳤을 때 목록에 <code>nxt-demo</code>가 보이면 준비된 것입니다. 안 보이면 <a href="#s2">설치하기</a>로.</p>
      <ul class="check"><li><input type="checkbox" id="d-0"><label for="d-0">명령 목록에 nxt-demo가 보인다</label></li></ul></div></div>
    <div class="step"><div><h4>체험 명령 실행 <span class="time-tag">2분</span></h4><p>아래 한 줄을 치면 직업군별로 할 수 있는 일을 표로 보여 주고 하나를 고르게 합니다. 처음에는 <b>회의록</b>을 권합니다. 결과가 가장 직관적입니다.</p>
      <div class="cmd-wrap"><pre class="cmd">/nxt-demo 회의록 샘플로 해 보자</pre>{copy_btn("/nxt-demo 회의록 샘플로 해 보자", cls="copy")}</div>
      <ul class="check"><li><input type="checkbox" id="d-1"><label for="d-1">메뉴 표가 나오고 "자료 소개"(무슨 회의인지, 안건 3개에서 무엇이 오갔는지, 함정 2~3개)를 받았다. 이 소개가 있어야 결과를 평가할 수 있다</label></li></ul></div></div>
    <div class="step"><div><h4>끝까지 진행하고 함정을 확인 <span class="time-tag">5분</span></h4><p>"시작할까요?"에 "네"라고 하면 회의록 정리원의 절차대로 진행합니다. 결과 아래 "이렇게 처리했습니다" 설명과 함께 다음 세 가지를 찾아보세요.</p>
      <ul class="check">
        <li><input type="checkbox" id="d-2"><label for="d-2">결정사항에는 참여기업 선정 의결만 있고, 이월·전용과 고교 캠프 예산은 미결사항으로 분리됐다</label></li>
        <li><input type="checkbox" id="d-3"><label for="d-3">조치사항 표에서 동의서 양식 담당은 "미지정", 다음 회의 일자는 "미정"으로 남았다 (지어내지 않음)</label></li>
        <li><input type="checkbox" id="d-4"><label for="d-4">복사기 잡담은 회의록에 들어가지 않았다</label></li>
      </ul></div></div>
    <div class="step"><div><h4>"내 자료로 하려면" 읽기 <span class="time-tag">2분</span></h4><p>결과 끝에 실제로 칠 명령, 준비할 자료, 지워야 할 개인정보가 세 줄로 나옵니다. 이것이 다음에 내 녹취록으로 할 때의 출발점입니다.</p>
      <ul class="check"><li><input type="checkbox" id="d-5"><label for="d-5">세 줄 안내를 받았고, 내 자료 중 무엇을 붙여 넣을지 정했다</label></li></ul></div></div>
    <div class="step"><div><h4>다른 샘플 하나 더 <span class="time-tag">5분</span></h4><p>이번엔 내 직업군의 것으로. "다른 것도 해 볼까요?"에 명령 이름을 답하면 됩니다. 아래 표에서 고르세요.</p>
      <ul class="check"><li><input type="checkbox" id="d-6"><label for="d-6">내 직업군 명령 하나를 샘플로 끝까지 돌려 봤다</label></li></ul></div></div>
  </div>
  <div class="prose"><p><b>더 깊이.</b> 직업군별로 실제 업무 순서대로 명령 3~4개를 이어서 해 보는 핸즈온 시나리오가 따로 있습니다. 페르소나와 상황이 주어지고, 실습마다 확인 항목과 기대 결과가 있습니다.</p></div>
  <div class="role-links">
    <a href="handson/project.html" style="--rc:var(--r-project);--rs:var(--r-project-soft)"><b>사업단</b><span>집행 점검 → 행사 준비 → 성과보고 → 차년도 계획 · 90분</span></a>
    <a href="handson/admin.html" style="--rc:var(--r-admin);--rs:var(--r-admin-soft)"><b>행정</b><span>회의록 → 문의 답변 → 동의서 → 처장 보고 · 60분</span></a>
    <a href="handson/research.html" style="--rc:var(--r-research);--rs:var(--r-research-soft)"><b>교수·연구자</b><span>선행연구 → 연구계획서 → 강의계획서 · 75분</span></a>
    <a href="handson/student.html" style="--rc:var(--r-student);--rs:var(--r-student-soft)"><b>학생</b><span>학기 계획 → 캡스톤 → 자기소개서 · 60분</span></a>
  </div>
  <div class="prose"><p><b>샘플에 넣어 둔 함정.</b> 담당자가 정해지지 않은 조치사항, 학부모가 자녀 성적을 묻는 문의, 목표에 못 미친 지표, 부풀리고 싶은 경험 같은 것들입니다. 명령이 이런 부분을 어떻게 처리하는지 보는 것이 체험의 핵심입니다.</p></div>
  <div class="tbl-wrap"><table>
    <thead><tr><th>명령</th><th>샘플 데이터</th><th>들어 있는 함정</th></tr></thead>
    <tbody>
      <tr><td><code>/meeting-minutes</code></td><td>운영위원회 녹취록</td><td>결정과 논의가 섞임, 담당·기한 없는 조치사항, 일시·장소 누락</td></tr>
      <tr><td><code>/report-summary</code></td><td>중간평가 자체보고서 요약본</td><td>수치가 많아 무엇을 남길지 골라야 함</td></tr>
      <tr><td><code>/inquiry-reply</code></td><td>문의·민원 4건</td><td>학부모의 자녀 성적 문의, 감정적 공정성 민원</td></tr>
      <tr><td><code>/consent-form</code></td><td>재학생 설문 계획</td><td>불필요한 수집 항목, 보관 기간 미정, 외부 제공</td></tr>
      <tr><td><code>/business-plan</code></td><td>공고 요강 발췌 + 사업단 현황</td><td>평가지표에 맞춰 강점·약점을 배치해야 함</td></tr>
      <tr><td><code>/performance-report</code></td><td>KPI 실적표 + 만족도</td><td>미달 지표의 원인과 개선 방향</td></tr>
      <tr><td><code>/event-prep</code></td><td>성과발표회 개요</td><td>담당자·예산이 미정인 항목</td></tr>
      <tr><td><code>/budget-check</code></td><td>세목별 집행 현황</td><td>집행 부진과 과집행, 미증빙 카드 건</td></tr>
      <tr><td><code>/literature-review</code></td><td>주제 메모 + 가상 문헌 10편</td><td>설계 수준이 제각각, 같은 데이터를 재사용한 논문</td></tr>
      <tr><td><code>/research-proposal</code></td><td>공고 발췌 + 연구자 프로필</td><td>배점표에 맞춘 계획서 구성</td></tr>
      <tr><td><code>/syllabus</code></td><td>과목 개요 + 지난 강의평가</td><td>강의평가 불만을 CQI로 반영</td></tr>
      <tr><td><code>/cover-letter</code></td><td>공공기관 공고 + 경험 목록</td><td>"부풀려도 될까?" 메모가 달린 경험</td></tr>
      <tr><td><code>/semester-plan</code></td><td>학생 상황 메모</td><td>목표 대비 시간이 부족한 시간표</td></tr>
      <tr><td><code>/capstone</code></td><td>아이디어 메모</td><td>기능 12개, 발표 2주 전, 코드 없음</td></tr>
    </tbody>
  </table></div>
</section>

<section id="s4">
  <div class="sec-head"><div class="num">04</div><h2>첫 명령 실행</h2></div>
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

<section id="s5">
  <div class="sec-head"><div class="num">05</div><h2>내 일에 맞는 명령</h2></div>
  <div class="prose"><p>직업군을 고르면 그 일에 맞는 명령이 나옵니다. 예시 문장은 복사해서 그대로 쓰고, 괄호 안 내용만 내 상황으로 바꾸면 됩니다.</p></div>
  <div data-tabs>
    <div class="role-tabs" role="tablist">{role_tabs}</div>
    {role_panels}
  </div>
</section>

<section id="s6">
  <div class="sec-head"><div class="num">06</div><h2>전문가 직접 부르기</h2></div>
  <div class="prose"><p>명령에 없는 일이거나 한 단계만 다시 하고 싶을 때는 전문가를 이름으로 부릅니다. "통계·연구설계 전문가로, …" 처럼 한글 이름을 앞에 붙이면 됩니다. 도구별로 직접 지정하는 방법도 있습니다. Claude Code는 <code>@statistician</code>(플러그인 설치면 <code>@nxt-agency:statistician</code>), Codex는 <code>$statistician</code>(설정에서 멀티에이전트를 켠 경우), Kiro CLI는 <code>kiro-cli chat --agent statistician</code>으로 시작하거나 대화 중 <code>/agent</code>로 바꿉니다.</p></div>
  <div class="tbl-wrap"><table>
    <thead><tr><th>분야</th><th>전문가</th><th>이럴 때</th><th>예시 요청</th></tr></thead>
    <tbody>{agent_table}</tbody>
  </table></div>
</section>

<section id="s7">
  <div class="sec-head"><div class="num">07</div><h2>자주 묻는 질문</h2></div>
  <div class="faq">
    <details><summary>한글로 <code>/회의록</code>이라고 치면 안 되나요?</summary><div class="a"><p>안 됩니다. Claude Code, Codex, Kiro 모두 명령 이름은 영문만 허용합니다. 대신 <code>/</code>(Codex는 <code>$</code>)만 치면 목록이 뜨고, "회의록 만들어줘"처럼 말로 해도 맞는 스킬을 찾아 씁니다.</p></div></details>
    <details><summary>결과에 나온 법령·수치를 그대로 써도 되나요?</summary><div class="a"><p>확인 후에 쓰세요. 전문가들은 법령 조항 번호처럼 확실하지 않은 사실은 쓰지 않도록 만들어져 있지만, AI는 틀릴 수 있습니다. 규정·법령 검토관과 개인정보보호 담당관의 결과는 법률 자문이 아니며, 최종 판단은 법무·감사 부서와 확인해야 합니다.</p></div></details>
    <details><summary>학생 명단이나 연락처를 붙여 넣어도 되나요?</summary><div class="a"><p>가급적 넣지 마세요. 이름·학번·연락처·주민번호는 지운 뒤 붙여 넣고, 필요하면 "A학생"처럼 바꿔 쓰세요. 민원 답변 명령은 답변에 개인정보가 들어가지 않도록 점검하지만, 입력 단계에서 빼는 것이 가장 안전합니다.</p></div></details>
    <details><summary>한글(HWP) 파일로 받을 수 있나요?</summary><div class="a"><p>바로는 어렵습니다. 문서 생성기는 DOCX·PPTX·XLSX·PDF를 만듭니다. DOCX로 받은 뒤 한컴오피스에서 열어 HWP로 저장하면 됩니다. 서식이 어긋나면 표 부분만 다시 잡아 주세요.</p></div></details>
    <details><summary>다른 도구에서 쓰는데 "전문가가 없다"고 나옵니다.</summary><div class="a"><p>정상입니다. claude.ai 웹처럼 전문가 에이전트를 따로 설치할 수 없는 도구에서는 각 명령이 전문가의 규칙과 서식을 안에 품고 혼자 동작합니다. 결과 품질은 같습니다.</p></div></details>
    <details><summary>명령을 몇 개만 골라 쓰고 싶어요.</summary><div class="a"><p>설치할 때 <code>--role student</code>(직업군) 또는 <code>--skill cover-letter</code>(명령 하나)를 붙이면 그것과 거기에 필요한 전문가만 들어갑니다. 웹은 zip을 골라 올리면 됩니다.</p></div></details>
  </div>
</section>

<section id="s8">
  <div class="sec-head"><div class="num">08</div><h2>문제 해결</h2></div>
  <div class="step-list">
    <div class="step"><div><h4>명령이 목록에 안 보여요</h4><p>도구를 완전히 닫고 다시 여세요. 그래도 없으면 설치 위치를 확인합니다: Claude Code는 <code>~/.claude/skills</code>, Codex는 <code>~/.codex/skills</code>, Kiro는 <code>~/.kiro/skills</code> 아래에 명령 이름 폴더가 있어야 합니다. 플러그인으로 넣었다면 <code>/plugin list</code>에 <code>nxt-agency</code>가 있는지, 명령은 <code>/nxt-agency:</code>로 시작하는지 확인합니다.</p></div></div>
    <div class="step"><div><h4>설치 스크립트가 "선택된 항목이 없습니다"라고 해요</h4><p><code>--role</code>이나 <code>--skill</code> 뒤의 이름이 틀린 경우입니다. <code>./scripts/install.sh --list</code>로 정확한 이름을 확인하세요. 직업군 값은 <code>project</code> <code>admin</code> <code>research</code> <code>student</code> 네 가지입니다.</p></div></div>
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
