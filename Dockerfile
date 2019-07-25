FROM python:3.6.9-alpine
LABEL maintainer="Tong Zhang <zhangt@frib.msu.edu>"

WORKDIR "/phyapps"

ADD requirements-freezed.txt .
RUN apk add --no-cache py3-cffi py3-openssl

RUN mkdir notebooks && \
    pip install --no-cache-dir -r requirements-freezed.txt

ADD phycloud.tar.bz2 .

EXPOSE 5050

CMD ["sh", "-c", "python application.py"]
