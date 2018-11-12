FROM python:3.7-alpine

RUN adduser -D wms

WORKDIR /home/wms

RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY wms.py config.py run.sh ./
RUN chmod a+x run.sh

ENV FLASK_APP wms.py

RUN chown -R wms:wms ./
USER wms

EXPOSE 5000
ENTRYPOINT ["./run.sh"]