FROM python:3.12.3-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask

COPY . /sigma/sigma

WORKDIR /sigma/sigma

CMD ["python", "./work1.py"]
