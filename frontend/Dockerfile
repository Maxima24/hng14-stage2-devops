FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm install

FROM node:20-alpine
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
  CMD wget -qO- http://localhost:3000 || exit 1
CMD ["node", "app.js"]