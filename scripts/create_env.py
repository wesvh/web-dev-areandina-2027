"""Print private development settings for redirection into an ignored .env."""
import secrets

values = {
    'DJANGO_SECRET_KEY': secrets.token_hex(48),
    'DJANGO_DEBUG': 'False',
    'DJANGO_ALLOWED_HOSTS': 'localhost,127.0.0.1',
    'MYSQL_DATABASE': 'festival',
    'MYSQL_USER': 'festival',
    'MYSQL_PASSWORD': secrets.token_hex(24),
    'MYSQL_ROOT_PASSWORD': secrets.token_hex(24),
    'MYSQL_HOST': 'db',
    'MYSQL_PORT': '3306',
    'DEMO_ADMIN_USER': 'admin_demo',
    'DEMO_ADMIN_PASSWORD': secrets.token_hex(20),
    'WEB_PORT': '8000',
}
for key, value in values.items():
    print(f'{key}={value}')
