FROM python:3.7.1-stretch

ENV PROJ pykafka_debug
ENV ROOT /opt/$PROJ

RUN mkdir -p $ROOT/bin
RUN mkdir -p $ROOT/etc
RUN mkdir -p $ROOT/usr/share

ADD pykafka_debug.py $ROOT/bin
ADD requirements.txt $ROOT/usr/share

RUN find $ROOT

RUN pip install -r $ROOT/usr/share/requirements.txt

CMD [ "sh", "-c", "exec python ${ROOT}/bin/pykafka_debug.py" ]
