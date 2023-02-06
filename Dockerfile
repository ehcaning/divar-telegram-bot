FROM python:3.7
WORKDIR /app
RUN apt-get update && apt-get -y install python3-requests
RUN echo '[]' > /app/tokens.json
COPY run.sh /app/
COPY main.py /app/
# run crond as main process of container
ENTRYPOINT [ "/app/run.sh" ]
CMD ["python3", "-u", "main.py"]
