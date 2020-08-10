FROM python:3.7

LABEL maintainer="jadbin <jadbin.com@hotmail.com>"

ENV PIP_INDEX https://pypi.doubanio.com/simple/

ADD ./ /opt/cloudfunc
RUN pip install -e /opt/cloudfunc --index ${PIP_INDEX} \
  && pip install "gevent>=20.6.2"  --index ${PIP_INDEX}
