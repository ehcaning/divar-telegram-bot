FROM python:3.7
WORKDIR /app
RUN apt-get update && pip install requests
RUN echo '[]' > /app/tokens.json
COPY run.sh /app/
COPY main.py /app/
# run crond as main process of container
ENTRYPOINT [ "/app/run.sh" ]
CMD ["python3", "main.py"]
