FROM python:3.7
RUN apt-get update && apt-get -y install cron vim python3-requests
WORKDIR /app
COPY crontab /etc/cron.d/crontab
COPY main.py run.sh tokens.json /app/
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
ENTRYPOINT [ "/app/run.sh" ]
CMD ["cron","-f", "-l", "2"]
