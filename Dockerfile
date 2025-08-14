FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python packages
RUN pip3 install --upgrade pip
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Set working directory
WORKDIR /app
COPY . /app

CMD ["python3", "main.py"]