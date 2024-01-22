FROM node:20.9.0-alpine3.18

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY public/ ./public
COPY src/ ./src

CMD ["npm", "start"]
