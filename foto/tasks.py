import jsonpickle
from fotoawards.celery import app
from .models import Foto
from .service import send
from celery.contrib.abortable import AbortableTask


@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task(bind=True, base=AbortableTask)
def lazy_delete_foto(self, frozen):
    foto_pk = jsonpickle.decode(frozen)['foto_pk']
    foto = Foto.objects.get(id=foto_pk)
    if foto.deleted:
        foto.delete()
    else:
        return 'Задача остановлена'
