FROM python:3.7.5
LABEL description="Python development sandbox"
LABEL maintainer="samkennerly@gmail.com"

# Install system packages
RUN apt-get -y update && apt-get -y install less tree vim

# Install Python packages
COPY requirements.txt /tmp
RUN pip install --upgrade pip && pip install --requirement /tmp/requirements.txt

# Copy repo files (unless .dockerignore)
ENV PATH="/context/bin:${PATH}" PYTHONPATH="/context/src"
COPY [".", "/context"]
WORKDIR '/context'

CMD ["/bin/bash"]
