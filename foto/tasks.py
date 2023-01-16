import jsonpickle
from fotoawards.celery import app
from .service import send

@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task
def lazy_delete_foto(frozen):
    foto = jsonpickle.decode(frozen)
    print(f'Фото № {foto.pk} удалено')
    foto.delete()
