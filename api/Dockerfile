FROM debian:stretch

RUN apt-get update \
 && apt-get install -y curl unzip \
    python3 python3-setuptools \
 && ln -s /usr/bin/python3 /usr/bin/python \
 && easy_install3 pip py4j \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONHASHSEED 0
ENV PYTHONIOENCODING UTF-8
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN python3 -m pip install --upgrade pip

EXPOSE 5050

WORKDIR /usr/
 
COPY ./startup.sh /usr/
COPY ./api.py /usr/
COPY ./model.py /usr/
COPY ./nltksetup.py /usr/
COPY ./requirements.txt /usr/
COPY ./models/ /usr/models

RUN chmod 755 /usr/startup.sh
RUN chmod 755 /usr/nltksetup.py

RUN pip install -r requirements.txt

RUN python3 nltksetup.py

CMD ["sh", "startup.sh"]