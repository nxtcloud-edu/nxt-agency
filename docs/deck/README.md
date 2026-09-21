# 소개·핸즈온 발표자료

`nxt-agency-intro.json`은 nxt-agency 소개와 핸즈온 진행용 슬라이드 28장의 내용(제목·본문·발표자 메모)이고, `captures/`는 실제 설치·체험 명령 출력을 찍은 화면입니다(제작도구 `capture/`로 생성).
PPTX는 바탕화면 `발표자료서버/제작도구`의 빌더로 만듭니다.

```sh
cd ~/Desktop/발표자료서버-리팩토링/제작도구/artifact-tool
node build.mjs /path/to/nxt-agency/docs/deck/nxt-agency-intro.json out/nxt-agency-intro.pptx --preview out/preview
# 또는 node 없이
python3 ../python-pptx/build_from_json.py /path/to/nxt-agency/docs/deck/nxt-agency-intro.json out/nxt-agency-intro.pptx
```

디자인 규칙과 JSON 형식은 `제작도구/DESIGN.md`. 스킬·샘플이 바뀌면 이 JSON의 명령 표와 예시도 함께 고칩니다.
