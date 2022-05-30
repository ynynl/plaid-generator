# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD . /app
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "app.wsgi:app"]

# COPY . .
# EXPOSE 5000
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app"]


# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

