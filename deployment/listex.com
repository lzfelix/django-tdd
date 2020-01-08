server {
    listen 80;
    server_name listex.com;

    location /static {
        alias /var/www/django-tdd/superlists/static_content;
    }

    location / {
        proxy_pass http://localhost:8000;
    }
}
