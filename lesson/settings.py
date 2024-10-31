# ... другие настройки ...

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Добавляем настройки для работы через туннель
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.localhost.run',
    '.lhr.life',
    '4fa056128b71fd.lhr.life'
]

# Настройки безопасности для работы через туннель
CSRF_TRUSTED_ORIGINS = [
    'https://*.localhost.run',
    'https://*.lhr.life',
    'https://4fa056128b71fd.lhr.life'
]

# Для разработки отключаем проверку HTTPS
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Для разработки можно использовать wildcard, но не рекомендуется для продакшена
# ALLOWED_HOSTS = ['*']