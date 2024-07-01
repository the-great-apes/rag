# Create a cuda ready image
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04 as cuda_base

RUN apt update && apt install -y git python3.11 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /root

RUN pip install torch torchvision torchaudio
COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

FROM cuda_base as llm_service_cuda

# copy data
WORKDIR /app
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
