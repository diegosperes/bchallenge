from alpine:3.8

COPY . /app
WORKDIR /app

RUN apk update \
    && apk upgrade \
    && apk add make \
    && apk add python3 \
    && apk add nginx \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
    && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
    && make setup

EXPOSE 8000

CMD ["python", "-m", "b2w.server"]
