FROM {tag}

RUN /opt/ocfweb/venv/bin/pysassc /opt/ocfweb/ocfweb/static/scss/site.scss /opt/ocfweb/ocfweb/static/scss/site.scss.css
RUN find /opt/ocfweb/ocfweb/ \( -name '*.js' -o -name '*.css' \) -exec yui-compressor -o {} {} \;
RUN mkdir /opt/ocfweb/static
ENV OCFWEB_STATIC_ROOT /opt/ocfweb/static
RUN /opt/ocfweb/venv/bin/python /opt/ocfweb/manage.py collectstatic --noinput

COPY services/static /opt/ocfweb/services/static
RUN chown -R nobody:nogroup /opt/ocfweb/services

USER nobody

# vim: ft=Dockerfile
