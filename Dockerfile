# A base ocfweb Dockerfile containing the code and dependencies.
# This doesn't run the website or the background worker; see Dockerfile.* for those.
FROM docker.ocf.berkeley.edu/theocf/debian:jessie

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        cracklib-runtime \
        libcrack2 \
        libcrack2-dev \
        libffi-dev \
        libfreetype6-dev \
        libpng12-dev \
        libssl-dev \
        libxft-dev \
        libxml2-dev \
        locales \
        python3 \
        python3-dev \
        python3-pip \
        redis-tools \
        runit \
        spiped \
        virtualenv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN install -d --owner=nobody /opt/ocfweb /opt/ocfweb/venv /etc/ocfweb

COPY requirements.txt /opt/ocfweb/
# TODO: We can't use libsass==0.11.1 in the Debian packaging yet, but we can here.
# We go to the pain of sed-ing it out because 0.11.1 has a manylinux wheel.
RUN sed -i 's/^libsass==.*/libsass==0.11.1/' /opt/ocfweb/requirements.txt
RUN virtualenv -ppython3 /opt/ocfweb/venv \
    && /opt/ocfweb/venv/bin/pip install pip==8.1.2 \
    && /opt/ocfweb/venv/bin/pip install \
        -r /opt/ocfweb/requirements.txt

COPY ocfweb /opt/ocfweb/ocfweb/
COPY conf /etc/ocfweb/
ENV MATPLOTLIBRC /etc/ocfweb

# Marathon will set this to 0, but we set it to 1 in case staff run this
# locally to prevent ocflib report emails.
ENV OCFWEB_TESTING 1

# Add services common to all the images. Other images might add more.
COPY services/redis-tunnel /opt/ocfweb/services/redis-tunnel

WORKDIR /opt/ocfweb

CMD ["runsvdir", "/opt/ocfweb/services"]
