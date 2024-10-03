# Installing Dependencies and Building React Frontend
FROM node:20-alpine AS react-builder

WORKDIR /application/client

COPY /client/package.json /client/package-lock.json  ./

RUN npm install

COPY /client/src ./src
COPY /client/public ./public
# COPY next.config.mjs tailwind.config.ts postcss.config.mjs tsconfig.json ./
COPY /client/tsconfig.json ./

RUN npm run build

# Installing Dependencies FastAPI Backend
FROM python:3.11-alpine as python-builder

# TODO: Implementing python instalation build with UV

# Runtime
FROM python:3.11-alpine as runtime

# TODO: Getting from frontend stage /client/dist
# TODO: Getting from backend stage /server
