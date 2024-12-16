FROM python:3-alpine

RUN mkdir -p /app
ADD app/requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
ADD app/main.py /app
ADD app/models.py /app

CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]