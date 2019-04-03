FROM python:3.7

WORKDIR /opt/base_app

COPY config/requirements.txt requirements.txt

# first time (usually cached by Docker)
RUN pip install --upgrade --requirement requirements.txt

COPY src .

# second time (upgrade all requirements)
RUN pip install --upgrade --requirement requirements.txt

CMD ["./manage.py", "runserver", "localhost:8000"]

ARG APP_VERSION=latest
