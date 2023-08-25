FROM python:3.7
WORKDIR /app
RUN apt-get update && pip install requests
RUN echo '[]' > /app/tokens.json
COPY main.py /app/
# run crond as main process of container
ENTRYPOINT [ "python3" ]
CMD ["main.py"]
