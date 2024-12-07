FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="TutorCenterApp"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=80  
# Changed from 8000 to 80
ENV APP_HOST=app
ENV APP_PORT=8000 
# Changed from 9000 to 8000 to match app port

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]