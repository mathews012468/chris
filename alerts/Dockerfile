FROM python:3

RUN apt-get update && apt-get -y install cron chromium chromium-driver

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

#I thought cron wasn't working and I spent a long time trying to figure out why it wasn't
#Turns out it was working, but my program was failing, and cron fails silently!!!!!
#I ended up verifying it was working by running a program every minute (* * * * *)
#that added some text to a file.
#Extremely valuable information on how to troubleshoot cron job:
#https://cronitor.io/cron-reference/crontab-not-working
RUN (crontab -l -u root; echo '10 * * * * bash /app/updates.sh\n*/10 * * * * bash /app/alerts.sh\n') | crontab

RUN chmod 0744 updates.sh
RUN chmod 0744 alerts.sh

RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log