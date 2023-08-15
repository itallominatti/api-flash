FROM python:3.9-slim-bullseye
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  apt-get install -y locales && \
  sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales

RUN apt-get update && apt-get install -y firefox-esr
RUN apt-get install -y nginx

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
ENV TZ America/Recife

RUN pip list

RUN pip install pipenv


WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN pipenv install

COPY . /code/


EXPOSE 8080

CMD ["pipenv", "run", "exec_server"]