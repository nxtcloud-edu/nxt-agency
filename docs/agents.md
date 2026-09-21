# 👥 전문가 에이전트 목록

각 전문가는 마크다운 한 파일입니다. `name`으로 부르거나 한글 이름으로 부르면 됩니다. 도구별 직접 지정: Claude Code `@name`(플러그인 설치면 `@nxt-agency:name`), Codex `$name`, Kiro CLI `kiro-cli chat --agent name` 또는 `/agent`. 파일 끝의 **이렇게 요청하세요**에 복사해 쓸 수 있는 예시가 있습니다.

### 🧭 안내

| 전문가 | name | 이럴 때 |
|---|---|---|
| 🧭 [안내 데스크](../guide/guide-concierge.md) | `nxt-guide` | 어떤 전문가·스킬을 써야 할지 모를 때 |

### 🎓 연구 — 교수·연구자·대학원생

| 전문가 | name | 이럴 때 |
|---|---|---|
| 🔍 [문헌조사 전문가](../research/research-literature-reviewer.md) | `literature-reviewer` | 선행연구 정리, 근거 수준 평가, 참고문헌 검증 |
| 📊 [통계·연구설계 전문가](../research/research-statistician.md) | `statistician` | 연구 설계, 표본 크기, 분석 방법, 결과 해석 |
| 📝 [연구과제·사업 제안서 작성가](../research/research-proposal-writer.md) | `proposal-writer` | 연구계획서·사업계획서, 공모 대응, 예산 설명 |
| 📈 [연구·산업 동향 조사원](../research/research-trend-researcher.md) | `trend-researcher` | 정책·산업·기술 동향, 벤치마킹 |

### 📚 교육·진로 — 학생·교수

| 전문가 | name | 이럴 때 |
|---|---|---|
| 🧩 [교육과정 설계자](../education/education-course-designer.md) | `course-designer` | 강의계획서, 비교과 프로그램, 학습성과·CQI |
| 🌱 [학습·진로 멘토](../education/education-study-career-mentor.md) | `study-career-mentor` | 학기 계획, 공부 습관, 진로 탐색 |
| 🧾 [자기소개서·이력서 코치](../education/education-resume-coach.md) | `resume-coach` | 자기소개서, 이력서, NCS·블라인드 채용 |
| 🎓 [유학·교환학생 상담가](../education/education-study-abroad-advisor.md) | `study-abroad-advisor` | 교환학생·유학 준비, 장학금, 어학시험 |

### 🗂️ 행정 — 행정직원·공공기관

| 전문가 | name | 이럴 때 |
|---|---|---|
| 📋 [회의록 정리원](../admin/admin-meeting-minutes.md) | `meeting-minutes` | 녹취록·메모 → 회의록 서식 |
| 📝 [보고서 요약가](../admin/admin-report-summarizer.md) | `report-summarizer` | 긴 자료 → 1페이지 보고·결재용 요약 |
| 📄 [문서 생성기](../admin/admin-document-generator.md) | `document-generator` | DOCX·PPTX·XLSX·PDF 파일 |
| ⚖️ [규정·법령 검토관](../admin/admin-compliance-checker.md) | `compliance-checker` | 법령·학내 규정 사전 점검 |
| 🔐 [개인정보보호 담당관](../admin/admin-privacy-officer.md) | `privacy-officer` | 동의서, 처리방침, 영향평가, 유출 대응 |
| ⚙️ [업무 프로세스 개선가](../admin/admin-process-improver.md) | `process-improver` | 업무 흐름 정리, 매뉴얼화, 반복업무 개선 |
| 💬 [민원·문의 응대원](../admin/admin-inquiry-responder.md) | `inquiry-responder` | 학생·민원 문의 답변, FAQ |

### 🎯 사업단

| 전문가 | name | 이럴 때 |
|---|---|---|
| 🗓️ [사업 관리자](../project/project-program-manager.md) | `program-manager` | 연차 사업계획 → 과업·일정·담당 |
| 📊 [성과 분석가](../project/project-performance-analyst.md) | `performance-analyst` | KPI 달성률, 연차평가 |
| 🗳️ [설문·의견 분석가](../project/project-survey-analyst.md) | `survey-analyst` | 만족도·수요조사·강의평가 |
| 📣 [홍보·보도자료 담당](../project/project-pr-manager.md) | `pr-manager` | 보도자료, 행사 홍보, 위기 메시지 |
| ✍️ [홍보 콘텐츠 제작자](../project/project-content-creator.md) | `content-creator` | 뉴스레터, 카드뉴스, SNS, 공고문 |
| 💰 [예산·집행 관리자](../project/project-budget-manager.md) | `budget-manager` | 사업비 편성·집행률·정산 |

### 💻 개발 — 학생·전산 담당자

| 전문가 | name | 이럴 때 |
|---|---|---|
| ⚡ [빠른 시제품 개발자](../engineering/engineering-rapid-prototyper.md) | `rapid-prototyper` | 캡스톤·해커톤·연구 데모 |
| 🎨 [프론트엔드 개발자](../engineering/engineering-frontend-developer.md) | `frontend-developer` | 웹 화면 구현 |
| 🏗️ [백엔드 설계자](../engineering/engineering-backend-architect.md) | `backend-architect` | API·DB 설계 |
| 👁️ [코드 리뷰어](../engineering/engineering-code-reviewer.md) | `code-reviewer` | 코드 품질·보안 점검 |
| 🤖 [AI 엔지니어](../engineering/engineering-ai-engineer.md) | `ai-engineer` | LLM API, 모델 실험, 데이터 파이프라인 |
