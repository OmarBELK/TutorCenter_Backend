server {
    listen ${LISTEN_PORT};

    location / {
        proxy_pass http://frontend:82;
    }

    location /api {
        uwsgi_pass ${APP_HOST}:${APP_PORT};
        include /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }

    location /static {
        alias /vol/static;
    }
}