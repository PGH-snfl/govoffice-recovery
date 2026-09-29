# 한글 문서 자동 작성 공개 프로젝트 추가 조사

확인일: 2026-09-08

## 조사 범위와 검증 수준

Exa Search로 스킬·업무 양식·한글 프로그램 직접 조작의 3개 방향에서 총 9회 검색했다. 검색 결과는 중복 포함 90건이다. 저장소 경로 기준 후보는 46개였으며, 별칭·복제본·기존 소개 항목을 구분한 뒤 아래 추가 후보 18개를 정리했다. 숫자는 검색 범위이며 설치 성공이나 기능 검증 수가 아니다.

제작자의 공개 저장소와 README(설명서), 기능 목록, 요구사항을 확인했다. 설치·실행·실제 한글 문서 편집·보안 감사는 수행하지 않았다. 설명서에 나오는 '완벽', '100% 보존', '모든 기능' 등의 표현은 보장으로 받아들이지 않았다. 아래 기능은 제작자가 문서화한 범위다.

스킬은 AI가 따르는 작업 지침과 보조 프로그램 묶음이다. MCP(Model Context Protocol)는 AI가 외부 도구를 호출하는 연결 규격이다. CLI(Command Line Interface)는 명령어로 프로그램을 실행하는 방식이다. COM(Component Object Model)은 Windows 프로그램의 기능을 다른 프로그램에서 호출하는 기술이다. DLL(Dynamic-Link Library)은 프로그램에 로드하는 기능 모듈 파일이다. API(Application Programming Interface)는 프로그램끼리 기능을 호출하는 인터페이스다.

## 1. 보고서·교육 문서 작성과 서식 적용 스킬

| 번호 | 프로젝트·출처 | 문서화된 기능 | 연결·실행 조건 | 제한과 검토 포인트 |
|---|---|---|---|---|
| 1 | [jkf87/hwpx-skill](https://github.com/jkf87/hwpx-skill) | 텍스트·마크다운으로 HWPX 생성, 기안문, 문제지·답안지, 학생 활동지 변환, 양식 필드 채우기 | Claude용 스킬과 Python 도구. HWP→HWPX 변환은 Node.js 사용 | 같은 제작자의 hwp-mcp와 다른 저장소. 포맷 변환 시 복잡한 도형·음영·쪽 나눔 변화 가능성을 설명서에 명시 |
| 2 | [Kminer2053/public-doc-to-hwpx](https://github.com/Kminer2053/public-doc-to-hwpx) | 공공기관 보고서 문체 정리, 개조식·두괄식 구성, 양식 슬롯에 내용 삽입, HWPX·메일 본문 출력 | Claude 스킬, Python 빌더, 동봉 양식 | 단순 파일 변환보다 보고서 문체·정해진 양식에 초점. 임의 기관 서식의 완전 보존을 검증한 것은 아님 |
| 3 | [dohyun851208/teacher](https://github.com/dohyun851208/teacher) | 교사 행정문서, 공문, 이력·공적조서, 연수·경력 목록, HWPX 양식 작업 | Claude와 Codex 설치 안내 및 Codex 메타데이터 제공 | 증빙·개인정보·서명·완성 제출물은 공개 저장소에 포함되지 않음. 실제 사용자 자료를 별도로 제공해야 함 |
| 4 | [ratiertm/hwpx-skill](https://github.com/ratiertm/hwpx-skill) | 자연어 지시에 따른 제목·본문·표·목록 문서 구성, 마크다운 변환, 웹 작성 화면 | Python 도구를 호출하는 에이전트 환경. 내장 웹 화면의 AI 작성은 Claude Code 로그인에 의존 | ChatGPT 언급은 있지만 웹 화면의 생성 모델까지 ChatGPT인 것은 아님. 라이선스 상세 파일 위치는 추가 확인 필요 |
| 5 | [sdkparkforbi/claude-skill-hwpx](https://github.com/sdkparkforbi/claude-skill-hwpx) | 표·병합·이미지·머리말·꼬리말·쪽번호를 갖춘 문서 생성, 읽기·편집·변환 | Claude Code 중심. 생성과 한글 재저장·PDF 변환은 Windows+한글 필요 | 한글에서 열고 다시 저장해 배치를 재계산하는 절차를 권장. 한글 버전 차이 시 기준 문서 재생성 필요 |
| 6 | [6aneffy/hwpx-kit](https://github.com/6aneffy/hwpx-kit) | 기획서 생성, 양식 채우기, 명단별 문서 일괄 생성, 표 구성·계산, 공문 표기 점검, 사용자 제공 도장 삽입 | Claude Code 플러그인과 Python 명령 도구. 일부 변환·실제 한글 검수는 Windows+한글 필요 | 워드·프레젠테이션 출력까지 한글과 완전히 같은 디자인이라고 보장할 수 없음. 명단별 출력은 원본과 분리한 사본 경로 확인 필요 |
| 7 | [parkjui92/form-tailor](https://github.com/parkjui92/form-tailor) | 기관 샘플의 절 순서·문체·표 구조를 읽고 새 내용을 같은 틀로 배치, 항목별 대조표 작성 | Claude Code 스킬. 한글 읽기·쓰기는 kordoc 등 별도 도구 필요 | **내용 조사·집필을 대신하지 않는다고 명시.** 샘플과 채울 원고가 모두 필요. 공개 검증 기록은 가상 양식 시험 한 건이라고 명시 |
| 8 | [kangdacool/hwpx-editing-skill](https://github.com/kangdacool/hwpx-editing-skill) | HWPX 편집 규칙, 내부 구조 점검, 재압축·참조 검증 등 생성·수정 보조 | Claude·Codex 등 에이전트용. 제작자는 ChatGPT 대화에 가이드를 첨부하는 방법도 안내 | **완성형 보고서 집필기보다는 편집·검증 보조 스킬.** 가이드 첨부만으로 실행 도구가 설치되거나 한글 창에 연결되지는 않음 |

## 2. 초안 생성·파일 작성·변환 도구

| 번호 | 프로젝트·출처 | 문서화된 기능 | 연결·실행 조건 | 제한과 검토 포인트 |
|---|---|---|---|---|
| 9 | [maenjh/han-auto](https://github.com/maenjh/han-auto) | 참고 자료와 주제로 보고서 초안 생성, 예산·일정·역할분담 표 구성, 양식에 맞춘 HWPX 출력 | OpenAI API·Codex CLI·Claude CLI 등을 선택. 기본 HWPX 처리는 한글 없이 실행 | OpenAI API 방식과 Codex 로그인 방식은 다른 경로. HWP 입력은 HWPX 변환하며 Java 개발 도구 및 첫 실행 다운로드가 필요할 수 있음 |
| 10 | [DoHyun468/claw-hwp](https://github.com/DoHyun468/claw-hwp) | HWP/HWPX 생성·편집, 표·도형·차트·쪽 설정·필드 채우기, 브라우저 미리보기 | Claude·Codex용 안내. rhwp 기반으로 한글 설치 없이 파일 처리 | HWP 원래 형식 저장도 지원한다고 설명하지만 실제 호환성은 미검증. PDF·워드 변환은 확인한 설명서에서 예정 기능으로 구분 |
| 11 | [chrisryugj/kordoc](https://github.com/chrisryugj/kordoc) | 한글·다른 문서에서 자료 추출, 신구대조, 양식 채우기, 마크다운→HWPX | Node.js 기반 명령 도구와 MCP 서버. Windows·macOS·Linux 안내 | 문서 분석·변환 엔진 성격이 강함. 내용 작성은 연결된 AI가 담당. 자체 미리보기가 한글의 실제 쪽 배치와 동일하다고 단정하면 안 됨 |
| 12 | [gridi-ai/hancom-mcp](https://github.com/gridi-ai/hancom-mcp) | HWP→HWPX 변환, 문단·표 삽입, 텍스트 치환, 문서 스타일 조회·추가·적용 | Python, 변환에는 Java. 기본 파일 처리는 한글 설치 필수가 아님 | **한컴 공식 서버가 아니라 gridi-ai의 공개 프로젝트.** HWP 직접 편집보다는 변환 후 HWPX 편집 경로 |

## 3. 설치된 한글을 직접 조작하는 연결 도구

아래 5개는 Windows에 한글 프로그램이 있어야 한다. AI가 작성한 내용을 실제 한글 기능으로 넣는 구조이며, 파일만 생성하는 도구와 다르다.

| 번호 | 프로젝트·출처 | 문서화된 기능 | 구별되는 점 | 제한과 검토 포인트 |
|---|---|---|---|---|
| 13 | [innae1121-bit/gsghwp](https://github.com/innae1121-bit/gsghwp) | 현재 열린 문서·선택 영역 조회, 표 채우기·복제, 서식 변경, 이미지·캡션, 페이지 결과 확인 | Codex·Claude 안내. 문서와 개체 식별자를 사용한 대상 확인, 한글 내부 모듈 사용 | 한글 2024를 지원 대상으로 명시. **DLL 설치와 사용자 레지스트리 변경**, 자동 업데이트가 있어 변경·복구 범위를 설치 전에 검토해야 함 |
| 14 | [Feynman520/d01-p01-hwp-form-automation-mcp](https://github.com/Feynman520/d01-p01-hwp-form-automation-mcp) | 정부·학교 양식의 변환→내용 추출→입력 필드 생성→값 채우기→PDF 출력 | pyhwpx 기반의 양식 처리 작업 흐름. 진단·세션 복구 도구도 제공 | 로그인된 Windows 데스크톱과 한글 필요. 확인한 설명서는 한글 2024 검증 환경을 명시. 임의 문서 전체의 서식 무손실을 독립 검증한 것은 아님 |
| 15 | [realcoding2003/readwrite-hwp-mcp](https://github.com/realcoding2003/readwrite-hwp-mcp) | 기본 문서 생성·열기·저장, 텍스트 삽입, 표 생성 | 간단한 한글 자동화 연결을 살펴보기 좋은 구조 | 소개 상단에는 넓은 편집 기능이 있지만 최소 구현 목록은 6개 도구. **광범위한 기능 전체가 완성됐다고 분류하지 않음** |
| 16 | [mjyoo2/hwp-mcp](https://github.com/mjyoo2/hwp-mcp) | 텍스트·표·쪽 서식, 누름틀 일괄 채움, 선택 영역 저장 등 명령 목록 | Python 서버와 장기 실행 PowerShell 한글 연결 프로세스를 분리 | 도구 수와 '100% coverage'는 제작자 설명이며 실행 보장이 아님. 임의 동작·스크립트 호출 기능도 있어 허용 도구 제한 필요 |
| 17 | [twoLoop-40/HwpAutomation](https://github.com/twoLoop-40/HwpAutomation) | 문서 생성·열기·닫기·저장, 텍스트 삽입, 표 생성, 상태 조회 | 문서의 열림·수정·저장 상태를 구분하는 단순 구성 | 제공 목록이 7개 기본 도구. 복잡한 기관 양식 자동 작성 완제품보다는 기초 연결 예제에 가까움 |

## 4. 범정부오피스에 붙이는 개발용 재료

| 번호 | 프로젝트·출처 | 문서화된 기능 | 연결·실행 조건 | 제한과 검토 포인트 |
|---|---|---|---|---|
| 18 | [psychofict/hwpkit](https://github.com/psychofict/hwpkit) | HWP/HWPX 텍스트 읽기·교체, 빈 셀 채우기, 체크 표시 변경, 도장·서명 이미지 삽입 | 한글 설치 없이 쓰는 Python 라이브러리 | **ChatGPT용 스킬이나 문서 집필 앱이 아님.** 우리 코드 또는 별도 연결 도구가 필요. 바이너리 HWP 재작성은 원본 보존·실제 열림 시험 필요 |

## 우리 목적에 맞춘 우선 검토

이 순서는 실행 성능 순위가 아니라 공개 문서의 작업 범위와 현재 요구사항을 비교한 판단이다.

1. **참고 자료로 보고서 초안부터 파일까지**: han-auto. AI 초안 생성과 파일 조립을 구분하며 OpenAI·Codex 경로를 명시한다.
2. **공문·계획서·교육 문서를 폭넓게**: jkf87/hwpx-skill. 기안문과 문제지·활동지처럼 용도가 구체적이다.
3. **명단별 반복 생성·기관 실무 작업**: hwpx-kit. 양식 채우기와 문서 일괄 생성에 초점이 있다.
4. **열어 둔 문서에 즉시 적용**: GSG HWP. 다만 다른 후보보다 설치 변경 범위가 크므로 시험용 환경에서 먼저 확인해야 한다.
5. **내용은 이미 있고 기관 양식만 맞추기**: form-tailor. 집필기가 아닌 형식 적용 지침이라는 한계가 오히려 분명하다.

## ChatGPT에서 쓴다는 표현의 구분

- ChatGPT 웹에 GitHub 주소를 붙이는 것만으로 로컬 Python 프로그램이나 한글 창이 자동 연결되는 것은 아니다.
- 로컬 Codex는 로컬 MCP 서버를 연결할 수 있다. ChatGPT 웹은 원격 MCP 기반 도구를 사용하며 로컬 Codex 설정 파일을 읽지 않는다. [OpenAI 공식 MCP 문서](https://learn.chatgpt.com/docs/extend/mcp)
- Claude용 스킬을 Codex로 가져올 수 있는지는 경로·명령·의존성·클라이언트 전용 기능을 확인해야 한다. SKILL.md 파일이 있다는 이유만으로 모든 클라이언트에서 검증됐다고 볼 수 없다.
- han-auto의 OpenAI API 경로는 'ChatGPT 웹에서 실행'과 다르다. API 키를 사용하는 프로그램 연동이다. Codex CLI 경로는 설치된 Codex의 실행·인증을 사용하는 별도 선택지다. [han-auto 설명서](https://github.com/maenjh/han-auto)
- 문서 처리가 로컬이라는 사실과 문서 내용이 AI 서비스로 전달되지 않는다는 주장은 별개다. 내부 문서는 사용하는 AI 서비스와 기관 규정에 맞춰 제공 범위를 정해야 한다.

## 중복·제외·미확인 기록

- airmang/hwpx-skill과 hwpx-plugins는 이름 변경·동일 계열로 구분했으며 새 후보 수를 늘리는 데 쓰지 않았다.
- STARG-LEE/claude-skill-hwpx는 설명서에 sdkparkforbi 저장소 설치 안내가 있어 같은 계열로 묶었다.
- coport-uni/hwp-mcp는 기존 소개한 treesoop 계열과 설명·구성이 중복되어 별도 추천으로 세지 않았다.
- redasdm/hwpx-skills는 검색 결과에 Codex 보고서·계획서 스킬이 나왔지만 원본 본문 조회가 반복 실패해 검증된 18개에 넣지 않았다.
- ratiertm/pyhwpxlib, airmang/python-hwpx 등은 스킬의 기반 엔진을 다시 세어 목록을 부풀리지 않도록 구분했다.
- 전에 소개한 airmang/hwpx-plugins, kist-aix/hwpx, HwpForge, Hangeul-mcp, treesoop/hwp-mcp, jkf87/hwp-mcp는 이번 추가 18개에 포함하지 않았다.
- 제작자 설명서의 높은 도구 수, 시험 통과 수, '손실 없음' 주장은 이번 조사에서 직접 재현한 수치가 아니다.

## 도입 전에 할 확인

시험용 문서로 생성·저장·재열기, 본문과 여러 표의 읽기 순서, 병합 셀, 쪽 나눔, 글꼴, 그림, 대상 문서 고정을 확인한다. 기존 범정부오피스가 연결한 한글과 동시에 쓰는 경우 서로 다른 문서를 조작하지 않는지도 확인해야 한다. 현재 프로젝트나 한글 설정은 이번 조사로 변경하지 않았다. 추가한 것은 이 조사 문서뿐이다.
