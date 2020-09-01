FROM nginx

COPY nginx.conf /etc/nginx/conf.d/anarchonet.conf
COPY static /etc/static/static
