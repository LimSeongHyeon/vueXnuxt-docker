
# Vue X Nuxt Docker 프로젝트

이 프로젝트는 Docker를 이용하여 Vue + Nuxt 기반의 리포지토리를 설정하고 실행하는 환경을 제공합니다.

.env파일을 구성하고 Docker에 등록하는 것으로 배포가 가능하며, Github의 Webhook을 이용하여 release branch로 push를 감지하여 재배포하는 기능으로 구성되어 있습니다.

## 요구 사항

- Docker
- Docker Compose

## 설정 사항

- Github Webhook 설정
- .env 설정
- 개인 환경 포트 설정

## 프로젝트 구조


- `docker-compose.yml`: Docker Compose로 Vue.js 애플리케이션 및 추가 서비스를 실행하기 위한 설정 파일입니다.
- `frontend/`: Vue X Nuxt 기반의 Front 셋업을 위한 디렉터리입니다.
  - `Dockerfile`: 메인 Vue.js 애플리케이션의 환경을 정의합니다.
  - `scripts/`: 셋업에 필요한 스크립트들을 포함하는 디렉토리입니다.
    - `scripts/start.sh`: clone을 하고 필요한 패키지를 설치하여 빌드하고 배포하는 스크립트입니다.
- `reloader/`: Python 기반의 리로더 서비스가 포함된 디렉터리입니다.
  - `requirements.txt`: 리로더 서비스의 Python 의존성 목록입니다.
  - `Dockerfile`: 리로더 서비스의 환경을 정의합니다.
  - `main.py`: 리로더 서비스의 메인 코드입니다.
- `nginx/`: frontend와 reloader를 분기시켜줄 nginx의 설정을 위한 디렉터리입니다.
  - `Dockerfile`: nginx에 대한 환경을 정의합니다.
  - `nginx.conf`: 실제로 사용할 nginx에 대한 설정 파일입니다. 
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
```

## 시작하기

### 1. 리포지토리 클론
가급적 clone보다는 파일로 받으시어 본인 설정에 알맞게 git을 사용하시는 것을 추천드립니다.

```bash
git clone https://github.com/LimSeongHyeon/vueXnuxt-docker
cd vue-docker
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 필요한 설정으로 수정이 필요합니다. 예시 값은 다음과 같습니다:

```
PRIVATE_KEY="ghp_PAT"
REPOSITORY="Owner/Repository"       
WEBHOOK_SECRET="LMZdaSnCkFIoO+Wi4K6YYkt2XBniflhB10yUoeC9Ml8HqP9uuA==
```



### 3. 프로젝트 빌드 및 실행

Docker Compose를 사용하여 프로젝트를 빌드하고 실행합니다.:

```bash
docker-compose up --build -d
```

이 명령어는 Vue.js 애플리케이션과 리로더 서비스를 실행합니다.



### 4. 서비스 중지

실행 중인 서비스를 중지하려면 다음 명령어를 사용합니다.:

```bash
docker-compose down
```


## 추가 정보

### 리로더 서비스
리로더 서비스는 애플리케이션의 변경 사항을 감지하여 자동으로 다시 로드하는 Python 기반의 서비스입니다. 해당 서비스는 `reloader` 디렉터리에 있으며, 의존성은 `requirements.txt` 파일에 정의되어 있습니다.

해당 기능을 이용하기 위해서 repository의 webhook 설정이 필요합니다.
자세한 내용은 [GitHub Webhook 설정 공식 문서](https://docs.github.com/ko/webhooks/using-webhooks/creating-webhooks)을 참조해주세요.

`WEBHOOK_SECRET`에 대한 값은 `openssl rand -base64 37`와 같이 본인이 원하는 방식으로 발급하시면 됩니다.


## 라이선스
이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 라이선스가 부여됩니다.
