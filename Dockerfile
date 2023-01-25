FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /usr/src/fotoawards

COPY ./requirements.txt /usr/src/fotoawards/requirements.txt
RUN pip install -r /usr/src/fotoawards/requirements.txt

COPY .  /usr/src/fotoawards

CMD [ "python3", "manage.py", "runserver", "127.0.0.1:8000"]