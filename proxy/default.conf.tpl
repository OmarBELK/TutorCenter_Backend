server {
    listen ${LISTEN_PORT};
    server_name deltainstitut.app www.deltainstitut.app;  # Added server_name
    server_tokens off;

    location / {
        proxy_pass http://frontend:82;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
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