# React (Node.js) Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . /app
# COPY ./public /app/public

RUN npm run build
CMD ["npm", "run", "start"]