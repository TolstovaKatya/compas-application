FROM node:20-alpine AS builder
WORKDIR /app
COPY compas-client/front/package*.json ./
RUN npm install
COPY compas-client/front/ ./
RUN npm run build

FROM nginx:stable-alpine
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]