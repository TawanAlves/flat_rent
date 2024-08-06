from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Definir o módulo de configuração do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flatrent.settings')

app = Celery('flatrent')

# Usar uma string aqui significa que o Celery não precisa serializar o objeto configuração para o worker
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregar tarefas de todos os aplicativos registrados no Django
app.autodiscover_tasks()
