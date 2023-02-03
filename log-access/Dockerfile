FROM python:3

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD gunicorn -b 0.0.0.0:8000 app:app

#docker build . -t log-access
#docker run --name log-cont -dp 80:8000 log-access