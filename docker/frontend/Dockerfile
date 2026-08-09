FROM node:20-alpine as build-stage
WORKDIR /app

# Путь ОТ КОРНЯ РЕПО (так как context: ..)
COPY compas-client/front/package*.json ./
RUN npm install

# Копируем весь фронтенд
COPY compas-client/front/ ./

RUN npm run build

FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf
# Копируем твой конфиг из папки docker/frontend
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# ПРОВЕРЬ ИМЯ ПАПКИ ЗДЕСЬ! Если у тебя vite - то dist. Если react - то build.
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]