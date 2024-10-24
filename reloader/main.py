import docker
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

app = FastAPI()
client = docker.from_env()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

@app.post("/webhook")
async def handle_webhook(request: Request):

    # 헤더에서 웹훅 고유 값 추출 (예시로 'X-Hub-Signature-256' 사용)
    signature = request.headers.get("X-Hub-Signature-256")

    # 고유 값 비교
    if signature != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid Webhook Signature")

    payload = await request.json()

    # GitHub에서 release 브랜치에 대한 푸시 이벤트인지 확인
    if payload.get("ref") == "refs/heads/release":
        # Vue 컨테이너 가져오기
        vue_container = client.containers.get("vue-front")

        # Vue 컨테이너 내에서 명령어 실행
        vue_container.exec_run("git reset --hard origin/release")
        vue_container.exec_run("npm install")
        vue_container.exec_run("npm run build")
        vue_container.exec_run("npm run start")

    return {"status": "Frontend updated"}
