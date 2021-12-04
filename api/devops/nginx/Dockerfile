FROM nginx:1.16.0

RUN rm -rf /etc/nginx/conf.d/*
COPY --chown=root:root housing-units-api-nginx.conf /etc/nginx/conf.d/housing-units-api-nginx.conf
RUN chmod 600 /etc/nginx/conf.d/housing-units-api-nginx.conf
