FROM python:3.7.6
LABEL description="Python science laboratory"
LABEL maintainer="samkennerly@gmail.com"

# Install system packages
RUN apt-get -y update && apt-get -y install cmake gcc less tree

# Install major stack components
RUN pip install --upgrade pip && pip install notebook==6.0 pandas==0.25 scipy==1.4

# Install other Python packages
COPY requirements.txt /tmp
RUN pip install --upgrade pip && pip install --requirement /tmp/requirements.txt

# Create user and context folder
RUN useradd --create-home kos
ENV PYTHONPATH=/context/code
WORKDIR /context

CMD ["/bin/bash"]
