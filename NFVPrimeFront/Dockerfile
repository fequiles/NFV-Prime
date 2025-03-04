# Stage 1 - build
FROM node:18.17.0 AS builder
WORKDIR /app
COPY --chown=node:node package*.json ./
COPY --chown=node:node next.config.js ./
RUN  npm install

# Stage 2 - production
FROM node:18.17.0 AS final
USER node
WORKDIR /home/node
ADD package.json .
ADD next.config.js .
COPY --chown=node:node --from=builder /app/node_modules ./node_modules
COPY --chown=node:node ./ ./
EXPOSE 8080
CMD ["npm", "run", "dev"]
