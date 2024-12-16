#!/bin/sh

set -e

# Print environment variables for debugging
echo "DOMAIN_NAME=${DOMAIN_NAME}"
echo "HTTP_PORT=${HTTP_PORT}"
echo "HTTPS_PORT=${HTTPS_PORT}"

# Ensure environment variables are set
: "${DOMAIN_NAME:?DOMAIN_NAME is not set}"
: "${HTTP_PORT:?HTTP_PORT is not set}"
: "${HTTPS_PORT:?HTTPS_PORT is not set}"

envsubst '$DOMAIN_NAME $HTTP_PORT $HTTPS_PORT $APP_HOST $APP_PORT' < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Print the generated config for debugging
echo "Generated Nginx config:"
cat /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'