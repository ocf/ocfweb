# A base ocfweb Dockerfile containing the code and dependencies.
# This doesn't run the website or the background worker; see Dockerfile.* for those.
FROM theocf/debian:bookworm AS base

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
        python3-dev \
        python3-pip \
        python3-virtualenv \
        python-is-python3 \
        redis-tools \
        runit \
        rustc \
        yui-compressor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN install -d --owner=nobody /opt/ocfweb /opt/ocfweb/venv /etc/ocfweb

COPY requirements.txt /opt/ocfweb/
RUN virtualenv -ppython3.11 /opt/ocfweb/venv \
    && /opt/ocfweb/venv/bin/pip install \
        -r /opt/ocfweb/requirements.txt

ARG ocflib_version=
RUN /opt/ocfweb/venv/bin/pip install ocflib${ocflib_version}

COPY bootstrap-scss /opt/ocfweb/bootstrap-scss/
COPY manage.py /opt/ocfweb/
COPY ocfweb /opt/ocfweb/ocfweb/
COPY conf /etc/ocfweb/
ENV MATPLOTLIBRC /etc/ocfweb

# Kubernetes will set this to 0, but we set it to 1 in case staff run this
# locally to prevent ocflib report emails.
ENV OCFWEB_TESTING 1

WORKDIR /opt/ocfweb

CMD ["runsvdir", "/opt/ocfweb/services"]

##########
# static #
##########

FROM base AS static

RUN /opt/ocfweb/venv/bin/pysassc /opt/ocfweb/ocfweb/static/scss/site.scss /opt/ocfweb/ocfweb/static/scss/site.scss.css
RUN find /opt/ocfweb/ocfweb/ \( -name '*.js' -o -name '*.css' \) -exec yui-compressor -o {} {} \;
RUN mkdir /opt/ocfweb/static
ENV OCFWEB_STATIC_ROOT /opt/ocfweb/static
RUN /opt/ocfweb/venv/bin/python /opt/ocfweb/manage.py collectstatic --noinput

COPY services/static /opt/ocfweb/services/static
RUN chown -R nobody:nogroup /opt/ocfweb/services

USER nobody

#######
# web #
#######

FROM base as web

COPY services/web /opt/ocfweb/services/
RUN chown -R nobody:nogroup /opt/ocfweb/services

USER nobody

##########
# worker #
##########

FROM base as worker

COPY services/worker /opt/ocfweb/services/worker
RUN chown -R nobody:nogroup /opt/ocfweb/services

USER nobody

# vim: ft=Dockerfile
