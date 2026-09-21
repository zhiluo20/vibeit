FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server git && rm -rf /var/lib/apt/lists/* && useradd -m -s /bin/bash student && mkdir -p /run/sshd
RUN pip install --no-cache-dir numpy pandas matplotlib ipykernel
COPY run.sh /usr/local/bin/run-tutorial-ssh
RUN chmod 755 /usr/local/bin/run-tutorial-ssh
EXPOSE 22
ENTRYPOINT ["/usr/local/bin/run-tutorial-ssh"]
