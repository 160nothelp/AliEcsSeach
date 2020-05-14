import os
from celery import Celery, platforms
from datetime import timedelta
from kombu import Exchange, Queue


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliyunCenter.settings')
app = Celery("MyCelery")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
platforms.C_FORCE_ROOT = True


CELERY_QUEUES = (
    Queue("default", Exchange("default", type='direct'), routing_key="default"),
    Queue("for_task_search", Exchange("for_task_search", type='direct'), routing_key="for_task_search"),
    Queue("for_task_setCache", Exchange("for_task_setCache", type='direct'), routing_key="for_task_setCache"),
)


CELERY_ROUTES = {
    'aliecs.tasks.SearchHostIp': {"queue": "for_task_search", "routing_key": "for_task_search"},
    'aliecs.tasks.SearchHostInstancename': {"queue": "for_task_search", "routing_key": "for_task_search"},
    'aliecs.tasks.SetEcsCache': {"queue": "for_task_setCache", "routing_key": "for_task_setCache"},
    'ops.tasks.SwitchDomain': {"queue": "for_task_search", "routing_key": "for_task_search"},
    'ops.tasks.tmpCytIptables': {"queue": "for_task_search", "routing_key": "for_task_search"},
    'ops.tasks.createshadowsocket': {"queue": "for_task_search", "routing_key": "for_task_search"},
    'ops.tasks.createforward': {"queue": "for_task_search", "routing_key": "for_task_search"},
}


app.conf.update(CELERY_QUEUES=CELERY_QUEUES, CELERY_ROUTES=CELERY_ROUTES)


app.conf.update(
    CELERY_BEAT_SCHEDULE={
        'Cache_Ecs_Data': {
            'task': 'aliecs.tasks.SetEcsCache',
            'schedule': timedelta(seconds=60*5),
        },
    }
)

