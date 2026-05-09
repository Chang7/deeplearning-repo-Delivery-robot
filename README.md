# Smart Shopping Cart / Delivery Robot AI

YOLO 기반 객체 인식과 분산 애플리케이션 구조를 활용한 스마트 쇼핑카트/배송 로봇 AI 프로젝트입니다.  
카메라 영상에서 장애물, 사람, 상품을 감지하고 Main Hub, UI, DB와 연동하는 구조를 목표로 합니다.

## 주요 구성

- `src/ai_server.py`
  - AI 추론 서버
  - UDP 영상 수신, YOLO 추론, 이벤트 전송 담당
- `src/main_hub.py`
  - 중앙 허브
  - AI 이벤트 처리, DB 연동, UI 명령 전송 담당
- `src/cart_camera_app.py`
  - 카트/로봇 카메라 스트리밍 클라이언트
- `src/cart_ui_app.py`, `src/cart_ui_app_v2.py`
  - PyQt6 기반 UI 애플리케이션
- `src/detectors/`
  - 장애물 감지, 상품 인식, 추적, 위험도 평가 로직
- `src/network/`
  - TCP/UDP 통신 모듈
- `src/database/`
  - MySQL 연동 및 DAO 계층
- `configs/`
  - 앱, DB, 모델, 네트워크 설정
- `test/`
  - 로컬 테스트, 웹캠 테스트, 모델/통합 테스트, 학습 스크립트

## 설치

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 환경 설정

```bash
cp .env.example .env
```

주요 변수:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

네트워크/모델 설정은 `configs/` 아래 YAML 파일에서 관리합니다.

## 실행 예시

### 1. AI 서버

```bash
python src/ai_server.py
```

### 2. Main Hub

```bash
python src/main_hub.py
```

### 3. 카트 UI

```bash
python src/cart_ui_app.py
```

또는 v2 UI:

```bash
python src/cart_ui_app_v2.py
```

### 4. 카트 카메라 스트리밍

```bash
python src/cart_camera_app.py
```

## 모델 파일

현재 저장소에는 다음 YOLO 모델 파일이 포함되어 있습니다.

- `yolo11n.pt`
- `yolo11n-obb.pt`
- `yolov8n-obb.pt`

모델 경로와 confidence threshold는 `configs/model_config.yaml`에서 조정합니다.

## 테스트

```bash
pytest -q
```

일부 테스트는 카메라, DB, YOLO 모델, GUI 환경이 필요할 수 있습니다.  
로컬 PC에서 먼저 실행 가능한 smoke test부터 분리하는 것을 권장합니다.

## 실제 카트/카메라 없이 로컬 시뮬레이션

카메라, DB, 실제 카트 없이 localhost TCP/UDP 통신 흐름을 검증할 수 있습니다.

```bash
python scripts/simulate_localhost_io.py
```

pytest 기반 테스트:

```bash
python -m pytest -q test/test_localhost_io.py
```

이 검증은 다음을 확인합니다.

- TCP length-prefixed JSON request/response round-trip
- UDP frame chunking/reassembly round-trip
- `send_frame_raw()` 경로가 OpenCV 없이도 동작하는지 확인

## 개발 상태 요약

현재 `dev` 브랜치는 핵심 구조와 모델/네트워크/DB/UI 모듈이 포함되어 있으나, GitHub에 다시 올리기 전 다음 보완이 필요합니다.

1. README/문서 인코딩 정리
2. 실행 가능한 최소 smoke test 정리
3. DB 없이 동작 가능한 mock 모드 보강
4. 카메라 없는 환경에서 테스트 가능한 샘플 이미지/비디오 입력 지원
5. CI가 무거운 GUI/YOLO 테스트를 직접 실행하지 않도록 테스트 분리
6. 설정 파일의 로컬/배포 환경 분리

자세한 작업 목록은 `DEVELOPMENT_PLAN.md`를 참고하세요.

## 보안 주의

- `.env` 파일은 Git에 올리지 마세요.
- DB 비밀번호, RDS 주소, 개인 토큰은 커밋하지 마세요.
- 학습 데이터와 대용량 모델 파일은 필요 시 Git LFS 또는 release asset 사용을 검토하세요.
