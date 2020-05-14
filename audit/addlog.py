from .models import CeleryTaskAudit
from user.models import User


def add_tasks_log(type):
    def func_all(fc):
        def wrapper(request):
            username = request.user.username
            username_obj = User.objects.get(username=username)
            task_log = CeleryTaskAudit()
            task_log.task = type
            task_log.user = username_obj
            task_log.save()
            return fc(request)
        return wrapper
    return func_all

