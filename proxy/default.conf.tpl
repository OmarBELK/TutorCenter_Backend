server {
    listen ${LISTEN_PORT};

    # Frontend routes
    location / {
        proxy_pass http://localhost:82;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API routes
    location /api {
        uwsgi_pass ${APP_HOST}:${APP_PORT};
        include /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }

    # Static files
    location /static {
        alias /vol/static;
    }
}