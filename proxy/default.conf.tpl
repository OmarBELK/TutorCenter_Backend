server {
    listen ${LISTEN_PORT};

    # Frontend routes
    location / {
        proxy_pass http://frontend:82;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
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