#!/bin/bash
dvc update -R data/ && dvc repro
