FROM python:3.9.16-alpine
LABEL MAINTAINER="Katy Stuparu kastuparu@wpi.edu"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app

RUN addgroup -g $GROUP_ID flask-user
RUN adduser -D -u $USER_ID -G flask-user flask-user -s /bin/sh
USER flask-user

# CMD [ "python", "scout_app.py" ]
CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "scout_app:app"]