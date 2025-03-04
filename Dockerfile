# LTS
ARG NODE_VERSION=20.14.0

FROM node:${NODE_VERSION}-alpine as base

ENV NODE_ENV=development

WORKDIR /src

# Build
FROM base as build

COPY package*.json ./

# RUN npm install
RUN npm cache clean --force && \
    npm install -g npm@latest && \
    npm i --legacy-peer-deps

# copia arquivos e pastas para o diretório atual de trabalho
COPY . .

# Run
FROM base

COPY --from=build /src/. /src/.

CMD [ "npm", "run", "dev" ]
