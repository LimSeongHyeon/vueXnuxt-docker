import docker
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import os
import hmac
import hashlib

app = FastAPI()
client = docker.from_env()
vue_container = client.containers.get("frontend")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
REPOSITORY = os.getenv("REPOSITORY")
lock_file = "/shared/build.lock"


def checkSignature(signature, payload):
    if not signature:
        raise HTTPException(status_code=403, detail="Missing X-Hub-Signature")

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403, detail="Invalid X-Hub-Signature")


@app.post("/github-webhook")
async def handle_webhook(request: Request):
    # 헤더에서 웹훅 고유 값 추출 (예시로 'X-Hub-Signature-256' 사용)
    signature = request.headers.get("X-Hub-Signature-256")
    event = request.headers.get("X-GitHub-Event")
    payload = await request.json()

    checkSignature(signature, await request.body())
    
    if event != "push":
        raise HTTPException(status_code=200, detail="Ignoring event other than 'push'")

    if payload.get("ref") != "refs/heads/release":
        raise HTTPException(status_code=200, detail="Ignoring branch other than 'release'")

    if os.path.exists(lock_file):
        raise HTTPException(status_code=429, detail="Build in progress")

    try:
        # lock 설정
        open(lock_file, 'w').close()
        print(payload.get("repository").get("full_name"))

        # GitHub에서 release 브랜치에 대한 푸시 이벤트인지 확인
        if payload.get("ref") == "refs/heads/release":
            # Vue 컨테이너 내에서 명령어 실행
            vue_container.exec_run("cd /usr/src/app/front-deploy")
            vue_container.exec_run("git reset --hard origin/release")
            vue_container.exec_run("npm install --legacy-peer-deps --ignore-scripts")
            vue_container.exec_run("npm run build")
            vue_container.exec_run("pm2 restart front")

        return {"status": "Frontend updated"}

    finally:
        # lock 삭제
        os.remove(lock_file)
