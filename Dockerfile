FROM ubuntu:jammy as dvc_base

RUN apt update && apt install -y git python3.11 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /root
COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

FROM dvc_base as llm_service

# Create the data directory so we do 
# not get errors if there is none
WORKDIR /root/dvc_pipeline/data/raw
COPY . /root/dvc_pipeline
WORKDIR /root/dvc_pipeline

#CMD ["tail", "-f", "/dev/null"]
ENTRYPOINT [ "./entrypoint.sh" ]
