# --- ЭТАП 1: Сборка Vue приложения ---
FROM node:20-alpine AS builder
WORKDIR /app
# Копируем package.json и ставим зависимости
COPY compas-client/front/package*.json ./
RUN npm install
# Копируем весь исходный код фронтенда
COPY compas-client/front/ ./
# Собираем проект (появится папка dist)
RUN npm run build

# --- ЭТАП 2: Настройка Nginx ---
FROM nginx:stable-alpine

# Удаляем стандартный конфиг, чтобы он не мешал
RUN rm -f /etc/nginx/conf.d/default.conf

# Создаем наш конфиг с нуля прямо внутри образа через echo
# Это гарантирует, что там не будет лишних символов или дублей
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    \
    # Явно прописываем типы, чтобы браузер не скачивал файлы \
    types { \
        text/html html htm; \
        text/css css; \
        application/javascript js; \
        image/svg+xml svg; \
        image/png png; \
        image/jpeg jpg jpeg; \
        image/gif gif; \
        image/x-icon ico; \
        font/woff2 woff2; \
        font/woff woff; \
        application/json json; \
        model/gltf-binary glb; \
        model/gltf+json gltf; \
    } \
    \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    \
    location /api/ { \
        proxy_pass http://backend:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
    \
    location /admin/ { \
        proxy_pass http://backend:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Копируем собранные файлы из этапа builder
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]