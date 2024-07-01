# aiquity Data Analyzer

To run this you have two options:
 - Either using the OpenAI API keys from the hackathon (or your own if you add them to the params.yml)
 - Or by creating a [Groq API Key](https://console.groq.com/keys) for free and adding it to the .env file

## Using OpenAI
You only need to make sure (by brute force trial) that your openAI API keys are valid. Make sure that you have access to something like gpt4o AND an embedding model like ada-02.
In the `params.yml`file make sure to set the `use_openai` setting to true.
```
use_openai: true
```
Run the docker container standalone or with the rest of the parent repository.

## Using Groq
As mentioned create a Groq API Key. Copy the `.env.template`-file in the parent repo, rename it to simply `.env` and edit the line with 
```
GROQ_API_KEY=yoUrApIkEY
```
to have your api key. Note that `.env` is in gitignore and won't be committed, s.t. your key is safe.
In the `params.yml`file make sure to set the `use_openai` setting to true.
```
use_openai: false
```
Run the docker container standalone or with the rest of the parent repository.

NOTE: For this version we run an embedding model locally on the GPU or CPU. For a GPU we recommend at least a `RTX3070`for doing so.
To switch between cpu or gpu please select in the parent repo which version to include:
```
include:
  - ./llm_service/cpu/docker-compose.yml #Comment this out 
  #- ./llm_service/cuda/docker-compose.yml # And uncomment this to use gpu
```
For using the cuda version, please note that you will have to have the gpu drivers, cuda drivers and the [container toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed on your system.

## Disable DVC to only upload data to mongodb
If you already have the data you needed with the llm gathered in the `data/summary/` folder and you only need the container to upload your data to the mongodb instance of the parent repo, disable DVC in the parent repos docker compose file like this:
Copy the `.env.template`-file in the parent repo, rename it to simply `.env` and edit the line with 

```
 RUN_DVC=false   
```