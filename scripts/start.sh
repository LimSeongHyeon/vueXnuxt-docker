#!/bin/sh

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
npm install --legacy-peer-deps --ignore-scripts || { echo "npm install failed"; exit 1; }
echo ""

# Nuxt 앱 빌드
echo "[앱 빌드를 진행합니다.]"
npm run build || { echo "Build failed"; exit 1; }
echo ""

# Nuxt 앱 실행
echo "[앱 실행을 진행합니다.]"
npm run start || { echo "Failed to start app"; exit 1; }
echo ""
