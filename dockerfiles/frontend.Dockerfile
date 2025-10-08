FROM node:24

WORKDIR /frontend

COPY ./frontend .

RUN npm install
