#!/bin/bash

if [ "$RUN_DVC" = "true" ]; then
    dvc update -R data/
    dvc repro    
fi
python3 -m src.upload_to_mongodb