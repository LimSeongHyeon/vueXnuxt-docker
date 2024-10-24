FROM node:lts-alpine

RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    bash \
    git

WORKDIR /usr/src/app

COPY scripts/start.sh ./

RUN npm install -g npm@10.9.0
RUN npm install -g pm2

EXPOSE 3000

CMD [ "sh", "./start.sh" ]
