FROM nvidia/cuda:12.3.1-devel-ubuntu22.04

RUN apt-get update
RUN apt-get install -y python3-pip python3.10 python3-libnvinfer \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt 
