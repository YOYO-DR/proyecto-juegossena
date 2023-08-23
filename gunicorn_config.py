# Número de procesos de trabajo para manejar las solicitudes
workers = 3

# Clase de trabajador a utilizar
worker_class = 'uvicorn.workers.UvicornWorker'

# Host y puerto en los que se escucharán las solicitudes
bind = '0.0.0.0:8000'

# Nivel de registro (opcional)
loglevel = 'info'

# en configuracion de configuracion de la app, en general settings, EXPLICAR
# gunicorn -c gunicorn_config.py config.asgi:application