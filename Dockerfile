FROM python:2

WORKDIR /api_czujnikow_rzek

ADD . /api_czujnikow_rzek

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uwsgi", "app.ini" ]