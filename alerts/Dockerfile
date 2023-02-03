FROM python:3

RUN apt-get update && apt-get -y install cron chromium chromium-driver

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN (crontab -l -u root; echo '10 * * * * bash /app/updates.sh\n*/10 * * * * bash /app/alerts.sh\n') | crontab

RUN chmod 0744 updates.sh
RUN chmod 0744 alerts.sh

RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log