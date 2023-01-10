import redis
from django.core.mail import send_mail

def send(user_email):
    send_mail(
        'Вы подписались на рассылку',
        'Мы будем присылать Вам сообщения о новых фотографиях',
        'kirill.pochta1212@gmail.com',
        [user_email],
        fail_silently=False,

    )

'''
redis_client = redis.Redis(host='localhost', port=6379, db=0)
print(redis_client.set(name='name', value='John'))
redis_client.close()'''