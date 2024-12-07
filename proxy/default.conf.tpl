server {
    listen ${LISTEN_PORT};
    server_name deltainstitut.app www.deltainstitut.app;
    server_tokens off;

    location / {
        proxy_pass http://frontend:82;
    }

    location /api {
        uwsgi_pass ${APP_HOST}:9000;
        include /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }

    location /static {
        alias /vol/static;
    }
}