FROM python:3.10

COPY requirements.txt /app/
WORKDIR /app
RUN python -m pip install -U pip && pip install -r requirements.txt
RUN echo '[]' > /app/tokens.json
COPY main.py /app/
# run crond as main process of container
ENTRYPOINT [ "python3" ]
CMD ["main.py"]
