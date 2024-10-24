FROM python:3.9-slim

WORKDIR /usr/src/reloader

# FastAPI 및 의존성 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 앱 복사
COPY . .

# FastAPI 앱 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]
