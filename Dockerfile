# A base ocfweb Dockerfile containing the code and dependencies.
# This doesn't run the website or the background worker; see Dockerfile.* for those.
FROM docker.ocf.berkeley.edu/theocf/debian:stretch

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        cracklib-runtime \
        libcrack2 \
        libcrack2-dev \
        libffi-dev \
        libfreetype6-dev \
        libpng-dev \
        libssl-dev \
        libxft-dev \
        libxml2-dev \
        locales \
        nginx \
        python3.7-dev \
        redis-tools \
        runit \
        virtualenv \
        yui-compressor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN install -d --owner=nobody /opt/ocfweb /opt/ocfweb/venv /etc/ocfweb

COPY requirements.txt /opt/ocfweb/
RUN virtualenv -ppython3.7 /opt/ocfweb/venv \
    && /opt/ocfweb/venv/bin/pip install pip==8.1.2 \
    && /opt/ocfweb/venv/bin/pip install \
        -r /opt/ocfweb/requirements.txt

ARG ocflib_version=
RUN /opt/ocfweb/venv/bin/pip install ocflib${ocflib_version}

COPY bootstrap-scss /opt/ocfweb/bootstrap-scss/
COPY manage.py /opt/ocfweb/
COPY ocfweb /opt/ocfweb/ocfweb/
COPY conf /etc/ocfweb/
ENV MATPLOTLIBRC /etc/ocfweb

# Marathon will set this to 0, but we set it to 1 in case staff run this
# locally to prevent ocflib report emails.
ENV OCFWEB_TESTING 1

WORKDIR /opt/ocfweb

CMD ["runsvdir", "/opt/ocfweb/services"]
