FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install --no-install-recommends -y \
  gettext=0.* \
  pipenv=2022.12.* \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

COPY ./Pipfile* /opt/
RUN pipenv install --ignore-pipfile --system --dev

WORKDIR /etip/etip

COPY ./docker/entrypoint.sh /entrypoint.sh
COPY ./ /etip

ENTRYPOINT ["/entrypoint.sh"]
CMD ["init"]
