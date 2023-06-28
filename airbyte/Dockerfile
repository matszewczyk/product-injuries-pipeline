FROM ubuntu:20.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN git clone https://github.com/airbytehq/airbyte.git /airbyte

WORKDIR /airbyte

ENTRYPOINT [ "executable" ]