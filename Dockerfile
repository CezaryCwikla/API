FROM python:3

WORKDIR /api_czujnikow_rzek

ADD . /api_czujnikow_rzek

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY app.ini .

CMD [ "uwsgi", "app.ini" ]
