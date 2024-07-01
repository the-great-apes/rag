FROM ubuntu:jammy as cpu_base

RUN apt update && apt install -y git python3.11 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /root
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt
RUN cat 

FROM cpu_base as nlp_service

# copy data
WORKDIR /app
COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]