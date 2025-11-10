# Biblioteca personal con tareas asíncronas

Esta aplicación Flask permite gestionar una biblioteca personal y envía
notificaciones por correo electrónico cuando se agregan o eliminan libros. El
envío de correos se realiza como tareas asíncronas utilizando **Celery** y
**KeyDB** (compatible con Redis) como broker de mensajes.

## Requisitos

- Python 3.11+
- KeyDB o Redis accesible mediante `CELERY_BROKER_URL`
- Servidor SMTP accesible para enviar correos

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita el archivo `.env` con las credenciales de tu servidor SMTP y la URL de
KeyDB. Al iniciar la aplicación por primera vez se creará automáticamente la
base de datos SQLite definida en la configuración.

## Ejecución en desarrollo

En una terminal inicia la aplicación Flask:

```bash
flask --app manage.py run
```

En otra terminal arranca el worker de Celery apuntando al mismo archivo de
configuración:

```bash
celery -A celery_app.celery worker --loglevel=info
```

## Despliegue en producción

Para producción puedes ejecutar la aplicación con Gunicorn y un worker de
Celery independiente:

```bash
gunicorn wsgi:app
celery -A celery_app.celery worker --loglevel=info
```

Asegúrate de que Gunicorn y Celery compartan las mismas variables de entorno.
Cuando uses Nginx como proxy reverso únicamente redirige las peticiones HTTP a
Gunicorn.
