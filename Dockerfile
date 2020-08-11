FROM tiangolo/uvicorn-gunicorn-fastapi

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

RUN mkdir /app/test/
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["/start.sh"]