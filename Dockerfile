FROM python:2.7-slim
LABEL maintainer="Tong Zhang <zhangt@frib.msu.edu>"

WORKDIR "/phyapps"
ADD phycloud.tar.bz2 .

RUN mkdir notebooks && pip install -r requirements.txt

EXPOSE 5050

CMD ["sh", "-c", "python run.py"]
