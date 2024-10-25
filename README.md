<br><br>
# Vue X Nuxt Docker 프로젝트

이 프로젝트는 Docker를 이용하여 Vue + Nuxt 기반의 리포지토리를 설정하고 실행하는 환경을 제공합니다. 

.env 파일을 구성하고 Docker에 등록하여 배포가 가능하며, Github의 Webhook을 이용하여 release 브랜치로 push를 감지하여 재배포하는 기능을 제공합니다.

<br><br>

## 목차
1. [요구 사항](#요구-사항)
2. [설정 사항](#설정-사항)
3. [프로젝트 구조](#프로젝트-구조)
4. [Vue X Nuxt 애플리케이션 실행](#vue-x-nuxt-애플리케이션-실행)
5. [시작하기](#시작하기)
6. [추가 정보](#추가-정보)
7. [라이선스](#라이선스)

<br><br>

## 요구 사항

- Docker
- Docker Compose

<br><br>

## 설정 사항

- Github Webhook 설정
- .env 설정
- 개인 환경 포트 설정

<br><br>


## 프로젝트 구조

- `docker-compose.yml`: Docker Compose로 Vue.js 애플리케이션 및 추가 서비스를 실행하기 위한 설정 파일
<br>

- `frontend/`: Vue X Nuxt 기반의 Front 셋업을 위한 디렉터리
  - `Dockerfile`: 메인 Vue.js 애플리케이션의 환경 정의
  - `scripts/`: 셋업에 필요한 스크립트들이 포함된 디렉터리
    - `scripts/start.sh`: 클론 후 패키지 설치 및 빌드 배포 스크립트
<br>

- `reloader/`: Python 기반의 리로더 서비스가 포함된 디렉터리
  - `requirements.txt`: 리로더 서비스의 Python 의존성 목록
  - `Dockerfile`: 리로더 서비스의 환경 정의
  - `main.py`: 리로더 서비스의 메인 코드
<br>

- `nginx/`: frontend와 reloader를 분기시켜줄 nginx의 설정 디렉터리
  - `Dockerfile`: nginx 환경 정의
  - `nginx.conf`: nginx 설정 파일
<br>

- `.env`: 환경 변수를 설정하는 파일


<br><br>


## Vue X Nuxt 애플리케이션 실행

애플리케이션을 실행하려면 `package.json`의 `scripts` 섹션에 빌드 및 실행 스크립트가 정의되어 있어야 합니다.

```json
{
  "scripts": {
    "build": "nuxt build",
    "start": "node .output/server/index.mjs"
  }
}
```


<br><br>


## 시작하기

### 1. 리포지토리 클론

```bash
git clone https://github.com/LimSeongHyeon/vueXnuxt-docker
cd vue-docker
```
<br>


### 2. 환경 변수 설정

`.env` 파일을 생성하고 필요한 설정을 적용합니다:

```
PRIVATE_KEY="ghp_PAT"
REPOSITORY="Owner/Repository"       
WEBHOOK_SECRET="LMZdaSnCkFIoO+Wi4K6YYkt2XBniflhB10yUoeC9Ml8HqP9uuA==
```
<br>


### 3. 프로젝트 빌드 및 실행

```bash
docker-compose up --build -d
```

이 명령어는 Vue.js 애플리케이션과 리로더 서비스를 실행합니다.
<br>


### 4. 서비스 중지

```bash
docker-compose down
```


<br><br>


## 추가 정보

### 리로더 서비스

리로더 서비스는 애플리케이션의 변경 사항을 감지하여 자동으로 다시 로드하는 Python 기반의 서비스입니다. `reloader` 디렉터리 내에 있으며, 의존성은 `requirements.txt`에 정의되어 있습니다.

Github Webhook 설정이 필요하며, 자세한 내용은 [GitHub Webhook 설정 공식 문서](https://docs.github.com/ko/webhooks/using-webhooks/creating-webhooks)를 참조해주세요.

`WEBHOOK_SECRET` 값은 `openssl rand -base64 37` 명령어를 사용해 발급할 수 있습니다.


<br><br>


## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 배포됩니다.
<br>
