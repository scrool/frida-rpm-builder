FROM ubuntu:focal

# Setting up tzdata (2021e-0ubuntu0.20.04) ...
# debconf: unable to initialize frontend: Dialog
# debconf: (TERM is not set, so the dialog frontend is not usable.)
# debconf: falling back to frontend: Readline
# Define while the image is being built
ARG DEBIAN_FRONTEND=noninteractive
# TZ persists at runtime
ENV TZ=Etc/UTC

RUN apt-get update -y

# Dependencies from https://frida.re/docs/building/
RUN apt-get install -y \
    build-essential \
    curl \
    git \
    lib32stdc++-9-dev \
    libc6-dev-i386 \
    nodejs \
    npm \
    python3-dev \
    python3-pip

# Additional dependencies to run releng/release.py
# From: https://fpm.readthedocs.io/en/v1.13.1/installing.html
RUN apt-get install -y \
    ruby \
    ruby-dev \
    rubygems \
    build-essential
RUN gem install --no-document fpm

# Additional dependencies to create package for recent Fedora
# On Focal python3.10 is not available
# https://packages.ubuntu.com/search?keywords=python3.10
# so install it from ppa
# https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/
RUN apt-get install -y \
    software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-distutils

# Need executable 'rpmbuild' to convert python to rpm {:level=>:error}
RUN apt-get install -y \
    rpm

# Own build command
COPY build_rpm.py /build/
