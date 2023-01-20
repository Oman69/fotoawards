import jsonpickle
from celery.worker.control import revoke
from django.core.cache import cache

from fotoawards.celery import app
from .service import send
from celery.contrib.abortable import AbortableTask, AbortableAsyncResult
from celery.utils.log import get_task_logger


@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task(bind=True, base=AbortableTask)
def lazy_delete_foto(self, frozen):
    id_task = str(self.request.id)
    foto = jsonpickle.decode(frozen)
    print(f'Фото № {foto.pk} удалено. Task_id:{id_task}')
    if not self.is_aborted():
        foto.delete()
    else:
        revoke(task_id=id_task, terminate=True)
        return 'Задача остановлена'


def stop_deleting():
    stop = AbortableAsyncResult(id=str(lazy_delete_foto))
    stop.abort()