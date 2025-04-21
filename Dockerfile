FROM python:3.12.10
LABEL description="Python science laboratory"
LABEL maintainer="samkennerly@gmail.com"

# Install system packages
RUN apt-get -y update && apt-get -y install cmake gcc less tree

# Install core Python packages
RUN pip3 install notebook pandas scipy

# Install extra Python packages
COPY requirements.txt /tmp
RUN pip3 install --requirement /tmp/requirements.txt

# Create user and context folder
RUN useradd --create-home kos
ENV PYTHONPATH=/home/kos/code
WORKDIR /home/kos

CMD ["/bin/bash"]
