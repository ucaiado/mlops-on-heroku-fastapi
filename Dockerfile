FROM continuumio/miniconda3:latest

# change user
USER root


# install linux dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim  wget curl gnupg2\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


# Install Heroku
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh


# Install AWS Cli
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         zip unzip less\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -f awscliv2.zip


# Install additional python packages
COPY environment.yml /tmp/
RUN conda env create -f tmp/environment.yml && \
    rm -rf /root/.cache


# Copy aditional files
COPY .netrc /root/


# Expose port 5000
EXPOSE 5000
