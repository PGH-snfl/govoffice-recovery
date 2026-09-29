# HwpForge 상세 검토

확인일: 2026-09-08. 대상: ai-screams/HwpForge의 v0.16.4 및 당시 main(f403d6fcdd09798bf86460c9d3d1e8b2de988d88).

## 결론

HwpForge는 한글 프로그램의 창을 조작하는 프로그램이 아니라, 한글 문서 파일을 직접 읽고 만드는 Rust 라이브러리다. AI에 연결하는 MCP 서버와 명령행 도구, 문서 작업 방법을 알려주는 스킬을 함께 제공한다. 범정부오피스에는 새 HWPX 보고서 생성과 정해진 양식의 내용 채우기를 보조하는 용도로 검토할 가치가 있다. 현재 문서 선택·선택 영역 복사·커서 위치 삽입을 담당하는 기존 한글 연결을 통째로 대체할 근거는 없다.

이번 검토는 공개 소스·테스트 코드·릴리스·이슈의 정적 확인이다. 설치하거나 실행하지 않았으며, 사용자의 실제 한글 문서로 호환성을 시험하지 않았다. ‘구현 확인’과 ‘실행 검증 완료’는 다르다.

출처: [저장소](https://github.com/ai-screams/HwpForge), [v0.16.4 릴리스](https://github.com/ai-screams/HwpForge/releases/tag/v0.16.4), [실제 MCP 등록 코드](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-mcp/src/server.rs).

## 1. 무엇으로 구성되는가

- Rust 라이브러리: 파일의 문단·표·글자 모양·그림 등을 데이터로 해석하고 파일로 만든다.
- Hammer: CLI(Command Line Interface, 명령을 입력해 사용하는 인터페이스). 파일 변환·편집·점검을 명령으로 실행한다.
- Anvil: MCP(Model Context Protocol, AI와 외부 도구를 연결하는 공통 규약) 서버. AI가 문서 처리 기능을 도구처럼 호출하게 한다. 소개에서는 Beta로 명시한다.
- HwpForge Skill: AI가 작업에 맞는 명령을 고르고 문서를 편집하도록 안내하는 사용 지침과 예시 모음. 자체적으로 문서를 처리하는 실행 엔진은 아니다.

자료: [서버 진입점](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-mcp/src/main.rs), [CLI 진입점](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-cli/src/main.rs), [제공 스킬](https://github.com/ai-screams/HwpForge/blob/v0.16.4/.claude/skills/hwpforge/SKILL.md).

## 2. 최신 상태와 설명서 불일치

GitHub가 latest로 반환한 공개 버전은 2026-08-28의 v0.16.4다. 당시 main도 이 버전이었다. 하지만 검색에 잡힌 소개와 저장소의 일부 문서는 이전 상태를 설명한다.

| 항목 | 설명서와 실제 소스의 차이 |
|---|---|
| MCP 도구 수 | 루트 소개는 9개, v0.16.4 서버에 등록된 도구는 19개 |
| 하위 MCP README | 더 적은 5개 도구만 설명하며 설치 패키지 이름도 다른 곳과 불일치 |
| PDF | 루트 구조 그림에는 빠져 있지만 현재 작업공간에 PDF 처리 크레이트와 to-pdf 명령 존재 |
| Rust 요구 버전 | 공통 값과 MCP는 1.88, 현재 CLI는 PDF 의존성 때문에 1.92 |
| CLI 설치 | 현재 CLI Cargo.toml에는 publish=false. 소개의 cargo install 명령이 최신 소스 기능 전체 설치를 보장하지 않음 |
| npm 버전 | 저장소 package.json의 0.0.1은 빌드 시 버전을 바꾸는 구조. 이 값으로 실제 공개 버전을 판단하면 안 됨 |

따라서 사용한다면 설치한 실행기의 버전과 실제 도구 목록을 다시 확인해야 한다. 이번에는 npm 레지스트리의 최신 버전 직접 조회가 실패하여 npm 최신 패키지와 v0.16.4의 일치 여부를 확정하지 않았다. 검색에 나타난 Windows 패키지의 오래된 색인 값도 최신 값으로 간주하지 않았다.

자료: [공통 패키지 설정](https://github.com/ai-screams/HwpForge/blob/v0.16.4/Cargo.toml), [CLI 설정](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-cli/Cargo.toml), [npm 공개 작업](https://github.com/ai-screams/HwpForge/blob/v0.16.4/.github/workflows/npm-publish.yml).

## 3. 실제 등록된 MCP 도구 19개

아래는 v0.16.4의 server.rs에서 등록 이름과 연결된 처리 함수를 확인한 목록이다. 모든 도구가 모든 한글 파일에서 성공한다는 뜻은 아니다.

| 도구 이름 | 사용자 관점의 기능 | 주요 제한 |
|---|---|---|
| hwpforge_convert | Markdown을 새 HWPX로 생성 | 기존 문서 디자인의 완전 복사 기능 아님 |
| hwpforge_inspect | 문서의 구역·문단·표·그림 등의 수 확인 | 화면 결과 검증 아님 |
| hwpforge_to_json | 문서 전체 또는 특정 구역을 편집용 구조 데이터로 추출 | 화면에서 선택한 영역과 구역은 다름 |
| hwpforge_from_json | 구조 데이터에서 HWPX 생성·재구성 | 미지원 요소 보존 보장 없음 |
| hwpforge_patch | 원본 파일의 특정 구역 내 기존 텍스트 교체 | 글자 모양 변경·표 구조 변경 등은 거부 |
| hwpforge_outline | 제목·표·이름 붙은 누름틀·책갈피 목록 확인 | 구조 변경 후 위치 정보를 다시 읽어야 함 |
| hwpforge_diff | 편집 전후 내용과 파일 내부 구성 비교 | 화면 모양·페이지 배치의 동일성 보장 아님 |
| hwpforge_delete_para | 본문 최상위 문단 삭제 | 참조·강제 쪽 나눔·첫 문단 등 제한 |
| hwpforge_insert_para | 기준 문단 앞뒤에 문단 삽입 | 기준 문단 서식을 상속, 안전 검사 통과 필요 |
| hwpforge_read | 특정 문단 범위·표·누름틀의 내용만 읽기 | 글자가 아닌 내용은 표시자로 표현될 수 있음 |
| hwpforge_fields | 누름틀 이름·힌트·현재 값·채우기 가능 여부 조회 | 사용자 화면의 대표필드와 자동으로 동일시하면 안 됨 |
| hwpforge_fill | 누름틀 이름에 대응하는 값 입력 | 중복 이름·빈 값·채울 수 없는 필드 거부 |
| hwpforge_stamp_plan | 양식의 입력 위치 후보 탐색 | 의미를 완벽하게 판정하는 자동 완성 기능 아님 |
| hwpforge_stamp | 승인된 후보를 이름 붙은 누름틀로 전환 | 안전 검사 및 전체 사전 검증, 명세 작성 필요 |
| hwpforge_set_cell | 표 번호와 셀 위치·인접 항목명으로 셀 내용 교체 | 텍스트 셀만, 복합 서식은 첫 텍스트 서식 기준 |
| hwpforge_validate | 파일 구조와 데이터 관계 검사 | 한글에서 화면이 동일한지까지 확인하지 않음 |
| hwpforge_restyle | 기본 글꼴을 프리셋 글꼴로 변경 | 실제 구현은 주로 기본 글꼴 치환, 임의 디자인 전체 변경 아님 |
| hwpforge_templates | 내장 스타일 목록 조회 | 우리 선택 영역 프리셋 저장소와 다른 개념 |
| hwpforge_to_md | HWPX 내용을 Markdown으로 추출 | 읽기 좋은 텍스트 변환과 원본 서식 보존은 구분 필요 |

자료: [19개 등록 함수](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-mcp/src/server.rs), [도구 구현 폴더](https://github.com/ai-screams/HwpForge/tree/v0.16.4/crates/hwpforge-bindings-mcp/src/tools).

HWP5 읽기·변환·점검과 PDF 출력은 현재 이 19개 MCP 도구에 포함되지 않는다. CLI 쪽의 별도 기능이다.

## 4. 파일 형식과 한글 설치 여부

HWPX는 XML(eXtensible Markup Language, 태그로 문서 구조를 표현하는 언어) 파일 등을 ZIP으로 묶은 형식이다. HwpForge는 이 내부 데이터를 직접 처리한다. HWP5는 확장자가 .hwp인 기존 바이너리 문서 계열이다.

- HWPX 읽기·쓰기: 제공.
- HWP5 읽기 및 HWPX 변환: 별도 변환 경로 제공.
- HWP5 .hwp 저장: 제공하지 않음.
- 이미 열린 한글 창·현재 커서·마우스 선택 범위 조작: 현재 MCP 도구 목록에 없음.
- 파일 생성과 편집 자체를 위해 한글 창을 켤 필요는 없는 방식이다. 최종 실제 한글 표시 확인은 별도다.

근거: [제공 스킬의 HWP5 writer 제한](https://github.com/ai-screams/HwpForge/blob/v0.16.4/.claude/skills/hwpforge/SKILL.md), [파일 변환 경로](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-cli/src/main.rs).

## 5. ‘원본 서식을 유지하고 내용만 변경’의 정확한 범위

### 기존 텍스트만 고치는 patch

patch.rs는 원본의 건드리지 않은 내부 파일을 보존하고, 대상 구역에서 기존 텍스트 위치를 찾아 교체한다. 보존 정보의 버전·원본 해시·텍스트 위치 관계를 재검증한다. 과거 원본으로 만든 편집 정보를 새 파일에 잘못 적용하는 것을 차단하려는 설계다.

하지만 보존형 patch는 의도적으로 텍스트 변경만 허용한다. 글자 모양 번호만 바꿔도 구조 변경으로 거부할 수 있으며, 스타일 저장소 변경·바탕쪽 편집·표 형태 변경을 자유롭게 받아주는 방식이 아니다. 텍스트 길이가 달라지면 한글이 다시 배치할 때 줄바꿈이나 쪽수가 달라질 수 있으므로, 서식 보존을 화면 배치 불변으로 설명해서는 안 된다.

자료: [보존형 patch 구현](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-hwpx/src/patch.rs).

### 누름틀 채우기 fill

예를 들어 ‘성명’이라는 누름틀에 홍길동을 입력한다. 한 요청의 대상들을 먼저 검증하고, 하나라도 잘못되면 작업을 거부한다. 같은 이름의 누름틀이 여러 개이면 모호하다고 판단하여 거부한다. 빈 문자열로 누름틀 값을 지우는 것도 거부한다.

우리의 ‘같은 대표필드 이름을 묶어 여러 위치에 한 값을 넣기’와는 정책이 다르다. 활용한다면 대표필드는 하나로 보여주되 내부 입력 위치에는 성명_01, 성명_02처럼 고유 이름을 부여하고 동일 값을 각각 전달하는 연결 처리가 필요하다. 이는 제안이며 HwpForge가 우리 프로젝트를 자동 처리한다는 뜻이 아니다.

자료: [fill 정책 및 구현](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-hwpx/src/fill.rs), [중복·빈 값·다중 구역·전체 실패 테스트](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-hwpx/tests/fill_api.rs).

### 표 셀 수정 set-cell

표 순번과 행·열 주소 또는 ‘성명 오른쪽 칸’, ‘비고 아래 칸’ 같은 위치 지정이 가능하다. 병합된 칸의 내부 좌표는 실제 병합 기준 셀로 연결하며, 모호한 항목명은 거부한다. 단순히 문서 전체에서 같은 글자만 검색해 바꾸는 것보다 대상 지정이 명확하다.

그러나 셀에 그림·표·컨트롤이 들어 있으면 거부한다. 새 텍스트는 첫 텍스트 문단/글자의 서식을 상속하므로, 원래 한 셀 안에서 이름은 굵게, 연락처는 작게 쓰인 복합 서식을 그대로 분배해 유지하는 편집이 아니다. 이 경우 기존 글자 덩어리별 patch 경로와 별도 대응이 필요하다.

자료: [셀 편집 계약](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-hwpx/src/cell_edit.rs).

### 전체 재생성 from-json

JSON(JavaScript Object Notation, 구조화된 데이터를 저장하는 표기 형식)으로 문서 전체를 다시 만들 수는 있다. 그러나 해석 가능한 내부 모델로 재구성하는 경로이므로 복잡한 한글 요소를 모두 보존한다고 보장할 수 없다. 제공 스킬도 실제 기관 서식을 재생성한 뒤에는 한글에서 시각적으로 확인하라고 경고한다.

자료: [제공 스킬의 Fidelity Warning](https://github.com/ai-screams/HwpForge/blob/v0.16.4/.claude/skills/hwpforge/SKILL.md).

## 6. 프리셋과 양식 인식

내장 목록은 default(함초롬돋움), modern(맑은 고딕), classic(바탕), latest(함초롬바탕) 네 가지다. 이는 우리 프로젝트에서 사용자가 선택한 표의 행·열별 글자 모양, 테두리, 정렬 등 전체 디자인을 보관하는 프리셋과 다르다.

특히 MCP restyle 소스는 원본 스타일 번호들을 유지하면서 기본 글꼴 이름을 바꾸는 처리다. 도구 설명의 ‘스타일 일괄 적용’을 기관 양식 전체 디자인 자동 변환으로 확대 해석하면 안 된다. MCP convert는 네 목록을 조회하고 글꼴을 적용하는 반면, 제공 스킬에는 CLI convert가 default만 처리한다고 적혀 있어 두 진입점의 동작도 구분해야 한다.

자료: [내장 프리셋](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-hwpx/src/presets.rs), [restyle 실제 처리](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-mcp/src/tools/restyle.rs), [MCP convert](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-mcp/src/tools/convert.rs).

stamp 계열은 네모·괄호 빈칸·날짜 빈칸 같은 표시와 빈 표 셀 등을 입력 위치 후보로 만들고, 작성한 명세에 따라 누름틀로 바꾸는 기능이다. 사용자의 문서에서 개인정보 의미를 완벽하게 판별하거나 기관별 대표필드 체계를 자동 구성하는 기능으로 확인된 것은 아니다.

자료: [stamp 도구](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-mcp/src/tools/stamp.rs).

## 7. 현재 확인된 실무 위험

### 미해결 이슈 #143

등록자는 2026-08-17 기준으로 보존형 편집의 두 제약을 보고했다. 첫째는 글자 서식 변경도 거부한다는 점, 둘째는 구조 편집 전 안전 검사가 실제 편집 범위보다 넓어 많은 문서를 거부한다는 점이다. 등록자가 시험한 자체 서식군과 저장소 예제군의 실패 수치는 해당 실험의 결과이며 모든 문서의 일반 실패율로 볼 수 없다.

확인일 현재 이슈는 open이다. v0.16.4 structural.rs에도 문서를 한 번 변환해 다시 읽은 결과와 원본의 문서·서식·그림 및 내부 파일 구성을 비교하는 진입 검사가 남아 있다. 안전 검사가 있다는 점과 실제 기관 양식에서 기능이 잘 통과한다는 점은 별개다.

자료: [#143](https://github.com/ai-screams/HwpForge/issues/143), [구조 편집 검사](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-hwpx/src/structural.rs).

### 미해결 이슈 #141

일부 문서의 도형 배치 정보에 반복되는 행렬 항목이 있을 때 문서 전체 읽기가 실패한다는 보고다. 확인일 현재 open이며 독립 재현은 하지 않았다. 복잡한 그림·도형이 섞인 원본을 읽을 때 시험할 항목이다.

자료: [#141](https://github.com/ai-screams/HwpForge/issues/141).

### 수정된 이슈 #142

공백만 들어 있는 글자 덩어리가 읽기 과정에서 사라진다는 문제가 있었다. 유지관리자는 v0.16.4에서 수정했다고 답변했고 이슈가 completed로 종료되었다. 현재도 미해결인 것처럼 나열하지 않는다. 다만 사용자가 설치한 패키지가 이전 버전이면 수정 포함 여부를 확인해야 한다.

자료: [#142 및 유지관리자 답변](https://github.com/ai-screams/HwpForge/issues/142).

### 테스트 수와 호환성

저장소에는 누름틀 채우기·중복 이름 거부·대상 외 데이터 보존 등을 확인하는 테스트가 있다. 최신 main에 대한 2026-09-07 Nightly 작업 성공도 확인했다. 그러나 소개의 테스트 수·커버리지 배지는 모든 실제 한글 서식의 화면 동일성을 증명하지 않는다. 이번 검토에서 테스트를 직접 실행하지 않았다.

자료: [테스트 파일](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-hwpx/tests/fill_api.rs), [확인한 Nightly 실행](https://github.com/ai-screams/HwpForge/actions/runs/34101102217).

## 8. PDF 기능의 범위

PDF(Portable Document Format, 화면·인쇄 형태를 고정해 전달하는 문서 형식) 출력 코드와 CLI to-pdf 명령은 있다. 하지만 새로 문장을 배치하고 페이지를 계산하는 완전한 한글 조판 엔진은 아니다. 한글이 저장해 둔 줄·위치 정보인 조판 캐시를 재생하는 구조다.

따라서 새로 생성해 캐시가 없거나 편집으로 캐시가 제거된 문서는 한글에서 다시 열고 저장하는 과정이 필요할 수 있다. fill 테스트에도 변경 문단의 오래된 배치 캐시를 지우는 검사가 있다. ‘한글 없이 어떤 문서든 한글과 똑같은 PDF’라고 설명할 수 없다. 미지원 항목·글꼴·캐시 정책에 따라 경고 또는 거부가 발생한다. PDF 도구는 위 MCP 19개에는 없다.

자료: [PDF 엔진 계약과 오류](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-pdf/src/lib.rs), [to-pdf 구현](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-cli/src/commands/to_pdf.rs), [fill의 캐시 제거 테스트](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-smithy-hwpx/tests/fill_api.rs).

## 9. Codex 연결과 ChatGPT 연결

HwpForge 서버는 STDIO(Standard Input/Output, 로컬 프로세스의 표준 입출력) 방식으로 통신한다. OpenAI 공식 문서는 로컬 Codex 클라이언트에서 이 방식의 MCP 연결을 지원한다고 설명한다. 따라서 로컬 실행기를 등록하는 구조가 맞다. 아직 이 환경에 등록하거나 연결 시험하지 않았다.

ChatGPT 웹은 로컬 Codex 설정 파일을 읽지 않는다. 따라서 ‘Codex에 로컬 HwpForge를 등록했으니 ChatGPT 웹도 내 PC 파일을 바로 다룬다’고 말하면 안 된다. 웹에서 쓰려면 지원되는 원격 연결 방식과 접근 권한 설계가 별도로 필요하다. 이번 내부 프로젝트 용도에서는 불필요하게 원격 공개부터 할 이유가 없다.

자료: [OpenAI 공식 MCP 문서](https://learn.chatgpt.com/docs/extend/mcp), [HwpForge의 STDIO 서버](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-mcp/src/main.rs).

Windows x64용 실행 패키지 경로가 있고 Node.js 20 이상을 요구하는 npm 실행기가 있다. 지원 목록은 Windows x64, macOS x64/ARM64, Linux x64/ARM64다. 소스에 대상이 있다고 이 환경에서 실제 실행 검증까지 끝난 것은 아니다.

자료: [플랫폼 실행기](https://github.com/ai-screams/HwpForge/blob/v0.16.4/npm/packages/mcp/bin/hwpforge-mcp.js), [npm 설정](https://github.com/ai-screams/HwpForge/blob/v0.16.4/npm/packages/mcp/package.json).

## 10. 비용·내부 정보·파일 보호

MIT 또는 Apache-2.0 선택 라이선스다. MIT 원문은 이용·수정 권한을 무료로 부여하며 고지문 유지 조건을 둔다. HwpForge 소프트웨어 자체의 유료 이용료를 전제로 하는 구조는 아니다. AI 사용 요금, 한글 프로그램 사용권, 유지보수 작업은 별개다. 특정 AI 요금제나 가격은 이번 검토 대상이 아니다.

확인한 MCP 진입점은 로컬 도구 통신이며, 문서 생성 도구가 별도 AI 제공자에게 글 작성을 요청하는 구조는 아니다. 문장 작성은 연결한 AI가 맡고 HwpForge가 파일 처리를 한다. 단, 로컬 도구가 문서 텍스트나 기존 개인정보를 AI에 응답하면 그 내용은 AI 대화에 포함될 수 있다. 로컬 실행을 외부 전송 전혀 없음과 동일시하면 안 된다.

파일 출력 처리에는 상위 경로 이동·일부 민감 설정 폴더·마지막 경로의 심볼릭 링크를 차단하는 검사가 있다. 하지만 프로젝트 폴더만 허용하는 완전한 경계는 아니며, 기존 파일을 덮어쓸 수 있는 일반 쓰기 함수를 사용한다. 제공 스킬도 원본 덮어쓰기를 기본으로 안내하므로, 우리 내부 사용 정책에 맞게 사본 출력·백업·허용 경로를 별도로 정해야 한다. 원격 저장소의 이 지침을 이번 조사에서 실행하지 않았다.

자료: [MIT 원문](https://github.com/ai-screams/HwpForge/blob/v0.16.4/LICENSE-MIT), [MCP 파일 입출력 구현](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-mcp/src/output.rs), [제공 스킬](https://github.com/ai-screams/HwpForge/blob/v0.16.4/.claude/skills/hwpforge/SKILL.md).

## 11. 범정부오피스에 적용한다면

아래는 적용 제안이며 구현한 내용이 아니다.

| 역할 | 맡길 쪽 | 이유 |
|---|---|---|
| 현재 한글 문서 연결·대상 고정 | 기존 한글 연결 | 사용자가 실제로 작업하는 문서와 연결 필요 |
| 선택 영역 서식 보관·커서 위치 삽입 | 기존 한글 연결과 우리 프리셋 | HwpForge의 구역 편집과 다른 기능 |
| 자연어로 새 보고서 초안 만들기 | AI + HwpForge | 텍스트를 HWPX 파일로 만드는 경로 존재 |
| 사전 검증된 기관 양식의 값 채우기 | HwpForge fill 또는 patch | 이름·값과 텍스트 위치를 명확히 지정 가능 |
| 같은 대표필드의 여러 위치 연결 | 우리 필드 관계 처리 | HwpForge fill은 중복 누름틀 이름을 거부 |
| 최종 화면·쪽 나눔·복잡한 서식 확인 | 실제 한글 | 구조 검사가 화면 동일성까지 증명하지 못함 |

Python 직접 연결 모듈은 현재 lib.rs에 덧셈 예제와 테스트만 있는 뼈대다. 따라서 ‘pip로 설치해 바로 우리 Python 코드에서 완성 API 사용’은 현재 확인된 상태와 다르다. 사용하려면 우선 검증된 실행기를 별도 프로세스로 호출하거나 MCP로 연결하는 형태를 검토하는 것이 현실적이다.

자료: [Python 모듈 현황](https://github.com/ai-screams/HwpForge/blob/v0.16.4/crates/hwpforge-bindings-py/src/lib.rs).

권장 시험 순서는 단순 새 문서 → 이름 붙은 누름틀 양식 → 본문과 병합표가 섞인 문서 → 원본 서식·텍스트만 교체 순서다. 원본 사본으로 각 작업의 성공 여부, 대상 외 변경, 글자·문단 서식, 쪽 나눔을 확인한 후 통과한 문서 유형만 기능에 연결하는 편이 좋다. 보존형 편집이 거부된 문서를 사용자에게 알리지 않고 전체 재생성으로 우회하지 않는 것이 중요하다.

## 조사 방법과 출처의 성격

Exa 검색 스킬로 프로젝트 자체, 제약·이슈, Windows 패키지의 3개 관점을 검색했다. 검색 요청은 중단된 호출을 포함하여 합계 20개 결과 규모였으며, 검색 결과를 그대로 검증 완료 자료로 간주하지 않았다. GitHub 연결 도구로 릴리스와 v0.16.4 소스, 이슈 상태, 테스트 구현을 직접 대조했다. OpenAI 연결 범위는 OpenAI 공식 문서로 확인했다.

- 저장소 코드·라이선스·릴리스: 제작자 직접 자료. 구현과 버전의 근거이나 실제 사용자 문서의 품질 보증은 아님.
- 이슈 #141/#143: 재현 조건을 제시한 이용자의 보고. 현재 이슈 상태 확인, 독립 재현 미실시.
- 이슈 #142 답변: 유지관리자의 수정 버전 설명. 이번 환경의 실제 실행 결과는 아님.
- OpenAI 문서: 제품 연결 방식의 공식 자료.

실시하지 않은 것: 프로그램 설치, npm 바이너리 실행, 프로젝트 코드 변경, 원본 문서 수정, 내부 자료 업로드, 실제 한글 화면 검증.
