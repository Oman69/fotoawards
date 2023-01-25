from time import sleep

import jsonpickle


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
    if not self.is_aborted():
        foto.delete()
        print(f'Фото № {foto.pk} удалено. Task_id:{id_task}')
    else:
        return 'Задача остановлена'


def stop_deleting(task_id):
    stop = AbortableAsyncResult(task_id)
    stop.abort()