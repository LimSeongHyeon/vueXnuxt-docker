#!/bin/sh

LOCK_FILE="/shared/build.lock"

# 잠금 파일 생성
echo "[배포를 시작합니다.]"
touch "$LOCK_FILE"
echo "LOCK FILE을 생성합니다.: $LOCK_FILE"
echo ""


# front-deploy 폴더가 없는 경우 GitHub에서 클론
if [ ! -d "./front-deploy" ]; then
  echo "[GitHub 리포지토리에서 클론합니다.]"
  
  # GitHub 프라이빗 리포지토리 클론
  git clone https://${PRIVATE_KEY}@github.com/${REPOSITORY}.git front-deploy
  
  # front-deploy 디렉토리로 이동
  cd front-deploy

  # release 브랜치로 변경
  git fetch
  git switch release

else
  # front-deploy 디렉토리로 이동
  cd front-deploy
fi
echo ""

# npm 패키지 설치
echo "[npm 패키지 설치를 진행합니다.]"
rm -rf node_modules package-lock.json yarn.lock
yarn install --ignore-scripts || { echo "npm install failed"; exit 1; }
echo ""

# Nuxt 앱 빌드
echo "[앱 빌드를 진행합니다.]"
yarn build || { echo "Build failed"; exit 1; }
echo ""

# lock 해제
echo "Removing lock file..."
echo "Lock file path: $LOCK_FILE"
ls -l "$LOCK_FILE"
rm -f "$LOCK_FILE"
echo "Lock file removed."

# Nuxt 앱 실행
echo "[앱 실행을 진행합니다.]"
pm2-runtime start "yarn start" --name front || { echo "Failed to start app"; exit 1; }
echo ""