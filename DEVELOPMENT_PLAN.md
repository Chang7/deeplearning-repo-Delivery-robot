# Development Plan

이 문서는 `dev` 브랜치를 정리해 재업로드하기 위한 우선순위 목록입니다.

## 1. 즉시 개선할 항목

- 깨진 README/문서 인코딩 정리
- 실제 실행 파일명 기준으로 실행 가이드 정리
  - `src/ai_server.py`
  - `src/main_hub.py`
  - `src/cart_camera_app.py`
  - `src/cart_ui_app.py`
  - `src/cart_ui_app_v2.py`
- CI에서 GUI/카메라/DB 의존 테스트를 분리

## 2. AI/Detection

- `ObstacleDetector`, `ProductRecognizer`의 입력/출력 schema 문서화
- 모델 파일 경로를 `configs/model_config.yaml` 기준으로 통일
- 카메라 없이 샘플 이미지/동영상으로 실행 가능한 demo script 추가
- 위험도 평가 기준을 `configs/`로 이동하거나 문서화

## 3. Main Hub / Network

- TCP/UDP 포트와 메시지 protocol 문서화
- 연결 실패/타임아웃 처리 보강
- 로컬 단일 PC 테스트용 config profile 추가

## 4. Database

- DB가 없어도 시작 가능한 mock mode 또는 dry-run mode 추가
- 초기 schema/seed 실행 순서 정리
- DAO 단위 테스트 추가

## 5. UI

- PyQt6 UI를 실제 카메라/DB 없이 실행하는 demo mode 추가
- v1/v2 UI 중 권장 버전 명시
- UI 이벤트 protocol 예제 추가

## 6. GitHub 재업로드 전 체크리스트

- `git status` clean 확인
- `.env`, DB 비밀번호, 개인 경로 제거
- README 실행 명령 검증
- 최소 smoke test 통과
- 작업 브랜치로 push 후 PR 생성 권장
