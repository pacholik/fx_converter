FROM python:3.9-slim AS python-build

RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        gcc \
        libpython3.7-dev \
    ; \
    rm -rf /var/lib/apt/lists/*;

WORKDIR /www/fx_converter/

COPY requirements.in .

RUN set -ex; \
    pip install setuptools wheel; \
    pip install --no-cache-dir -r requirements.in; \
    pip uninstall -y wheel setuptools

RUN mkdir /mnt/db
COPY fx_converter fx_converter
COPY uwsgi.ini uwsgi.py ./

RUN set -ex; \
    mkdir -p run; \
    useradd fx_converter; \
    chown fx_converter -R /www/fx_converter/

EXPOSE 3992 3992

CMD ["uwsgi", "/www/fx_converter/uwsgi.ini"]
