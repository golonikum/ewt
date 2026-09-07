FROM nginx:1.20-alpine
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY htdocs/media /usr/share/nginx/media
