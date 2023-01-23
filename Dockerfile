FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /usr/src/fotoawards

COPY ./requirements.txt /usr/src/fotoawards/requirements.txt
RUN pip install -r /usr/src/fotoawards/requirements.txt

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]