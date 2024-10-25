import docker
from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
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


def commandRun(command, workdir='/usr/src/app/front-deploy'):
    print(f"command > {command}")
    result = vue_container.exec_run(command, workdir=workdir)
    print(result.output.decode())
    print()


def reload_vue_container():
    try:
        # lock 설정
        open(lock_file, 'w').close()

        # Vue 컨테이너 내에서 명령어 실행
        commandRun("git reset --hard origin/release")
        commandRun("npm install --legacy-peer-deps --ignore-scripts")
        commandRun("npm run build")
        commandRun("pm2 restart front")

    finally:
        # lock 삭제
        os.remove(lock_file)

@app.post("/github-webhook")
async def handle_webhook(request: Request):
    # 헤더에서 웹훅 고유 값 추출 (예시로 'X-Hub-Signature-256' 사용)
    signature = request.headers.get("X-Hub-Signature-256")
    event = request.headers.get("X-GitHub-Event")
    payload = await request.json()
    raw_payload = await request.body()

    if os.path.exists(lock_file):
        raise HTTPException(status_code=429, detail="Build in progress")

    if not signature:
        raise HTTPException(status_code=403, detail="Missing X-Hub-Signature")

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=raw_payload, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403, detail="Invalid X-Hub-Signature")
    
    if event != "push":
        raise HTTPException(status_code=200, detail="Ignoring event other than 'push'")

    if payload.get("ref") != "refs/heads/release":
        raise HTTPException(status_code=200, detail="Ignoring branch other than 'release'")

    if payload.get("repository").get("full_name") != REPOSITORY:
        raise HTTPException(status_code=200, detail=f"Ignoring repository other than '{REPOSITORY}'")
    
    background_tasks.add_task(reload_vue_container)
    return {"status": "Build process started, frontend update will proceed in the background"}


