FROM python:3.11

SHELL ["/bin/bash", "-c"]

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev\
    libpq-dev gettext cron openssh-client locales vim

RUN useradd -rms /bin/bash dev && chmod 777 /opt /run

WORKDIR /shop_app

RUN mkdir /shop_app/static && mkdir /shop_app/media && chown -R dev:dev /shop_app && chmod 755 /shop_app

COPY --chown=dev:dev . .

RUN pip install -r requirements.txt

USER dev

CMD ["sh", "-c", "python3 gunicorn -b 0.0.0.0:8001 shop_app.wsgi:application"]



