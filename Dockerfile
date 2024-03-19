FROM ubuntu:20.04

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

WORKDIR /app
ADD . /app

RUN set -xe \
    && apt-get update -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        python3-pip \
        openssl \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && openssl req -x509 -newkey rsa:4096 -keyout /app/keyfile.pem -out /app/certfile.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/OU=Organizational Unit/CN=localhost"

COPY . .
RUN pip install -r requirements.txt

# Make port 443 available to the world outside this container
# EXPOSE 443

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint script
# ENTRYPOINT ["/entrypoint.sh"]

# Run app.py when the container launches
# CMD ["uvicorn", "wedding_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--ssl-keyfile", "/app/keyfile.pem", "--ssl-certfile", "/app/certfile.pem"]
CMD ["uvicorn", "wedding_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]