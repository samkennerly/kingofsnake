FROM python:3.8.2
LABEL description="Python science laboratory"
LABEL maintainer="samkennerly@gmail.com"

# Install system packages
RUN apt-get -y update && apt-get -y install cmake gcc less tree

# Install major stack components
RUN pip install --upgrade pip && pip install \
    notebook==6.0.3 \
    pandas==1.0.1 \
    scipy==1.4.1

# Install other Python packages
COPY requirements.txt /tmp
RUN pip install --upgrade pip && pip install --requirement /tmp/requirements.txt

# Create user and context folder
RUN useradd --create-home kos
ENV PYTHONPATH=/context/code
WORKDIR /context

CMD ["/bin/bash"]
