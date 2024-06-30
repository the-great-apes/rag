FROM python:3.11-slim

# copy data
WORKDIR /app
COPY . /app

# install deps
RUN apt  update && apt install -y git
RUN pip install -U -r requirements.txt
# pull data
RUN dvc update -R data/

# run pipeline
CMD ["dvc", "repro"]
