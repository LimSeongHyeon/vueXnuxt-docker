
# Vue X Nuxt Docker 프로젝트

이 프로젝트는 Docker를 이용하여 Vue.js 애플리케이션을 설정하고 실행하는 환경을 제공합니다. Docker Compose를 사용하여 구성되었으며, 리로더 서비스가 포함되어 있습니다.

## 요구 사항

- Docker
- Docker Compose

## 프로젝트 구조

- `Dockerfile`: 메인 Vue.js 애플리케이션의 환경을 정의합니다.
- `docker-compose.yml`: Docker Compose로 Vue.js 애플리케이션 및 추가 서비스를 실행하기 위한 설정 파일입니다.
- `scripts/start.sh`: 애플리케이션을 시작하는 스크립트입니다.
- `reloader/`: Python 기반의 리로더 서비스가 포함된 디렉터리입니다.
  - `requirements.txt`: 리로더 서비스의 Python 의존성 목록입니다.
  - `Dockerfile`: 리로더 서비스의 환경을 정의합니다.
  - `main.py`: 리로더 서비스의 메인 스크립트입니다.
- `.env`: 환경 변수를 설정하는 파일입니다.

## Vue X Nuxt 애플리케이션 실행

애플리케이션을 실행하기 위해서는 `package.json` 파일의 `scripts` 섹션에 `build`와 `start` 스크립트가 정의되어 있어야 합니다. 이 스크립트들은 애플리케이션의 빌드 및 실행을 자동화합니다.

`package.json`의 예시:

```json
{
  "scripts": {
    "build": "nuxt build",
    "start": "node .output/server/index.mjs"
  }
}


## 시작하기

### 1. 리포지토리 클론

```bash
git clone <repository-url>
cd vue-docker
```

### 2. 환경 변수 설정

`.env` 파일을 열어 필요한 설정으로 수정하세요. 예시 값은 다음과 같습니다:

```
PRIVATE_KEY="ghp_PAT"
REPOSITORY="Owner/Repository"       
WEBHOOK_SECRET="LMZdaSnCkFIoO+Wi4K6YYkt2XBniflhB10yUoeC9Ml8HqP9uuA==
```
`WEBHOOK_SECRET`에 대한 값은 `openssl rand -base64 37`와 같이 본인이 원하는 방식으로 발급하면 됩니다.
이후 Github에서 해당 repository의 webhook 설정이 필요합니다.
자세한 내용은 [GitHub Webhook 설정 공식 문서](https://docs.github.com/en/webhooks-and-events/webhooks/creating-webhooks)을 참조해주세요.

### 3. 프로젝트 빌드 및 실행

Docker Compose를 사용하여 프로젝트를 빌드하고 실행하세요:

```bash
docker-compose up --build
```

이 명령어는 Vue.js 애플리케이션과 리로더 서비스를 실행합니다.

### 4. 서비스 중지

실행 중인 서비스를 중지하려면 다음 명령어를 사용하세요:

```bash
docker-compose down
```

## 추가 정보

### 리로더 서비스

리로더 서비스는 애플리케이션의 변경 사항을 감지하여 자동으로 다시 로드하는 Python 기반의 서비스입니다. 해당 서비스는 `reloader` 디렉터리에 있으며, 의존성은 `requirements.txt` 파일에 정의되어 있습니다.

### 시작 스크립트

`start.sh` 스크립트는 애플리케이션을 설정하고 실행하는 과정을 자동화합니다. 스크립트에 실행 권한을 부여해야 합니다:

```bash
chmod +x scripts/start.sh
```

스크립트를 실행하여 애플리케이션을 시작하려면 다음 명령어를 사용하세요:

```bash
./scripts/start.sh
```

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 라이선스가 부여됩니다.