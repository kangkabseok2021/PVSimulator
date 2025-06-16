ARG PYTHON_VERSION=3.10

FROM python:$PYTHON_VERSION-slim-bookworm
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y -q --no-install-recommends \
    wget \
    ssh \
    git \
    git-lfs \
    build-essential \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/kangkabseok2021/PVSimulator.git
WORKDIR ./PVSimulator
RUN pip install --no-cache-dir -r ./requirements.txt
