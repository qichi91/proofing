# --- build stage ---
FROM node:20-alpine AS builder
WORKDIR /app
COPY app/package.json app/package-lock.json ./
RUN npm ci
COPY app .
RUN npm run build

# --- production stage ---
FROM nginx:1.25-alpine
WORKDIR /usr/share/nginx/html
COPY --from=builder /app/dist .
COPY app/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
