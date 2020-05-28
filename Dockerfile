FROM python:3-alpine

LABEL maintainer="w.fantom@lancaster.ac.uk"

RUN pip install pyxs unimon-ctl

ENTRYPOINT [ "unimon-ctl" ]