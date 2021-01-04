FROM ubuntu:18.04

WORKDIR /usr/src/pss_app

COPY . .

RUN apt-get update

RUN apt install -y python3 python3-pip

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN echo "MODE = dev" > pss_app/.env

CMD ["python3", "pss_app/manage.py", "runserver", "0.0.0.0:8000","--settings=pss_app.settings.dev"]
