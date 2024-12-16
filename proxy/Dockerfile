FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="GenericMLApp"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8001
ENV APP_HOST=app
ENV APP_PORT=9000
ENV DOMAIN_NAME=localhost
ENV HTTP_PORT=81
ENV HTTPS_PORT=444

USER root

RUN mkdir -p /vol/static && \
    mkdir -p /etc/nginx/ssl && \
    chmod 755 /vol/static && \
    chmod 755 /etc/nginx/ssl && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chown -R nginx:nginx /etc/nginx/ssl && \
    chmod +x /run.sh

VOLUME /vol/static
VOLUME /etc/nginx/ssl

USER nginx

CMD ["/run.sh"]