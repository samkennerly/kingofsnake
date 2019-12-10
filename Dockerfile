FROM python:3.8.0
LABEL description="Python science laboratory"
LABEL maintainer="samkennerly@gmail.com"

# Install system packages
RUN apt-get -y update && apt-get -y install less tree vim

# Install Python packages
COPY requirements.txt /tmp
RUN pip install --upgrade pip && pip install --requirement /tmp/requirements.txt


RUN useradd --create-home kos
ENV PYTHONPATH=/context/code
WORKDIR /context

CMD ["/bin/bash"]
