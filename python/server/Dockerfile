# FROM python:3.11-alpine
# WORKDIR /app # Enclave did not work with this line?
# RUN pip install --no-cache-dir web3==7.4.0
# COPY . .
# CMD ["python3", "server.py", "server", "5005"]


FROM python:3.11-alpine

RUN pip install --no-cache-dir web3==7.4.0

COPY server.py .

CMD ["/usr/local/bin/python3", "server.py", "server", "5005"]
